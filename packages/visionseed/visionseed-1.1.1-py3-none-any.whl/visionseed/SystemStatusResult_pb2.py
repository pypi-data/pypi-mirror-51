# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SystemStatusResult.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='SystemStatusResult.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x18SystemStatusResult.proto\"i\n\x12SystemStatusResult\x12\x13\n\x0bheartBeatId\x18\x01 \x02(\x05\x12\x18\n\x0ctemperatures\x18\x02 \x03(\x02\x42\x02\x10\x01\x12\x12\n\x06powers\x18\x03 \x03(\x02\x42\x02\x10\x01\x12\x10\n\x08\x66reeHeap\x18\x04 \x02(\x05')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_SYSTEMSTATUSRESULT = _descriptor.Descriptor(
  name='SystemStatusResult',
  full_name='SystemStatusResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='heartBeatId', full_name='SystemStatusResult.heartBeatId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='temperatures', full_name='SystemStatusResult.temperatures', index=1,
      number=2, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='powers', full_name='SystemStatusResult.powers', index=2,
      number=3, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='freeHeap', full_name='SystemStatusResult.freeHeap', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=133,
)

DESCRIPTOR.message_types_by_name['SystemStatusResult'] = _SYSTEMSTATUSRESULT

SystemStatusResult = _reflection.GeneratedProtocolMessageType('SystemStatusResult', (_message.Message,), dict(
  DESCRIPTOR = _SYSTEMSTATUSRESULT,
  __module__ = 'SystemStatusResult_pb2'
  # @@protoc_insertion_point(class_scope:SystemStatusResult)
  ))
_sym_db.RegisterMessage(SystemStatusResult)


_SYSTEMSTATUSRESULT.fields_by_name['temperatures'].has_options = True
_SYSTEMSTATUSRESULT.fields_by_name['temperatures']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_SYSTEMSTATUSRESULT.fields_by_name['powers'].has_options = True
_SYSTEMSTATUSRESULT.fields_by_name['powers']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)
