import msgpack
import zmq

from mq.protocol import Message, message_tag, create_message, never_expires


def default_error_handler(error_recv, logger, config, shared_message, task_id):
    """
    Error handler.
    Receives error messages via Pipe and sends a MQ error.
    """
    context = zmq.Context()

    to_scheduler = context.socket(zmq.PUSH)
    to_scheduler.connect("tcp://" + config.scheduler_in['host'] + ':' + str(config.scheduler_in['comport']))

    while True:
        error = error_recv.recv()
        try:
            message = create_message(task_id.value.encode('UTF-8'), config.creator, never_expires, 'error', 'JSON', 'error', error.pack())

            tag = message_tag(message)
            packed_message = message.pack()
            to_scheduler.send_multipart([tag, packed_message])
        except Exception as e:
            print("Error handler :: %s" % format(e))

