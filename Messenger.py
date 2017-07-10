import json

class Messenger:
    """
    Messenger is a wrapper for either a Message or SlackClient instance.
    """
    def __init__(self, service, channel=None):
        self.service = service
        self.service_type = type(service).__name__
        self.channel = channel

    def reply(self, message):
        if self.service_type == "Message":
            self.service.reply(message)
        else:
            self.service.send_message(self.channel, message)

    def send(self, message):
        if self.service_type == "Message":
            self.service.send(message)
        else:
            self.service.send_message(self.channel, message)

    def send_attachments(self, attachments):
        if self.service_type == "Message":
            self.service.send_webapi('', json.dumps(attachments))
        else:
            self.service.send_message(self.channel, '', json.dumps(attachments))

    def full_name(self):
        if self.service_type == "Message":
            return self.service.channel._client.users[self.service.body['user']][u'real_name']
        else:
            return "*Unknown Person*" # Or should I throw an error?

    def sender_id(self):
        if self.service_type == "Message":
            return self.service.channel._client.users[self.service.body['user']]['id']
        else:
            return 0 # Or should I throw an error?
