from re import S
import struct
from typing import Any, Callable, Dict, Tuple


class InvokeOptions:
    INVOKE_SINGLE_THREADED = 0x01
    INVOKE_NONVIRTUAL = 0x02


class TypeTag:
    CLASS = 1
    INTERFACE = 2
    ARRAY = 3


class SuspendPolicy:
    NONE = 0
    EVENT_THREAD = 1
    ALL = 2


class ModKind:
    Count = 1
    Conditional = 2
    ThreadOnly = 3
    ClassOnly = 4
    ClassMatch = 5
    ClassExclude = 6
    LocationOnly = 7
    ExceptionOnly = 8
    FieldOnly = 9
    Step = 10
    InstanceOnly = 11
    SourceNameMatch = 12


class EventKind:
    SINGLE_STEP = 1
    BREAKPOINT = 2
    FRAME_POP = 3
    EXCEPTION = 4
    USER_DEFINED = 5
    THREAD_START = 6
    THREAD_DEATH = 7
    THREAD_END = 7  # obsolete - was used in jvmdi
    CLASS_PREPARE = 8
    CLASS_UNLOAD = 9
    CLASS_LOAD = 10
    FIELD_ACCESS = 20
    FIELD_MODIFICATION = 21
    EXCEPTION_CATCH = 30
    METHOD_ENTRY = 40
    METHOD_EXIT = 41
    METHOD_EXIT_WITH_RETURN_VALUE = 42
    MONITOR_CONTENDED_ENTER = 43
    MONITOR_CONTENDED_ENTERED = 44
    MONITOR_WAIT = 45
    MONITOR_WAITED = 46
    VM_START = 90
    VM_INIT = 90  # obsolete - was used in jvmdi
    VM_DEATH = 99
    VM_DISCONNECTED = 100  # Never sent across JDWP


cmd_def = {
    # VirtualMachine Command Set (1)
    'VM_Version': {
        'sig': (1, 1),
        'cmd': (),
        'reply': (
            ('string', 'description'),
            ('int', 'jdwpMajor'),
            ('int', 'jdwpMinor'),
            ('string', 'vmVersion'),
            ('string', 'vmName'),),

    },
    'VM_ClassesBySignature': {
        'sig': (2, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_AllClasses': {
        'sig': (3, 1),
        'cmd': (),
        'reply': (
            ('int', 'classes'),
            ('Repeated classes', (
                ('byte', 'refTypeTag'),
                ('referenceTypeID', 'typeID'),
                ('string', 'signature'),
                ('int', 'status'),
            )),
        ),

    },
    'VM_AllThreads': {
        'sig': (4, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_TopLevelThreadGroups': {
        'sig': (5, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_Dispose': {
        'sig': (6, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_IDSizes': {
        'sig': (7, 1),
        'cmd': (),
        'reply': (
            ("int", "fieldIDSize"),
            ("int", "methodIDSize"),
            ("int", "objectIDSize"),
            ("int", "referenceTypeIDSize"),
            ("int", "frameIDSize")),
    },
    'VM_Suspend': {
        'sig': (8, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_Resume': {
        'sig': (9, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_Exit': {
        'sig': (10, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_CreateString': {
        'sig': (11, 1),
        'cmd': (
            ('string', 'utf'),
        ),
        'reply': (
            ('stringID', 'stringObject'),
        ),

    },
    'VM_Capabilities': {
        'sig': (12, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_ClassPaths': {
        'sig': (13, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_DisposeObjects': {
        'sig': (14, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_HoldEvents': {
        'sig': (15, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_ReleaseEvents': {
        'sig': (16, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_CapabilitiesNew': {
        'sig': (17, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_RedefineClasses': {
        'sig': (18, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_SetDefaultStratum': {
        'sig': (19, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_AllClassesWithGeneric': {
        'sig': (20, 1),
        'cmd': (),
        'reply': (),

    },
    'VM_InstanceCounts': {
        'sig': (21, 1),
        'cmd': (),
        'reply': (),

    },
    # ReferenceType Command Set (2)
    'REF_Signature': {
        'sig': (1, 2),
        'cmd': (),
        'reply': (),
    },
    'REF_ClassLoader': {
        'sig': (2, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_Modifiers': {
        'sig': (3, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_Fields': {
        'sig': (4, 2),
        'cmd': (('referenceTypeID', 'refType'),),
        'reply': (
            ('int', 'declared'),
            ('Repeated declared', (
                ('fieldID', 'fieldID'),
                ('string', 'name'),
                ('string', 'signature'),
                ('int', 'modBits'))
             )
        ),
    },
    'REF_Methods': {
        'sig': (5, 2),
        'cmd': (('referenceTypeID', 'refType'),),
        'reply': (
            ('int', 'declared'),
            ('Repeated declared', (
                ('methodID', 'methodID'),
                ('string', 'name'),
                ('string', 'signature'),
                ('int', 'modBits'))
             )
        ),

    },
    'REF_GetValues': {
        'sig': (6, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_SourceFile': {
        'sig': (7, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_NestedTypes': {
        'sig': (8, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_Status': {
        'sig': (9, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_Interfaces': {
        'sig': (10, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_ClassObject': {
        'sig': (11, 2),
        'cmd': (('referenceTypeID','refType'),),
        'reply': (('classObjectID', 'classObject'),),
    },
    'REF_SourceDebugExtension': {
        'sig': (12, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_SignatureWithGeneric': {
        'sig': (13, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_FieldsWithGeneric': {
        'sig': (14, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_MethodsWithGeneric': {
        'sig': (15, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_Instances': {
        'sig': (16, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_ClassFileVersion': {
        'sig': (17, 2),
        'cmd': (),
        'reply': (),

    },
    'REF_ConstantPool': {
        'sig': (18, 2),
        'cmd': (),
        'reply': (),

    },
    # ClassType Command Set (3)
    'CLS_Superclass': {
        'sig': (1, 3),
        'cmd': (('classID','clazz'),),
        'reply': (('classID','superclass'),),

    },
    'CLS_SetValues': {
        'sig': (2, 3),
        'cmd': (),
        'reply': (),

    },
    'CLS_InvokeMethod': {
        'sig': (3, 3),
        'cmd': (
            ('classID', 'clazz'),
            ('threadID', 'thread'),
            ('methodID', 'methodID'),
            ('int', 'arguments'),
            ('Repeated arguments', (
                ('value', 'arg'),
            )),
            ('int', 'options'),
        ),
        'reply': (
            ('value', 'returnValue'),
            ('tagged-objectID', 'exception'),
        ),

    },
    'CLS_NewInstance': {
        'sig': (4, 3),
        'cmd': (),
        'reply': (),

    },
    # ArrayType Command Set (4)
    'ARR_NewInstance': {
        'sig': (1, 4),
        'cmd': (),
        'reply': (),

    },
    # InterfaceType Command Set (5)
    'INTF_InvokeMethod': {
        'sig': (1, 5),
        'cmd': (
            ('interfaceID', 'clazz'),
            ('threadID', 'thread'),
            ('methodID', 'methodID'),
            ('int', 'arguments'),
            ('Repeated arguments', (
                ('value', 'arg'),
            )),
            ('int', 'options'),
        ),
        'reply': (
            ('value', 'returnValue'),
            ('tagged-objectID', 'exception'),
        ),
    },
    # Method Command Set (6)
    'MTHD_LineTable': {
        'sig': (1, 6),
        'cmd': (),
        'reply': (),

    },
    'MTHD_VariableTable': {
        'sig': (2, 6),
        'cmd': (),
        'reply': (),

    },
    'MTHD_Bytecodes': {
        'sig': (3, 6),
        'cmd': (),
        'reply': (),

    },
    'MTHD_IsObsolete': {
        'sig': (4, 6),
        'cmd': (),
        'reply': (),

    },
    'MTHD_VariableTableWithGeneric': {
        'sig': (5, 6),
        'cmd': (),
        'reply': (),

    },
    # Field Command Set (8)
    # ObjectReference Command Set (9)
    'OBJ_ReferenceType': {
        'sig': (1, 9),
        'cmd': (('objectID', 'object'),),
        'reply': (
            ('byte', 'refTypeTag'),
            ('referenceTypeID', 'typeID')
        ),
    },
    'OBJ_GetValues': {
        'sig': (2, 9),
        'cmd': (),
        'reply': (),

    },
    'OBJ_SetValues': {
        'sig': (3, 9),
        'cmd': (),
        'reply': (),

    },
    'OBJ_MonitorInfo': {
        'sig': (5, 9),
        'cmd': (),
        'reply': (),

    },
    'OBJ_InvokeMethod': {
        'sig': (6, 9),
        'cmd': (
            ('objectID', 'object'),
            ('threadID', 'thread'),
            ('classID', 'clazz'),
            ('methodID', 'methodID'),
            ('int', 'arguments'),
            ('Repeated arguments', (
                ('value', 'arg'),
            )),
            ('int', 'options'),
        ),
        'reply': (
            ('value', 'returnValue'),
            ('tagged-objectID', 'exception'),
        ),

    },
    'OBJ_DisableCollection': {
        'sig': (7, 9),
        'cmd': (),
        'reply': (),

    },
    'OBJ_EnableCollection': {
        'sig': (8, 9),
        'cmd': (),
        'reply': (),

    },
    'OBJ_IsCollected': {
        'sig': (9, 9),
        'cmd': (),
        'reply': (),

    },
    'OBJ_ReferringObjects': {
        'sig': (10, 9),
        'cmd': (),
        'reply': (),

    },
    # StringReference Command Set (10)
    'STR_Value': {
        'sig': (1, 10),
        'cmd': (
            ('objectID', 'stringObject'),
        ),
        'reply': (
            ('string', 'stringValue'),
        ),

    },
    # ThreadReference Command Set (11)
    'THD_Name': {
        'sig': (1, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_Suspend': {
        'sig': (2, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_Resume': {
        'sig': (3, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_Status': {
        'sig': (4, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_ThreadGroup': {
        'sig': (5, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_Frames': {
        'sig': (6, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_FrameCount': {
        'sig': (7, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_OwnedMonitors': {
        'sig': (8, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_CurrentContendedMonitor': {
        'sig': (9, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_Stop': {
        'sig': (10, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_Interrupt': {
        'sig': (11, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_SuspendCount': {
        'sig': (12, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_OwnedMonitorsStackDepthInfo': {
        'sig': (13, 11),
        'cmd': (),
        'reply': (),

    },
    'THD_ForceEarlyReturn': {
        'sig': (14, 11),
        'cmd': (),
        'reply': (),

    },
    # ThreadGroupReference Command Set (12)
    'THDGRP_Name': {
        'sig': (1, 12),
        'cmd': (),
        'reply': (),

    },
    'THDGRP_Parent': {
        'sig': (2, 12),
        'cmd': (),
        'reply': (),

    },
    'THDGRP_Children': {
        'sig': (3, 12),
        'cmd': (),
        'reply': (),

    },
    # ArrayReference Command Set (13)
    'ARRREF_Length': {
        'sig': (1, 13),
        'cmd': (),
        'reply': (),

    },
    'ARRREF_GetValues': {
        'sig': (2, 13),
        'cmd': (),
        'reply': (),

    },
    'ARRREF_SetValues': {
        'sig': (3, 13),
        'cmd': (),
        'reply': (),

    },
    # ClassLoaderReference Command Set (14)
    'ARRREF_VisibleClasses': {
        'sig': (1, 14),
        'cmd': (),
        'reply': (),

    },
    # EventRequest Command Set (15)
    'EVT_Set': {
        'sig': (1, 15),
        'cmd': (
            ('byte', 'eventKind'),
            ('byte', 'suspendPolicy'),
            ('int', 'modifiers'),
            ('Repeated modifiers', (
                ('byte', 'modKind'),
                ('Case modKind', {
                    ModKind.Count: (
                        ('int', 'count'),
                    ),
                    ModKind.Conditional: (
                        ('int', 'exprID'),
                    ),
                    ModKind.ThreadOnly: (
                        ('threadID', 'thread'),
                    ),
                    ModKind.ClassOnly: (
                        ('referenceTypeID', 'clazz'),
                    ),
                    ModKind.ClassMatch: (
                        ('string', 'classPattern'),
                    ),
                    ModKind.ClassExclude: (
                        ('string', 'classPattern'),
                    ),
                    ModKind.LocationOnly: (
                        ('location', 'loc'),),
                    ModKind.ExceptionOnly: (
                        ('referenceTypeID', 'exceptionOrNull'),
                        ('boolean', 'caught'),
                        ('boolean', 'uncaught')
                    ),
                    ModKind.FieldOnly: (
                        ('referenceTypeID', 'declaring'),
                        ('fieldID', 'fieldID')
                    ),
                    ModKind.Step: (
                        ('threadID', 'thread'),
                        ('int', 'size'),
                        ('int', 'depth')
                    ),
                    ModKind.InstanceOnly: (
                        ('objectID', 'instance'),
                    ),
                    ModKind.SourceNameMatch: (
                        ('string', 'sourceNamePattern'),
                    ),
                })
            )),
        ),
        'reply': (
            ('int', 'requestID'),
        ),

    },
    'EVT_Clear': {
        'sig': (2, 15),
        'cmd': (
            ('byte', 'eventKind'),
            ('int', 'requestID')
        ),
        'reply': (),

    },
    'EVT_ClearAllBreakpoints': {
        'sig': (3, 15),
        'cmd': (),
        'reply': (),

    },
    # StackFrame Command Set (16)
    'STK_GetValues': {
        'sig': (1, 16),
        'cmd': (),
        'reply': (),

    },
    'STK_SetValues': {
        'sig': (2, 16),
        'cmd': (),
        'reply': (),

    },
    'STK_ThisObject': {
        'sig': (3, 16),
        'cmd': (),
        'reply': (),

    },
    'STK_PopFrames': {
        'sig': (4, 16),
        'cmd': (),
        'reply': (),

    },
    # ClassObjectReference Command Set (17)
    'CLSOBJ_ReflectedType': {
        'sig': (1, 17),
        'cmd': (),
        'reply': (),
    },
    # Event Command Set (64)
    'EVTSET_Composite': {
        'sig': (100, 64),
        'cmd': (('byte', 'suspendPolicy'),
                ('int', 'events'),
                ('Repeated events', (
                    ('byte', 'eventKind'),
                    ('Case eventKind', {
                        EventKind.VM_START: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                        ),
                        EventKind.SINGLE_STEP: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('location', 'location'),
                        ),
                        EventKind.BREAKPOINT: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('location', 'location'),
                        ),
                        EventKind.METHOD_ENTRY: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('location', 'location'),
                        ),
                        EventKind.METHOD_EXIT: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('location', 'location'),
                        ),
                        EventKind.METHOD_EXIT_WITH_RETURN_VALUE: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('location', 'location'),
                            ('value', 'value'),
                        ),
                        EventKind.MONITOR_CONTENDED_ENTER: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('tagged-objectID', 'object'),
                            ('location', 'location'),
                        ),
                        EventKind.MONITOR_CONTENDED_ENTERED: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('tagged-objectID', 'object'),
                            ('location', 'location'),
                        ),
                        EventKind.MONITOR_WAIT: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('tagged-objectID', 'object'),
                            ('location', 'location'),
                            ('long', 'timeout'),
                        ),
                        EventKind.MONITOR_WAITED: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('tagged-objectID', 'object'),
                            ('location', 'location'),
                            ('boolean', 'timed_out'),
                        ),
                        EventKind.EXCEPTION: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('location', 'location'),
                            ('tagged-objectID', 'exception'),
                            ('location', 'catchLocation'),
                        ),
                        EventKind.THREAD_START: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                        ),
                        EventKind.THREAD_DEATH: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                        ),
                        EventKind.CLASS_PREPARE: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('byte', 'refTypeTag'),
                            ('referenceTypeID', 'typeID'),
                            ('string', 'signature'),
                            ('int', 'status'),
                        ),
                        EventKind.CLASS_UNLOAD: (
                            ('int', 'requestID'),
                            ('string', 'signature'),
                        ),
                        EventKind.FIELD_ACCESS: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('location', 'location'),
                            ('byte', 'refTypeTag'),
                            ('referenceTypeID', 'typeID'),
                            ('fieldID', 'fieldID'),
                            ('tagged-objectID', 'object'),
                        ),
                        EventKind.FIELD_MODIFICATION: (
                            ('int', 'requestID'),
                            ('threadID', 'thread'),
                            ('location', 'location'),
                            ('byte', 'refTypeTag'),
                            ('referenceTypeID', 'typeID'),
                            ('fieldID', 'fieldID'),
                            ('tagged-objectID', 'object'),
                            ('value', 'valueToBe'),
                        ),
                        EventKind.VM_DEATH: (
                            ('int', 'requestID'),
                        )
                    })))),
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
        'pack': lambda data: (struct.pack(">h", data), 2),
        'unpack': lambda data: (struct.unpack(">h", data[:2]), 2),
    },
    "char": {  # 2 byte
        'pack': lambda data: (struct.pack(">2s", data), 2),
        'unpack': lambda data: (struct.unpack(">2s", data[:2]), 2),
    },
    "float": {  # 4 byte
        'pack': lambda data: (struct.pack(">f", data), 4),
        'unpack': lambda data: (struct.unpack(">f", data[:4]), 4),
    },
    "double": {  # 8 byte
        'pack': lambda data: (struct.pack(">d", data), 8),
        'unpack': lambda data: (struct.unpack(">d", data[:8]), 8),
    },
    "byte": {  # 1 byte
        'pack': lambda data: (struct.pack(">B", data), 1),
        'unpack': lambda data: (struct.unpack(">B", data[:1]), 1),
    },
    "boolean": {  # 1 byte
        'pack': lambda data: (struct.pack(">?", data), 1),
        'unpack': lambda data: (struct.unpack(">?", data[:1]), 1),
    },
    "int": {  # 4 bytes
        'pack': lambda data: (struct.pack(">i", data), 4),
        'unpack': lambda data: (struct.unpack(">i", data[:4]), 4),
    },
    "long": {  # 8 bytes
        'pack': lambda data: (struct.pack(">q", data), 8),
        'unpack': lambda data: (struct.unpack(">q", data[:8]), 8),
    },
}


DataDictType = Dict[str, Any]


def init_IDSIze(size_dict: DataDictType):
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
            'pack': _pack_location(True),
            'unpack': _pack_location(False)
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


def _pack_id_func(size: int, is_pack: bool, tagged: bool = False) -> Callable:
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
        if tagged:
            return lambda data: (struct.pack(format_pattern, *data), size)
        else:
            return lambda data: (struct.pack(format_pattern, data), size)
    else:
        return lambda data: (struct.unpack(format_pattern, data[:size]), size)


def _pack_location(is_pack: bool) -> Callable:
    global referenceTypeIDSize
    global methodIDSize

    spec = {4: "I", 8: "Q"}
    format_pattern = ">B" + \
        spec[referenceTypeIDSize] + spec[methodIDSize] + 'Q'

    size = 1 + referenceTypeIDSize + methodIDSize + 8
    if is_pack:
        return lambda data: (struct.pack(format_pattern, *data), size)
    else:
        return lambda data: (struct.unpack(format_pattern, data[:size]), size)


def _pack_string(data: str) -> Tuple[bytes, int]:
    length = len(data)
    return struct.pack('>I%ss' % length, length, data.encode('utf-8')), 4+length


def _unpack_string(data: bytes) -> Tuple[str, int]:
    length = struct.unpack(">I", data[:4])[0]
    content = struct.unpack(">%ss" % length, data[4:4+length])[0]
    return content.decode('utf-8'), 4+length


def _pack_value(data:Tuple[Any, str]) -> Tuple[bytes, int]:
    data, tag = data
    if tag == 'None':
        return tag_def[tag], 1
    else:
        out_data, size = pack_defs[tag]['pack'](data)
        return tag_def[tag] + out_data, size+1


def _unpack_value(data: bytes) -> Tuple[Any, int]:
    tag = tag_lbl[data[0]]
    if tag == 'None':
        return (None, tag), 1
    else:
        data, size = pack_defs[tag]['unpack'](data[1:])
        return data+(tag,), size+1


tag_lbl = {
    91: 'arrayID',  # ARRAY	'[' - an array object (objectID size).  
    66: 'byte',  # BYTE	'B' - a byte value (1 byte).  
    67: 'char',  # CHAR	'C' - a character value (2 bytes).  
    76: 'objectID',  # OBJECT	'L' - an object (objectID size).  
    70: 'float',  # FLOAT	'F' - a float value (4 bytes).  
    68: 'double',  # DOUBLE	'D' - a double value (8 bytes).  
    73: 'int',  # INT	'I' - an int value (4 bytes).  
    74: 'long',  # LONG	'J' - a long value (8 bytes).  
    83: 'short',  # SHORT	'S' - a short value (2 bytes).  
    86: 'None',  # VOID	'V' - a void value (no bytes).  
    90: 'boolean',  # BOOLEAN	'Z' - a boolean value (1 byte).  
    115: 'stringID',  # STRING	's' - a String object (objectID size).  
    116: 'threadID',  # THREAD	't' - a Thread object (objectID size).  
    # THREAD_GROUP	'g' - a ThreadGroup object (objectID size).
    103: 'threadGroupID',
    # CLASS_LOADER	'l' - a ClassLoader object (objectID size).
    108: 'classLoaderID',
    # CLASS_OBJECT	'c' - a class object object (objectID size).
    99: 'classObjectID',
}


tag_def = {value:struct.pack('>B', key) for key, value in tag_lbl.items()}