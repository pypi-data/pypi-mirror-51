# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/plugins/profile/trace_events.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorboard/plugins/profile/trace_events.proto',
  package='tensorboard.profile',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n.tensorboard/plugins/profile/trace_events.proto\x12\x13tensorboard.profile\"\xc5\x01\n\x05Trace\x12\x38\n\x07\x64\x65vices\x18\x01 \x03(\x0b\x32\'.tensorboard.profile.Trace.DevicesEntry\x12\x35\n\x0ctrace_events\x18\x04 \x03(\x0b\x32\x1f.tensorboard.profile.TraceEvent\x1aK\n\x0c\x44\x65vicesEntry\x12\x0b\n\x03key\x18\x01 \x01(\x04\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x1b.tensorboard.profile.Device:\x02\x38\x01\"\xb9\x01\n\x06\x44\x65vice\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tdevice_id\x18\x02 \x01(\x04\x12=\n\tresources\x18\x03 \x03(\x0b\x32*.tensorboard.profile.Device.ResourcesEntry\x1aO\n\x0eResourcesEntry\x12\x0b\n\x03key\x18\x01 \x01(\x04\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x1d.tensorboard.profile.Resource:\x02\x38\x01\"-\n\x08Resource\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bresource_id\x18\x02 \x01(\x04\"\xd3\x01\n\nTraceEvent\x12\x11\n\tdevice_id\x18\x01 \x01(\x04\x12\x13\n\x0bresource_id\x18\x02 \x01(\x04\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x14\n\x0ctimestamp_ps\x18\t \x01(\x04\x12\x13\n\x0b\x64uration_ps\x18\n \x01(\x04\x12\x37\n\x04\x61rgs\x18\x0b \x03(\x0b\x32).tensorboard.profile.TraceEvent.ArgsEntry\x1a+\n\tArgsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')
)




_TRACE_DEVICESENTRY = _descriptor.Descriptor(
  name='DevicesEntry',
  full_name='tensorboard.profile.Trace.DevicesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tensorboard.profile.Trace.DevicesEntry.key', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tensorboard.profile.Trace.DevicesEntry.value', index=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=269,
)

_TRACE = _descriptor.Descriptor(
  name='Trace',
  full_name='tensorboard.profile.Trace',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='devices', full_name='tensorboard.profile.Trace.devices', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trace_events', full_name='tensorboard.profile.Trace.trace_events', index=1,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TRACE_DEVICESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=72,
  serialized_end=269,
)


_DEVICE_RESOURCESENTRY = _descriptor.Descriptor(
  name='ResourcesEntry',
  full_name='tensorboard.profile.Device.ResourcesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tensorboard.profile.Device.ResourcesEntry.key', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tensorboard.profile.Device.ResourcesEntry.value', index=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=378,
  serialized_end=457,
)

_DEVICE = _descriptor.Descriptor(
  name='Device',
  full_name='tensorboard.profile.Device',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorboard.profile.Device.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_id', full_name='tensorboard.profile.Device.device_id', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resources', full_name='tensorboard.profile.Device.resources', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DEVICE_RESOURCESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=272,
  serialized_end=457,
)


_RESOURCE = _descriptor.Descriptor(
  name='Resource',
  full_name='tensorboard.profile.Resource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorboard.profile.Resource.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='tensorboard.profile.Resource.resource_id', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=459,
  serialized_end=504,
)


_TRACEEVENT_ARGSENTRY = _descriptor.Descriptor(
  name='ArgsEntry',
  full_name='tensorboard.profile.TraceEvent.ArgsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tensorboard.profile.TraceEvent.ArgsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tensorboard.profile.TraceEvent.ArgsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=675,
  serialized_end=718,
)

_TRACEEVENT = _descriptor.Descriptor(
  name='TraceEvent',
  full_name='tensorboard.profile.TraceEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_id', full_name='tensorboard.profile.TraceEvent.device_id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='tensorboard.profile.TraceEvent.resource_id', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorboard.profile.TraceEvent.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_ps', full_name='tensorboard.profile.TraceEvent.timestamp_ps', index=3,
      number=9, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='duration_ps', full_name='tensorboard.profile.TraceEvent.duration_ps', index=4,
      number=10, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='args', full_name='tensorboard.profile.TraceEvent.args', index=5,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TRACEEVENT_ARGSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=507,
  serialized_end=718,
)

_TRACE_DEVICESENTRY.fields_by_name['value'].message_type = _DEVICE
_TRACE_DEVICESENTRY.containing_type = _TRACE
_TRACE.fields_by_name['devices'].message_type = _TRACE_DEVICESENTRY
_TRACE.fields_by_name['trace_events'].message_type = _TRACEEVENT
_DEVICE_RESOURCESENTRY.fields_by_name['value'].message_type = _RESOURCE
_DEVICE_RESOURCESENTRY.containing_type = _DEVICE
_DEVICE.fields_by_name['resources'].message_type = _DEVICE_RESOURCESENTRY
_TRACEEVENT_ARGSENTRY.containing_type = _TRACEEVENT
_TRACEEVENT.fields_by_name['args'].message_type = _TRACEEVENT_ARGSENTRY
DESCRIPTOR.message_types_by_name['Trace'] = _TRACE
DESCRIPTOR.message_types_by_name['Device'] = _DEVICE
DESCRIPTOR.message_types_by_name['Resource'] = _RESOURCE
DESCRIPTOR.message_types_by_name['TraceEvent'] = _TRACEEVENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Trace = _reflection.GeneratedProtocolMessageType('Trace', (_message.Message,), dict(

  DevicesEntry = _reflection.GeneratedProtocolMessageType('DevicesEntry', (_message.Message,), dict(
    DESCRIPTOR = _TRACE_DEVICESENTRY,
    __module__ = 'tensorboard.plugins.profile.trace_events_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.profile.Trace.DevicesEntry)
    ))
  ,
  DESCRIPTOR = _TRACE,
  __module__ = 'tensorboard.plugins.profile.trace_events_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.profile.Trace)
  ))
_sym_db.RegisterMessage(Trace)
_sym_db.RegisterMessage(Trace.DevicesEntry)

Device = _reflection.GeneratedProtocolMessageType('Device', (_message.Message,), dict(

  ResourcesEntry = _reflection.GeneratedProtocolMessageType('ResourcesEntry', (_message.Message,), dict(
    DESCRIPTOR = _DEVICE_RESOURCESENTRY,
    __module__ = 'tensorboard.plugins.profile.trace_events_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.profile.Device.ResourcesEntry)
    ))
  ,
  DESCRIPTOR = _DEVICE,
  __module__ = 'tensorboard.plugins.profile.trace_events_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.profile.Device)
  ))
_sym_db.RegisterMessage(Device)
_sym_db.RegisterMessage(Device.ResourcesEntry)

Resource = _reflection.GeneratedProtocolMessageType('Resource', (_message.Message,), dict(
  DESCRIPTOR = _RESOURCE,
  __module__ = 'tensorboard.plugins.profile.trace_events_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.profile.Resource)
  ))
_sym_db.RegisterMessage(Resource)

TraceEvent = _reflection.GeneratedProtocolMessageType('TraceEvent', (_message.Message,), dict(

  ArgsEntry = _reflection.GeneratedProtocolMessageType('ArgsEntry', (_message.Message,), dict(
    DESCRIPTOR = _TRACEEVENT_ARGSENTRY,
    __module__ = 'tensorboard.plugins.profile.trace_events_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.profile.TraceEvent.ArgsEntry)
    ))
  ,
  DESCRIPTOR = _TRACEEVENT,
  __module__ = 'tensorboard.plugins.profile.trace_events_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.profile.TraceEvent)
  ))
_sym_db.RegisterMessage(TraceEvent)
_sym_db.RegisterMessage(TraceEvent.ArgsEntry)


_TRACE_DEVICESENTRY._options = None
_DEVICE_RESOURCESENTRY._options = None
_TRACEEVENT_ARGSENTRY._options = None
# @@protoc_insertion_point(module_scope)
