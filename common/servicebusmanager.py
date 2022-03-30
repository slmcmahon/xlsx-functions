import os
import json

from azure.servicebus import ServiceBusClient, ServiceBusMessage


class ServiceBusManager:
    def __init__(self, conn_string, queue_name):
        self.queue_name = queue_name
        self.sbc = ServiceBusClient.from_connection_string(conn_string)

    def enqueue(self, message):
        sbmessage = ServiceBusMessage(json.dumps(message))
        sender = self.sbc.get_queue_sender(queue_name=self.queue_name)
        sender.send_messages([sbmessage])
