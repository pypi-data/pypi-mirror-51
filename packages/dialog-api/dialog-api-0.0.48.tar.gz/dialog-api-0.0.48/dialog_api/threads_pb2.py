# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: threads.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from . import definitions_pb2 as definitions__pb2
from . import miscellaneous_pb2 as miscellaneous__pb2
from .scalapb import scalapb_pb2 as scalapb_dot_scalapb__pb2
from . import users_pb2 as users__pb2
from . import peers_pb2 as peers__pb2
from . import groups_pb2 as groups__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='threads.proto',
  package='dialog',
  syntax='proto3',
  serialized_options=_b('\342?\026\n\024im.dlg.grpc.services'),
  serialized_pb=_b('\n\rthreads.proto\x12\x06\x64ialog\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x11\x64\x65\x66initions.proto\x1a\x13miscellaneous.proto\x1a\x15scalapb/scalapb.proto\x1a\x0busers.proto\x1a\x0bpeers.proto\x1a\x0cgroups.proto\"u\n\x0fThreadReference\x12\x34\n\nmessage_id\x18\x01 \x01(\x0b\x32\x11.dialog.UUIDValueB\r\x8a\xea\x30\t\n\x07visible\x12,\n\x04peer\x18\x02 \x01(\x0b\x32\x0f.dialog.OutPeerB\r\x8a\xea\x30\t\n\x07visible\"\x85\x03\n\x13RequestCreateThread\x12 \n\trandom_id\x18\x01 \x01(\x03\x42\r\x8a\xea\x30\t\n\x07visible\x12>\n\x11parent_group_peer\x18\x02 \x01(\x0b\x32\x14.dialog.GroupOutPeerB\r\x8a\xea\x30\t\n\x07visible\x12:\n\x10start_message_id\x18\x03 \x01(\x0b\x32\x11.dialog.UUIDValueB\r\x8a\xea\x30\t\n\x07visible\x12\r\n\x05title\x18\x04 \x01(\t\x12;\n\x0bjoin_policy\x18\x05 \x01(\x0e\x32&.dialog.RequestCreateThread.JoinPolicy\x12\x33\n\x07members\x18\x06 \x03(\x0b\x32\x13.dialog.UserOutPeerB\r\x8a\xea\x30\t\n\x07visible\"1\n\nJoinPolicy\x12\x0f\n\x0bINVITE_ONLY\x10\x00\x12\x12\n\x0eTHREAD_MEMBERS\x10\x01:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"\xa0\x01\n\x14ResponseCreateThread\x12#\n\x0cthread_group\x18\x01 \x01(\x0b\x32\r.dialog.Group\x12\x1b\n\x05users\x18\x02 \x03(\x0b\x32\x0c.dialog.User\x12\'\n\nuser_peers\x18\x03 \x03(\x0b\x32\x13.dialog.UserOutPeer:\x1d\xe2?\x1a\n\x18im.dlg.grpc.GrpcResponse\"\x80\x02\n\x11RequestLiftThread\x12 \n\trandom_id\x18\x01 \x01(\x03\x42\r\x8a\xea\x30\t\n\x07visible\x12>\n\x11parent_group_peer\x18\x02 \x01(\x0b\x32\x14.dialog.GroupOutPeerB\r\x8a\xea\x30\t\n\x07visible\x12>\n\x11thread_group_peer\x18\x03 \x01(\x0b\x32\x14.dialog.GroupOutPeerB\r\x8a\xea\x30\t\n\x07visible\x12+\n\x05title\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValue:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"u\n\x12ResponseLiftThread\x12\x1c\n\x05group\x18\x01 \x01(\x0b\x32\r.dialog.Group\x12\"\n\x04peer\x18\x02 \x01(\x0b\x32\x14.dialog.GroupOutPeer:\x1d\xe2?\x1a\n\x18im.dlg.grpc.GrpcResponse\"k\n\x17RequestLoadGroupThreads\x12\x32\n\x05group\x18\x01 \x01(\x0b\x32\x14.dialog.GroupOutPeerB\r\x8a\xea\x30\t\n\x07\x63ompact:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest\"r\n\x18ResponseLoadGroupThreads\x12\x37\n\x07threads\x18\x01 \x03(\x0b\x32\x17.dialog.ThreadReferenceB\r\x8a\xea\x30\t\n\x07visible:\x1d\xe2?\x1a\n\x18im.dlg.grpc.GrpcResponse\"\xb1\x01\n\x11RequestJoinThread\x12>\n\x11parent_group_peer\x18\x02 \x01(\x0b\x32\x14.dialog.GroupOutPeerB\r\x8a\xea\x30\t\n\x07visible\x12>\n\x11thread_group_peer\x18\x03 \x01(\x0b\x32\x14.dialog.GroupOutPeerB\r\x8a\xea\x30\t\n\x07visible:\x1c\xe2?\x19\n\x17im.dlg.grpc.GrpcRequest2\xd8\x03\n\x07Threads\x12s\n\x0c\x43reateThread\x12\x1b.dialog.RequestCreateThread\x1a\x1c.dialog.ResponseCreateThread\"(\x82\xd3\xe4\x93\x02\"\"\x1d/v1/grpc/Threads/CreateThread:\x01*\x12k\n\nLiftThread\x12\x19.dialog.RequestLiftThread\x1a\x1a.dialog.ResponseLiftThread\"&\x82\xd3\xe4\x93\x02 \"\x1b/v1/grpc/Threads/LiftThread:\x01*\x12\x83\x01\n\x10LoadGroupThreads\x12\x1f.dialog.RequestLoadGroupThreads\x1a .dialog.ResponseLoadGroupThreads\",\x82\xd3\xe4\x93\x02&\"!/v1/grpc/Threads/LoadGroupThreads:\x01*\x12\x65\n\nJoinThread\x12\x19.dialog.RequestJoinThread\x1a\x14.dialog.ResponseVoid\"&\x82\xd3\xe4\x93\x02 \"\x1b/v1/grpc/Threads/JoinThread:\x01*B\x19\xe2?\x16\n\x14im.dlg.grpc.servicesb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,definitions__pb2.DESCRIPTOR,miscellaneous__pb2.DESCRIPTOR,scalapb_dot_scalapb__pb2.DESCRIPTOR,users__pb2.DESCRIPTOR,peers__pb2.DESCRIPTOR,groups__pb2.DESCRIPTOR,])



_REQUESTCREATETHREAD_JOINPOLICY = _descriptor.EnumDescriptor(
  name='JoinPolicy',
  full_name='dialog.RequestCreateThread.JoinPolicy',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INVITE_ONLY', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='THREAD_MEMBERS', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=620,
  serialized_end=669,
)
_sym_db.RegisterEnumDescriptor(_REQUESTCREATETHREAD_JOINPOLICY)


_THREADREFERENCE = _descriptor.Descriptor(
  name='ThreadReference',
  full_name='dialog.ThreadReference',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message_id', full_name='dialog.ThreadReference.message_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='peer', full_name='dialog.ThreadReference.peer', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=307,
)


_REQUESTCREATETHREAD = _descriptor.Descriptor(
  name='RequestCreateThread',
  full_name='dialog.RequestCreateThread',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='random_id', full_name='dialog.RequestCreateThread.random_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent_group_peer', full_name='dialog.RequestCreateThread.parent_group_peer', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start_message_id', full_name='dialog.RequestCreateThread.start_message_id', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='title', full_name='dialog.RequestCreateThread.title', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='join_policy', full_name='dialog.RequestCreateThread.join_policy', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='members', full_name='dialog.RequestCreateThread.members', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REQUESTCREATETHREAD_JOINPOLICY,
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=310,
  serialized_end=699,
)


_RESPONSECREATETHREAD = _descriptor.Descriptor(
  name='ResponseCreateThread',
  full_name='dialog.ResponseCreateThread',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='thread_group', full_name='dialog.ResponseCreateThread.thread_group', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='users', full_name='dialog.ResponseCreateThread.users', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_peers', full_name='dialog.ResponseCreateThread.user_peers', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\032\n\030im.dlg.grpc.GrpcResponse'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=702,
  serialized_end=862,
)


_REQUESTLIFTTHREAD = _descriptor.Descriptor(
  name='RequestLiftThread',
  full_name='dialog.RequestLiftThread',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='random_id', full_name='dialog.RequestLiftThread.random_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent_group_peer', full_name='dialog.RequestLiftThread.parent_group_peer', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='thread_group_peer', full_name='dialog.RequestLiftThread.thread_group_peer', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='title', full_name='dialog.RequestLiftThread.title', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=865,
  serialized_end=1121,
)


_RESPONSELIFTTHREAD = _descriptor.Descriptor(
  name='ResponseLiftThread',
  full_name='dialog.ResponseLiftThread',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='group', full_name='dialog.ResponseLiftThread.group', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='peer', full_name='dialog.ResponseLiftThread.peer', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\032\n\030im.dlg.grpc.GrpcResponse'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1123,
  serialized_end=1240,
)


_REQUESTLOADGROUPTHREADS = _descriptor.Descriptor(
  name='RequestLoadGroupThreads',
  full_name='dialog.RequestLoadGroupThreads',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='group', full_name='dialog.RequestLoadGroupThreads.group', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007compact'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1242,
  serialized_end=1349,
)


_RESPONSELOADGROUPTHREADS = _descriptor.Descriptor(
  name='ResponseLoadGroupThreads',
  full_name='dialog.ResponseLoadGroupThreads',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='threads', full_name='dialog.ResponseLoadGroupThreads.threads', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\032\n\030im.dlg.grpc.GrpcResponse'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1351,
  serialized_end=1465,
)


_REQUESTJOINTHREAD = _descriptor.Descriptor(
  name='RequestJoinThread',
  full_name='dialog.RequestJoinThread',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parent_group_peer', full_name='dialog.RequestJoinThread.parent_group_peer', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='thread_group_peer', full_name='dialog.RequestJoinThread.thread_group_peer', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\3520\t\n\007visible'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\342?\031\n\027im.dlg.grpc.GrpcRequest'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1468,
  serialized_end=1645,
)

_THREADREFERENCE.fields_by_name['message_id'].message_type = definitions__pb2._UUIDVALUE
_THREADREFERENCE.fields_by_name['peer'].message_type = peers__pb2._OUTPEER
_REQUESTCREATETHREAD.fields_by_name['parent_group_peer'].message_type = peers__pb2._GROUPOUTPEER
_REQUESTCREATETHREAD.fields_by_name['start_message_id'].message_type = definitions__pb2._UUIDVALUE
_REQUESTCREATETHREAD.fields_by_name['join_policy'].enum_type = _REQUESTCREATETHREAD_JOINPOLICY
_REQUESTCREATETHREAD.fields_by_name['members'].message_type = peers__pb2._USEROUTPEER
_REQUESTCREATETHREAD_JOINPOLICY.containing_type = _REQUESTCREATETHREAD
_RESPONSECREATETHREAD.fields_by_name['thread_group'].message_type = groups__pb2._GROUP
_RESPONSECREATETHREAD.fields_by_name['users'].message_type = users__pb2._USER
_RESPONSECREATETHREAD.fields_by_name['user_peers'].message_type = peers__pb2._USEROUTPEER
_REQUESTLIFTTHREAD.fields_by_name['parent_group_peer'].message_type = peers__pb2._GROUPOUTPEER
_REQUESTLIFTTHREAD.fields_by_name['thread_group_peer'].message_type = peers__pb2._GROUPOUTPEER
_REQUESTLIFTTHREAD.fields_by_name['title'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_RESPONSELIFTTHREAD.fields_by_name['group'].message_type = groups__pb2._GROUP
_RESPONSELIFTTHREAD.fields_by_name['peer'].message_type = peers__pb2._GROUPOUTPEER
_REQUESTLOADGROUPTHREADS.fields_by_name['group'].message_type = peers__pb2._GROUPOUTPEER
_RESPONSELOADGROUPTHREADS.fields_by_name['threads'].message_type = _THREADREFERENCE
_REQUESTJOINTHREAD.fields_by_name['parent_group_peer'].message_type = peers__pb2._GROUPOUTPEER
_REQUESTJOINTHREAD.fields_by_name['thread_group_peer'].message_type = peers__pb2._GROUPOUTPEER
DESCRIPTOR.message_types_by_name['ThreadReference'] = _THREADREFERENCE
DESCRIPTOR.message_types_by_name['RequestCreateThread'] = _REQUESTCREATETHREAD
DESCRIPTOR.message_types_by_name['ResponseCreateThread'] = _RESPONSECREATETHREAD
DESCRIPTOR.message_types_by_name['RequestLiftThread'] = _REQUESTLIFTTHREAD
DESCRIPTOR.message_types_by_name['ResponseLiftThread'] = _RESPONSELIFTTHREAD
DESCRIPTOR.message_types_by_name['RequestLoadGroupThreads'] = _REQUESTLOADGROUPTHREADS
DESCRIPTOR.message_types_by_name['ResponseLoadGroupThreads'] = _RESPONSELOADGROUPTHREADS
DESCRIPTOR.message_types_by_name['RequestJoinThread'] = _REQUESTJOINTHREAD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ThreadReference = _reflection.GeneratedProtocolMessageType('ThreadReference', (_message.Message,), {
  'DESCRIPTOR' : _THREADREFERENCE,
  '__module__' : 'threads_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ThreadReference)
  })
_sym_db.RegisterMessage(ThreadReference)

RequestCreateThread = _reflection.GeneratedProtocolMessageType('RequestCreateThread', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTCREATETHREAD,
  '__module__' : 'threads_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestCreateThread)
  })
_sym_db.RegisterMessage(RequestCreateThread)

ResponseCreateThread = _reflection.GeneratedProtocolMessageType('ResponseCreateThread', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSECREATETHREAD,
  '__module__' : 'threads_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ResponseCreateThread)
  })
_sym_db.RegisterMessage(ResponseCreateThread)

RequestLiftThread = _reflection.GeneratedProtocolMessageType('RequestLiftThread', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTLIFTTHREAD,
  '__module__' : 'threads_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestLiftThread)
  })
_sym_db.RegisterMessage(RequestLiftThread)

ResponseLiftThread = _reflection.GeneratedProtocolMessageType('ResponseLiftThread', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSELIFTTHREAD,
  '__module__' : 'threads_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ResponseLiftThread)
  })
_sym_db.RegisterMessage(ResponseLiftThread)

RequestLoadGroupThreads = _reflection.GeneratedProtocolMessageType('RequestLoadGroupThreads', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTLOADGROUPTHREADS,
  '__module__' : 'threads_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestLoadGroupThreads)
  })
_sym_db.RegisterMessage(RequestLoadGroupThreads)

ResponseLoadGroupThreads = _reflection.GeneratedProtocolMessageType('ResponseLoadGroupThreads', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSELOADGROUPTHREADS,
  '__module__' : 'threads_pb2'
  # @@protoc_insertion_point(class_scope:dialog.ResponseLoadGroupThreads)
  })
_sym_db.RegisterMessage(ResponseLoadGroupThreads)

RequestJoinThread = _reflection.GeneratedProtocolMessageType('RequestJoinThread', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTJOINTHREAD,
  '__module__' : 'threads_pb2'
  # @@protoc_insertion_point(class_scope:dialog.RequestJoinThread)
  })
_sym_db.RegisterMessage(RequestJoinThread)


DESCRIPTOR._options = None
_THREADREFERENCE.fields_by_name['message_id']._options = None
_THREADREFERENCE.fields_by_name['peer']._options = None
_REQUESTCREATETHREAD.fields_by_name['random_id']._options = None
_REQUESTCREATETHREAD.fields_by_name['parent_group_peer']._options = None
_REQUESTCREATETHREAD.fields_by_name['start_message_id']._options = None
_REQUESTCREATETHREAD.fields_by_name['members']._options = None
_REQUESTCREATETHREAD._options = None
_RESPONSECREATETHREAD._options = None
_REQUESTLIFTTHREAD.fields_by_name['random_id']._options = None
_REQUESTLIFTTHREAD.fields_by_name['parent_group_peer']._options = None
_REQUESTLIFTTHREAD.fields_by_name['thread_group_peer']._options = None
_REQUESTLIFTTHREAD._options = None
_RESPONSELIFTTHREAD._options = None
_REQUESTLOADGROUPTHREADS.fields_by_name['group']._options = None
_REQUESTLOADGROUPTHREADS._options = None
_RESPONSELOADGROUPTHREADS.fields_by_name['threads']._options = None
_RESPONSELOADGROUPTHREADS._options = None
_REQUESTJOINTHREAD.fields_by_name['parent_group_peer']._options = None
_REQUESTJOINTHREAD.fields_by_name['thread_group_peer']._options = None
_REQUESTJOINTHREAD._options = None

_THREADS = _descriptor.ServiceDescriptor(
  name='Threads',
  full_name='dialog.Threads',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1648,
  serialized_end=2120,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateThread',
    full_name='dialog.Threads.CreateThread',
    index=0,
    containing_service=None,
    input_type=_REQUESTCREATETHREAD,
    output_type=_RESPONSECREATETHREAD,
    serialized_options=_b('\202\323\344\223\002\"\"\035/v1/grpc/Threads/CreateThread:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='LiftThread',
    full_name='dialog.Threads.LiftThread',
    index=1,
    containing_service=None,
    input_type=_REQUESTLIFTTHREAD,
    output_type=_RESPONSELIFTTHREAD,
    serialized_options=_b('\202\323\344\223\002 \"\033/v1/grpc/Threads/LiftThread:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='LoadGroupThreads',
    full_name='dialog.Threads.LoadGroupThreads',
    index=2,
    containing_service=None,
    input_type=_REQUESTLOADGROUPTHREADS,
    output_type=_RESPONSELOADGROUPTHREADS,
    serialized_options=_b('\202\323\344\223\002&\"!/v1/grpc/Threads/LoadGroupThreads:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='JoinThread',
    full_name='dialog.Threads.JoinThread',
    index=3,
    containing_service=None,
    input_type=_REQUESTJOINTHREAD,
    output_type=miscellaneous__pb2._RESPONSEVOID,
    serialized_options=_b('\202\323\344\223\002 \"\033/v1/grpc/Threads/JoinThread:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_THREADS)

DESCRIPTOR.services_by_name['Threads'] = _THREADS

# @@protoc_insertion_point(module_scope)
