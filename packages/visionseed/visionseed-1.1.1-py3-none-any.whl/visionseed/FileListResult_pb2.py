# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: FileListResult.proto

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
  name='FileListResult.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x14\x46ileListResult.proto\"8\n\x08\x46ileInfo\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x10\n\x08isFolder\x18\x02 \x02(\x08\x12\x0c\n\x04size\x18\x03 \x02(\x05\"I\n\x0e\x46ileListResult\x12\x0e\n\x06\x66older\x18\x01 \x02(\t\x12\r\n\x05total\x18\x02 \x02(\x05\x12\x18\n\x05\x66iles\x18\x03 \x03(\x0b\x32\t.FileInfo')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_FILEINFO = _descriptor.Descriptor(
  name='FileInfo',
  full_name='FileInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='FileInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isFolder', full_name='FileInfo.isFolder', index=1,
      number=2, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='size', full_name='FileInfo.size', index=2,
      number=3, type=5, cpp_type=1, label=2,
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
  serialized_start=24,
  serialized_end=80,
)


_FILELISTRESULT = _descriptor.Descriptor(
  name='FileListResult',
  full_name='FileListResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='folder', full_name='FileListResult.folder', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total', full_name='FileListResult.total', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='files', full_name='FileListResult.files', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=82,
  serialized_end=155,
)

_FILELISTRESULT.fields_by_name['files'].message_type = _FILEINFO
DESCRIPTOR.message_types_by_name['FileInfo'] = _FILEINFO
DESCRIPTOR.message_types_by_name['FileListResult'] = _FILELISTRESULT

FileInfo = _reflection.GeneratedProtocolMessageType('FileInfo', (_message.Message,), dict(
  DESCRIPTOR = _FILEINFO,
  __module__ = 'FileListResult_pb2'
  # @@protoc_insertion_point(class_scope:FileInfo)
  ))
_sym_db.RegisterMessage(FileInfo)

FileListResult = _reflection.GeneratedProtocolMessageType('FileListResult', (_message.Message,), dict(
  DESCRIPTOR = _FILELISTRESULT,
  __module__ = 'FileListResult_pb2'
  # @@protoc_insertion_point(class_scope:FileListResult)
  ))
_sym_db.RegisterMessage(FileListResult)


# @@protoc_insertion_point(module_scope)
