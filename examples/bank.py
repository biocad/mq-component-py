from mq.component import Component
from mq.component.communication import all_topics
from mq.protocol import message_type, message_spec, message_pid, create_message, never_expires
from json import dumps, loads
from bank_messages import BankRequest, BankResponse
from calculator_messages import CalcRequest, CalcResponse

class Bank(Component):
    """
    Simple component example.
    It receives a config message with JSON-encoded data which contains monthly income and period length in month.
    Using calculator_py component it calculates total income and sends it back.
    Monitoring message variable is updated here as an example.
    """

    def run(self, sched_out, contr_out, sched_in, state_message):

        # subscribe to receive messages
        self.subscribe_type_spec(sched_out, 'config', 'example_bank')

        while True:
            tag, msg = sched_out.recv_multipart()
            if message_type(tag) == 'config' and message_spec(tag) == 'example_bank':
                self.approve_tag(tag)
                state_message.value = 'received message from %s' % msg.id
                req = BankRequest()
                req.unpack(msg.data)
                
                calculator_json = CalcRequest(req.months, req.per_month, '*') 
                calculator_msg = create_message(msg.id, self.get_config().creator, never_expires, 'example_calculator', 'JSON', 'config', calculator_json.pack())

                # do not forget to subscribe to get resulting message
                self.subscribe_type_spec(sched_out, 'result', 'example_calculator')
                self.subscribe_type_spec(sched_out, 'error', 'example_calculator')

                sched_in.send(calculator_msg)
                while True:
                    response_tag, response = sched_out.recv_multipart()
                    if message_type(response_tag) == 'result' and message_spec(response_tag) == 'example_calculator' and message_pid(response_tag) == calculator_msg.id:
                        # do not forget to unsubscribe after successful receiving
                        self.unsubscribe_type_spec(sched_out, 'result', 'example_calculator')
                        self.unsubscribe_type_spec(sched_out, 'error', 'example_calculator')
                        calculator_result = CalcResponse()
                        calculator_result.unpack(response.data)
                        state_message.value = 'Result sent back to %s' % msg.id

                        bank_res = BankResponse(calculator_result.answer)
                        answer = create_message(msg.id, self.get_config().creator, never_expires, 'example_bank', 'JSON', 'result', bank_res.pack())
                        sched_in.send(answer)
                        break
            else:
                print("not my message :(: %s" % tag)

if __name__ == "__main__":
    comp = Bank("example_bank-py")
