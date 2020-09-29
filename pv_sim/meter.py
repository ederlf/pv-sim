# SPDX-License-Identifier: BSD-3-Clause

import json
import datetime
import random
import msgbroker


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
