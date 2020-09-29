# SPDX-License-Identifier: BSD-3-Clause

import json
import sys
import os
import msgbroker
import datetime
import pv_gen


class PVSim(object):
    """ This is a class that performs a very simple simulation a photo voltaic
    (PV) system output. The class listens to a broker for values sent from
    another process that simulates a household meter. The received meter value
    and the generated PV are saved, along with the sum of both values and the
    timestamp (seconds since epoch) of the execution time.

    :param pv_generator: An object that generates a PV value according to its internal implementation.  
    :type pv_generator: class: `pv_gen.PVGenerator`
    :param broker: The type of the message broker. It defaults to
    msgbroker.RabbitMQBroker().
    :param fname: The file to output the generated values.
    :type fname: str
    """

    def __init__(self, pv_generator, broker, fname=None):
        if not fname:
            fname = "pv-data.csv"

        self.pv_generator = pv_generator
        self.broker = msgbroker.MsgBroker(broker)
        self.save_file = open(fname, 'w')
        self.start_time = None

    def _handle_msg(self, ch, method, properties, body):

        # If executed as a standalone program, the program exits after
        # receiving a finish message.
        # If running inside a thread, the sys.exit will just exit the thread
        # which gives a similar effect to terminating the program.
        if body.decode('utf-8') == "finish":
            self.stop()
            sys.exit(0)

        # Parse the json body, converting the meter value from Watts to Kw
        msg = json.loads(body)
        time = next(iter(msg))
        meter_value = float(msg[time]) / 1000

        # The start time is used to calculate how much time has elapsed
        # since the start of the simulation.
        if not self.start_time:
            self.start_time = float(time)

        # The generation of value uses the elapsed time as an argument.
        # This decision simplifies the generation of PV by requiring only
        # information about the current day time.
        time_elapsed = float(time) - self.start_time
        pv_value = self.pv_generator.gen_value(time_elapsed)

        pv_sum = meter_value + pv_value
        self.save_file.write(f"{time},{meter_value},{pv_value},"
                             f"{pv_sum}\n")

    def run(self):
        """ Runs the PV simulator by subscribing to the meter queue. 
        """
        self.broker.subscribe('meter', self._handle_msg)

    def stop(self):
        """ Closes the file used to write the information
        """
        self.save_file.close()
