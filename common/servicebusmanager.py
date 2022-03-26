import os
import json

from azure.servicebus import ServiceBusClient, ServiceBusMessage


class ServiceBusManager:
    def __init__(self):
        self.queue_name = os.environ["ServiceBusQueueName"]
        self.sbc = ServiceBusClient.from_connection_string(
            os.environ["ServiceBusConnectionString"])

    def enqueue(self, message):
        sbmessage = ServiceBusMessage(json.dumps(message))
        sender = self.sbc.get_queue_sender(queue_name=self.queue_name)
        sender.send_messages([sbmessage])
