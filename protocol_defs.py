from re import S
import struct

cmd_def = {
    # VirtualMachine Command Set (1)
    'Version': {
        'sig': (1, 1),
        'cmd': (),
        'reply': (
            ('string', 'description'),
            ('int', 'jdwpMajor'),
            ('int', 'jdwpMinor'),
            ('string', 'vmVersion'),
            ('string', 'vmName'),),

    },
    'ClassesBySignature': {
        'sig': (2, 1),
        'cmd': (),
        'reply': (),

    },
    'AllClasses': {
        'sig': (3, 1),
        'cmd': (),
        'reply': (),

    },
    'AllThreads': {
        'sig': (4, 1),
        'cmd': (),
        'reply': (),

    },
    'TopLevelThreadGroups': {
        'sig': (5, 1),
        'cmd': (),
        'reply': (),

    },
    'Dispose': {
        'sig': (6, 1),
        'cmd': (),
        'reply': (),

    },
    'IDSizes': {
        'sig': (7, 1),
        'cmd': (),
        'reply': (
            ("int", "fieldIDSize"),
            ("int", "methodIDSize"), 
            ("int", "objectIDSize"), 
            ("int", "referenceTypeIDSize"), 
            ("int", "frameIDSize")),
    },
    'Suspend': {
        'sig': (8, 1),
        'cmd': (),
        'reply': (),

    },
    'Resume': {
        'sig': (9, 1),
        'cmd': (),
        'reply': (),

    },
    'Exit': {
        'sig': (10, 1),
        'cmd': (),
        'reply': (),

    },
    'CreateString': {
        'sig': (11, 1),
        'cmd': (),
        'reply': (),

    },
    'Capabilities': {
        'sig': (12, 1),
        'cmd': (),
        'reply': (),

    },
    'ClassPaths': {
        'sig': (13, 1),
        'cmd': (),
        'reply': (),

    },
    'DisposeObjects': {
        'sig': (14, 1),
        'cmd': (),
        'reply': (),

    },
    'HoldEvents': {
        'sig': (15, 1),
        'cmd': (),
        'reply': (),

    },
    'ReleaseEvents': {
        'sig': (16, 1),
        'cmd': (),
        'reply': (),

    },
    'CapabilitiesNew': {
        'sig': (17, 1),
        'cmd': (),
        'reply': (),

    },
    'RedefineClasses': {
        'sig': (18, 1),
        'cmd': (),
        'reply': (),

    },
    'SetDefaultStratum': {
        'sig': (19, 1),
        'cmd': (),
        'reply': (),

    },
    'AllClassesWithGeneric': {
        'sig': (20, 1),
        'cmd': (),
        'reply': (),

    },
    'InstanceCounts': {
        'sig': (21, 1),
        'cmd': (),
        'reply': (),

    },
    # ReferenceType Command Set (2)
    'Signature': {
        'sig': (1, 2),
        'cmd': (),
        'reply': (),

    },
    'ClassLoader': {
        'sig': (2, 2),
        'cmd': (),
        'reply': (),

    },
    'Modifiers': {
        'sig': (3, 2),
        'cmd': (),
        'reply': (),

    },
    'Fields': {
        'sig': (4, 2),
        'cmd': (),
        'reply': (),

    },
    'Methods': {
        'sig': (5, 2),
        'cmd': (),
        'reply': (),

    },
    'GetValues': {
        'sig': (6, 2),
        'cmd': (),
        'reply': (),

    },
    'SourceFile': {
        'sig': (7, 2),
        'cmd': (),
        'reply': (),

    },
    'NestedTypes': {
        'sig': (8, 2),
        'cmd': (),
        'reply': (),

    },
    'Status': {
        'sig': (9, 2),
        'cmd': (),
        'reply': (),

    },
    'Interfaces': {
        'sig': (10, 2),
        'cmd': (),
        'reply': (),

    },
    'ClassObject': {
        'sig': (11, 2),
        'cmd': (),
        'reply': (),

    },
    'SourceDebugExtension': {
        'sig': (12, 2),
        'cmd': (),
        'reply': (),

    },
    'SignatureWithGeneric': {
        'sig': (13, 2),
        'cmd': (),
        'reply': (),

    },
    'FieldsWithGeneric': {
        'sig': (14, 2),
        'cmd': (),
        'reply': (),

    },
    'MethodsWithGeneric': {
        'sig': (15, 2),
        'cmd': (),
        'reply': (),

    },
    'Instances': {
        'sig': (16, 2),
        'cmd': (),
        'reply': (),

    },
    'ClassFileVersion': {
        'sig': (17, 2),
        'cmd': (),
        'reply': (),

    },
    'ConstantPool': {
        'sig': (18, 2),
        'cmd': (),
        'reply': (),

    },
    # ClassType Command Set (3)
    'Superclass': {
        'sig': (1, 3),
        'cmd': (),
        'reply': (),

    },
    'SetValues': {
        'sig': (2, 3),
        'cmd': (),
        'reply': (),

    },
    'InvokeMethod': {
        'sig': (3, 3),
        'cmd': (),
        'reply': (),

    },
    'NewInstance': {
        'sig': (4, 3),
        'cmd': (),
        'reply': (),

    },
    # ArrayType Command Set (4)
    'NewInstance': {
        'sig': (1, 4),
        'cmd': (),
        'reply': (),

    },
    # InterfaceType Command Set (5)
    'InvokeMethod': {
        'sig': (1, 5),
        'cmd': (),
        'reply': (),

    },
    # Method Command Set (6)
    'LineTable': {
        'sig': (1, 6),
        'cmd': (),
        'reply': (),

    },
    'VariableTable': {
        'sig': (2, 6),
        'cmd': (),
        'reply': (),

    },
    'Bytecodes': {
        'sig': (3, 6),
        'cmd': (),
        'reply': (),

    },
    'IsObsolete': {
        'sig': (4, 6),
        'cmd': (),
        'reply': (),

    },
    'VariableTableWithGeneric': {
        'sig': (5, 6),
        'cmd': (),
        'reply': (),

    },
    # Field Command Set (8)
    # ObjectReference Command Set (9)
    'ReferenceType': {
        'sig': (1, 9),
        'cmd': (),
        'reply': (),

    },
    'GetValues': {
        'sig': (2, 9),
        'cmd': (),
        'reply': (),

    },
    'SetValues': {
        'sig': (3, 9),
        'cmd': (),
        'reply': (),

    },
    'MonitorInfo': {
        'sig': (5, 9),
        'cmd': (),
        'reply': (),

    },
    'InvokeMethod': {
        'sig': (6, 9),
        'cmd': (),
        'reply': (),

    },
    'DisableCollection': {
        'sig': (7, 9),
        'cmd': (),
        'reply': (),

    },
    'EnableCollection': {
        'sig': (8, 9),
        'cmd': (),
        'reply': (),

    },
    'IsCollected': {
        'sig': (9, 9),
        'cmd': (),
        'reply': (),

    },
    'ReferringObjects': {
        'sig': (10, 9),
        'cmd': (),
        'reply': (),

    },
    # StringReference Command Set (10)
    'Value': {
        'sig': (1, 10),
        'cmd': (),
        'reply': (),

    },
    # ThreadReference Command Set (11)
    'Name': {
        'sig': (1, 11),
        'cmd': (),
        'reply': (),

    },
    'Suspend': {
        'sig': (2, 11),
        'cmd': (),
        'reply': (),

    },
    'Resume': {
        'sig': (3, 11),
        'cmd': (),
        'reply': (),

    },
    'Status': {
        'sig': (4, 11),
        'cmd': (),
        'reply': (),

    },
    'ThreadGroup': {
        'sig': (5, 11),
        'cmd': (),
        'reply': (),

    },
    'Frames': {
        'sig': (6, 11),
        'cmd': (),
        'reply': (),

    },
    'FrameCount': {
        'sig': (7, 11),
        'cmd': (),
        'reply': (),

    },
    'OwnedMonitors': {
        'sig': (8, 11),
        'cmd': (),
        'reply': (),

    },
    'CurrentContendedMonitor': {
        'sig': (9, 11),
        'cmd': (),
        'reply': (),

    },
    'Stop': {
        'sig': (10, 11),
        'cmd': (),
        'reply': (),

    },
    'Interrupt': {
        'sig': (11, 11),
        'cmd': (),
        'reply': (),

    },
    'SuspendCount': {
        'sig': (12, 11),
        'cmd': (),
        'reply': (),

    },
    'OwnedMonitorsStackDepthInfo': {
        'sig': (13, 11),
        'cmd': (),
        'reply': (),

    },
    'ForceEarlyReturn': {
        'sig': (14, 11),
        'cmd': (),
        'reply': (),

    },
    # ThreadGroupReference Command Set (12)
    'Name': {
        'sig': (1, 12),
        'cmd': (),
        'reply': (),

    },
    'Parent': {
        'sig': (2, 12),
        'cmd': (),
        'reply': (),

    },
    'Children': {
        'sig': (3, 12),
        'cmd': (),
        'reply': (),

    },
    # ArrayReference Command Set (13)
    'Length': {
        'sig': (1, 13),
        'cmd': (),
        'reply': (),

    },
    'GetValues': {
        'sig': (2, 13),
        'cmd': (),
        'reply': (),

    },
    'SetValues': {
        'sig': (3, 13),
        'cmd': (),
        'reply': (),

    },
    # ClassLoaderReference Command Set (14)
    'VisibleClasses': {
        'sig': (1, 14),
        'cmd': (),
        'reply': (),

    },
    # EventRequest Command Set (15)
    'Set': {
        'sig': (1, 15),
        'cmd': (),
        'reply': (),

    },
    'Clear': {
        'sig': (2, 15),
        'cmd': (),
        'reply': (),

    },
    'ClearAllBreakpoints': {
        'sig': (3, 15),
        'cmd': (),
        'reply': (),

    },
    # StackFrame Command Set (16)
    'GetValues': {
        'sig': (1, 16),
        'cmd': (),
        'reply': (),

    },
    'SetValues': {
        'sig': (2, 16),
        'cmd': (),
        'reply': (),

    },
    'ThisObject': {
        'sig': (3, 16),
        'cmd': (),
        'reply': (),

    },
    'PopFrames': {
        'sig': (4, 16),
        'cmd': (),
        'reply': (),

    },
    # ClassObjectReference Command Set (17)
    'ReflectedType': {
        'sig': (1, 17),
        'cmd': (),
        'reply': (),

    },
    # Event Command Set (64)
    'Composite': {
        'sig': (100, 64),
        'cmd': (),
        'reply': (),

    }
}

# initialize later, set here for auto-complimant
objectIDSize = -1
referenceTypeIDSize = -1
frameIDSize = -1
methodIDSize = -1
fieldIDSize = -1

pack_defs = {
    "short": {  # 2 byte
        'pack': lambda data: (struct.pack(">h", data[:2]), 2),
        'unpack': lambda data: (struct.unpack(">h", data[:2]), 2),
    },
    "char": {  # 2 byte
        'pack': lambda data: (struct.pack(">2s", data[:2]), 2),
        'unpack': lambda data: (struct.unpack(">2s", data[:2]), 2),
    },
    "float": {  # 4 byte
        'pack': lambda data: (struct.pack(">f", data[:4]), 4),
        'unpack': lambda data: (struct.unpack(">f", data[:4]), 4),
    },
    "double": {  # 8 byte
        'pack': lambda data: (struct.pack(">d", data[:8]), 8),
        'unpack': lambda data: (struct.unpack(">d", data[:8]), 8),
    },
    "byte": {  # 1 byte
        'pack': lambda data: (struct.pack(">c", data[:1]), 1),
        'unpack': lambda data: (struct.unpack(">c", data[:1]), 1),
    },
    "boolean": {  # 1 byte
        'pack': lambda data: (struct.pack(">?", data[:1]), 1),
        'unpack': lambda data: (struct.unpack(">?", data[:1]), 1),
    },
    "int": {  # 4 bytes
        'pack': lambda data: (struct.pack(">i", data[:4]), 4),
        'unpack': lambda data: (struct.unpack(">i", data[:4]), 4),
    },
    "long": {  # 8 bytes
        'pack': lambda data: (struct.pack(">q", data[:8]), 8),
        'unpack': lambda data: (struct.unpack(">q", data[:8]), 8),
    },
}


def init_IDSIze(size_dict):
    global objectIDSize
    global referenceTypeIDSize
    global frameIDSize
    global methodIDSize
    global fieldIDSize

    objectIDSize = size_dict['objectIDSize']
    referenceTypeIDSize = size_dict['referenceTypeIDSize']
    frameIDSize = size_dict['frameIDSize']
    methodIDSize = size_dict['methodIDSize']
    fieldIDSize = size_dict['fieldIDSize']

    global pack_defs
    _pack_defs = {
        **pack_defs,
        "objectID": {  # Target VM-specific, up to 8 bytes (see below)
            'pack': _pack_id_func(objectIDSize, True),
            'unpack': _pack_id_func(objectIDSize, False)
        },
        "tagged-objectID": {  # size of objectID plus one byte
            'pack': _pack_id_func(objectIDSize, True, tagged=True),
            'unpack': _pack_id_func(objectIDSize, False, tagged=True)
        },
        "threadID": {  # same as objectID
            'pack': _pack_id_func(objectIDSize, True),
            'unpack': _pack_id_func(objectIDSize, False)
        },
        "threadGroupID": {  # same as objectID
            'pack': _pack_id_func(objectIDSize, True),
            'unpack': _pack_id_func(objectIDSize, False)
        },
        "stringID": {  # same as objectID
            'pack': _pack_id_func(objectIDSize, True),
            'unpack': _pack_id_func(objectIDSize, False)
        },
        "classLoaderID": {  # same as objectID
            'pack': _pack_id_func(objectIDSize, True),
            'unpack': _pack_id_func(objectIDSize, False)
        },
        "classObjectID": {  # same as objectID
            'pack': _pack_id_func(objectIDSize, True),
            'unpack': _pack_id_func(objectIDSize, False)
        },
        "arrayID": {  # same as objectID
            'pack': _pack_id_func(objectIDSize, True),
            'unpack': _pack_id_func(objectIDSize, False)
        },
        "referenceTypeID": {  # same as objectID
            'pack': _pack_id_func(referenceTypeIDSize, True),
            'unpack': _pack_id_func(referenceTypeIDSize, False)
        },
        "classID": {  # same as referenceTypeID
            'pack': _pack_id_func(referenceTypeIDSize, True),
            'unpack': _pack_id_func(referenceTypeIDSize, False)
        },
        "interfaceID": {  # same as referenceTypeID
            'pack': _pack_id_func(referenceTypeIDSize, True),
            'unpack': _pack_id_func(referenceTypeIDSize, False)
        },
        "arrayTypeID": {  # same as referenceTypeID
            'pack': _pack_id_func(referenceTypeIDSize, True),
            'unpack': _pack_id_func(referenceTypeIDSize, False)
        },
        "methodID": {  # Target VM-specific, up to 8 bytes (see below)
            'pack': _pack_id_func(methodIDSize, True),
            'unpack': _pack_id_func(methodIDSize, False)
        },
        "fieldID": {  # Target VM-specific, up to 8 bytes (see below)
            'pack': _pack_id_func(fieldIDSize, True),
            'unpack': _pack_id_func(fieldIDSize, False)
        },
        "frameID": {  # Target VM-specific, up to 8 bytes (see below)
            'pack': _pack_id_func(frameIDSize, True),
            'unpack': _pack_id_func(frameIDSize, False)
        },
        "location": {  # Target VM specific
            'pack': lambda data: Exception("Unimplement type"),
            'unpack': lambda data: Exception("Unimplement type")
        },
        "string": {  # Variable
            'pack': _pack_string,
            'unpack': _unpack_string
        },
        "value": {  # Variable
            'pack': _pack_value,
            'unpack': _unpack_value
        },
        "untagged-value": {  # Variable
            'pack': lambda data: (data, len(data)),
            'unpack': lambda data: (data, len(data))
        },
        "arrayregion": {  # Variable
            'pack': lambda data: Exception("Unimplement type"),
            'unpack': lambda data: Exception("Unimplement type")
        },
    }
    pack_defs = _pack_defs


def _pack_id_func(size, is_pack, tagged=False):
    format_pattern = ""
    tagged_pattern = "c" if tagged else ""
    if size == 4:
        format_pattern = "I"
    elif size == 8:
        format_pattern = "Q"
    else:
        raise Exception("Unsupported id size")

    format_pattern = ">%s%s" % (tagged_pattern, format_pattern)
    size = size + 1 if tagged else size

    if is_pack:
        return lambda data: (struct.pack(format_pattern, data[:size]), size)
    else:
        return lambda data: (struct.unpack(format_pattern, data[:size]), size)


def _pack_string(data):
    length = len(data)
    return struct.pack('>I%ss' % length, length, data), 4+length


def _unpack_string(data):
    length = struct.unpack(">I", data[:4])[0]
    content = struct.unpack(">%ss" % length, data[4:4+length])[0]
    return content.decode('utf-8'), 4+length


def _pack_value(data):
    tag = tag_def[data[0]]
    if tag == 'None':
        return (data[0], 1)
    else:
        out_data, size = pack_defs[tag]['pack'](data[1:])
        return data[0] + out_data, size+1


def _unpack_value(data):
    tag = tag_def[data[0]]
    if tag == 'None':
        return (None, 1)
    else:
        data, size = pack_defs[tag]['unpack'](data[1:])
        return data+(tag,), size+1


tag_def = {
    b'91': 'arrayID',  # ARRAY	'[' - an array object (objectID size).  
    b'66': 'byte',  # BYTE	'B' - a byte value (1 byte).  
    b'67': 'char',  # CHAR	'C' - a character value (2 bytes).  
    b'76': 'objectID',  # OBJECT	'L' - an object (objectID size).  
    b'70': 'float',  # FLOAT	'F' - a float value (4 bytes).  
    b'68': 'double',  # DOUBLE	'D' - a double value (8 bytes).  
    b'73': 'int',  # INT	'I' - an int value (4 bytes).  
    b'74': 'long',  # LONG	'J' - a long value (8 bytes).  
    b'83': 'short',  # SHORT	'S' - a short value (2 bytes).  
    b'86': 'None',  # VOID	'V' - a void value (no bytes).  
    b'90': 'boolean',  # BOOLEAN	'Z' - a boolean value (1 byte).  
    b'115': 'stringID',  # STRING	's' - a String object (objectID size).  
    b'116': 'threadID',  # THREAD	't' - a Thread object (objectID size).  
    # THREAD_GROUP	'g' - a ThreadGroup object (objectID size).
    b'103': 'threadGroupID',
    # CLASS_LOADER	'l' - a ClassLoader object (objectID size).
    b'108': 'classLoaderID',
    # CLASS_OBJECT	'c' - a class object object (objectID size).
    b'99': 'classObjectID',
}
