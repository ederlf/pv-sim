# SPDX-License-Identifier: BSD-3-Clause

import json
import datetime
import random
import argparse
import msgbroker


parser = argparse.ArgumentParser()

parser.add_argument(
    "-b", "--broker", help="Chooses the msg broker. If not set, the simulator "
    "uses rabbitmq", default="rabbitmq")
parser.add_argument(
    "--broker_ip", help="Sets the IP location of the broker. If not set, "
    "localhost (127.0.0.1) is used")
parser.add_argument(
    "--broker_port", help="Sets the TCP port used to connect to the broker. If"
    " not set, uses the default of the selected broker")
parser.add_argument("-d", "--duration", type=int,
                    help="Sets the duration of the simulated time, in seconds."
                    "If not set, defaults to one day (86400 seconds)",
                    default=86400)
parser.add_argument("-s", "--step", type=int,
                    help="Sets the advance of time and the interval of meter "
                    "messages, in seconds. If not set, the simulator uses 5 "
                    "seconds If not set, defaults to one day (86400 seconds)",
                    default=5)
parser.add_argument("--seed", type=int,
                    help="Sets the seed for the random number generation. If "
                    "not set, the simulator uses 42", default=42)


class Meter(object):
    """ This class simulates a meter from a household that sends measurements 
    on a configurable interval

    :param start: the initial time of the simulation. The default is the 
    current time
    :type start: datetime
    :param duration: Total simulated time, in seconds.
    :type duration: int
    :param step: The intervals in which measurements are sent.
    :type: int
    :param broker: The type of the broker that will be used to exchange 
    messages. The default is rabbitmq
    :param seed: Set the seed of the random number generator. Useful for 
    reproducibility
    :seed: int
    """

    def __init__(self, duration, step, broker, seed,
                 start=datetime.datetime.now()):
        self.broker = msgbroker.MsgBroker(broker)
        self.cur_time = start.timestamp()
        self.end = start.timestamp() + duration
        self.step = step
        random.seed(seed)

    def run(self):
        """ Runs the meter simulation  
        """

        while self.cur_time < self.end:
            # The measurement is sent in the JSON format
            # with the timestamp as the key of the generated meter value
            msg = {self.cur_time: random.uniform(0.0, 9000.0)}
            message = json.dumps(msg)
            self.broker.publish('meter', message)
            self.cur_time += self.step
        self.broker.publish('meter', "finish")
        self.stop()

    def stop(self):
        """ Closes the connection with the broker
        """
        self.broker.close()
