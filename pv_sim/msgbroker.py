# SPDX-License-Identifier: BSD-3-Clause

import pika


class MsgBroker(object):
    """ Interface of message brokers.

    :param: The object of a message broker that implements the functionality 
    of the interface
    """

    def __init__(self, broker):
        self.broker = broker

    def subscribe(self, queue, action=None):
        """ Listens and receives messages from a message broker queue

        :param queue: The identification/name of the queue
        :type queue: str
        :param action: an optional callback that might be required from a broker API.
        """
        if action:
            self.broker.subscribe(queue, action)
        else:
            self.broker.subscribe(queue)

    def publish(self, queue, message):
        self.broker.publish(queue, message)

    def close(self):
        self.broker.close()


class RabbitMQBroker:
    """ This class is a possible implementation of a MsgBroker. A MsgBroker
    class that receives this class can send and receive messages from 
    rabbitmq queues

    :param host: The IP address of the machine running rabbitmq, 
        Defaults to localhost
        :type host: str
        :param port: The TCP port that rabbitmq listens. The default is the same port as rabbitmq listens by default
    """

    default_host = "localhost"
    default_port = 5672

    def __init__(self, host=None, port=None):
        if not host:
            host = self.default_host
        if not port:
            port = self.default_port

        self.conn = self._create_connection(host, port)
        self.channel = self.conn.channel()
        self.queue = None

    def _create_connection(self, host, port):
        """  Creates a new connection with an instance of rabbitmq

        :param host: The IP address of the machine running rabbitmq, 
        Defaults to localhost
        :type host: str
        :param port: The TCP port that rabbitmq listens. The default is the same port as rabbitmq listens by default
        """
        return pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                                 port=port))

    def subscribe(self, queue, action):
        """ Subscribes and receives messages from a rabbitmq queue

        :param queue: The identification/name of the queue
        :type queue: str
        :param action: This is a callback function, required by rabbitmq to perform an action on received messages
        """
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue=queue,
                                   on_message_callback=action,
                                   auto_ack=True)
        self.channel.start_consuming()

    def publish(self, queue, message):
        """ Sends a message to a rabbitmq queue

        :param queue: The identification/name of the queue
        :type queue: str
        :param message: The message to be sent
        :type message: str
        """

        # Instead of passing a queue to the constructor, the publish checks if
        # the target queue exists. If not, it declares the target queue
        if not self.queue:
            self.channel.queue_declare(queue=queue)
            self.queue = queue

        self.channel.basic_publish(
            exchange='', routing_key=queue, body=message)

    def close(self):
        """ Closes the connection with rabbitmq
        """
        self.conn.close()


def broker_factory(broker_name, ip=None, port=None):
    """ Creates a broker object according to its name. Supports only rabbitmq
    for now
    :param broker_name: the name of a supported broker
    :type broker_namae: str
    :param ip: the IP address where the broker is running. If None, the 
    created class will use localhost
    :type ip: str
    :param port: The TCP port to connect to the broker. If not set, it will use the broker's default port
    :type port: int
    """
    if broker_name == "rabbitmq":
        return RabbitMQBroker(ip, port)
