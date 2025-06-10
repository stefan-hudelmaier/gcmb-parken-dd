class MockMqttPublisher:
    def __init__(self):
        self.messages = []  # List of (payload, topic, retain)
    def send_msg(self, payload, topic, retain=False):
        self.messages.append({'payload': payload, 'topic': topic, 'retain': retain})
    def get_messages_by_topic(self, topic):
        return [m for m in self.messages if m['topic'] == topic]
    def get_payloads_by_topic(self, topic):
        return [m['payload'] for m in self.get_messages_by_topic(topic)]
    def get_all_topics(self):
        return [m['topic'] for m in self.messages]
    def get_all_messages(self):
        return list(self.messages)

