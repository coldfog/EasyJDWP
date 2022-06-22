cmd_def = {
    # VirtualMachine Command Set (1)
    'Version': {
        'sig': (1, 1),
        'cmd': (),
        'reply': (),

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
        'reply': (("fieldIDSize", "I"), ("methodIDSize", "I"), ("objectIDSize", "I"), ("referenceTypeIDSize", "I"), ("frameIDSize", "I")),
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
