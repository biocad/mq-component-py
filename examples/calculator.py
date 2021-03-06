from mq.component import Component
from mq.protocol import message_type, message_spec, create_message, never_expires, MQError, error_component
from json import loads
from calculator_messages import CalcRequest, CalcResponse

class Calculator(Component):
    """
    Simple component example.
    It receives a config message with JSON-encoded data which contains two operands and action and sends back the result.
    write_log function is used here as an example.
    """

    def run(self, sched_out, contr_out, sched_in, state_message):
        # this is way to get full config file
        print(self._config.full_config)

        self.subscribe_type_spec(sched_out, 'config', 'example_calculator')
        
        while True:
            tag, msg = sched_out.recv_multipart()
            if message_type(tag) == 'config' and message_spec(tag) == 'example_calculator':
                self.approve_tag(tag)
                self.logger.write_log('received message from %s' % msg.id)
                req = CalcRequest()
                req.unpack(msg.data)

                res = None
                print('Somebody wants to find out how much will be %s %s %s.' % (req.first, req.action, req.second))
                if req.action == '+':
                    res = req.first + req.second
                elif req.action == '*':
                    res = req.first * req.second
                if res is None:
                    self.logger.write_log('Unknown action received from %s' % msg.id, log_type = 'warning')
                    answer = create_message(msg.id, self.get_config().creator, never_expires, 'example_calculator', 'JSON', 'error', MQError(error_component, "unknown action %s" % req.action).pack())
                else:
                    self.logger.write_log('Result sent back to %s' % msg.id)
                    answer = create_message(msg.id, self.get_config().creator, never_expires, 'example_calculator', 'JSON', 'result', CalcResponse(res).pack())
                sched_in.send(answer)


if __name__ == "__main__":
    comp = Calculator("example_calculator-py")
