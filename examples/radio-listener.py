from mq.component import Component
from mq.component.communication import all_topics
from mq.protocol import message_type, message_spec


class RadioListener(Component):
    """
    Simple component example.
    In an infinite loop it receives message from the scheduler, prints its data and sets status variable.
    """
    def run(self, sched_out, contr_out, sched_in, state_message):
        # In this place we subscribe to all messages with type `data` and spec `example_radio`.
        # If component interested in all topics, uncomment this line:
        # self.subscribe(sched_out, all_topics)
        self.subscribe_type_spec(sched_out, 'data', 'example_radio')
        while True:
            tag, msg = sched_out.recv_multipart()

            if message_type(tag) == 'data' and message_spec(tag) == 'example_radio':
                self.approve_tag(tag)
                print(msg.data)
                state_message.value = "Processed message from %s" % msg.creator


if __name__ == "__main__":
    comp = RadioListener("example_radio-listener-py")
