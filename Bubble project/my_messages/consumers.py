import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        recipient = text_data_json['recipient']

        # Save the message in the database
        message_instance = Message(sender=sender, recipient=recipient, content=message)
        message_instance.save()

        # Broadcast the message to everyone in the room
        self.send(text_data=json.dumps({'message': message}))
