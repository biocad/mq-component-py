from mq.protocol.types import JSON
import msgpack
from json import loads


class MQError(JSON):
    def __init__(self, code : int = None, message : str = None):
        self.code = code
        self.message = message

    def unpack(self, packed_data):
        self.code = loads(packed_data.decode('UTF-8'))['code']
        self.message = loads(packed_data.decode('UTF-8'))['message']

# Error codes

# PROTOL ERROR: 1xx
########################################

error_protocol : int = 100

error_encoding : int = 101

########################################
# TRANSPORT ERROR: 2xx
########################################

error_transport : int = 200

error_tag : int = 201

########################################
# TECHNICAL ERROR: 3xx
########################################

error_technical : int = 300

error_killed : int = 301

########################################
# COMPONENT ERROR: 5xx
########################################

error_component : int = 500

error_foreign : int = 501
