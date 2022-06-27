import re
import socket
import struct
import subprocess
from sys import prefix
from time import sleep
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from weakref import ReferenceType

from pyparsing import java_style_comment
import protocol_defs
from protocol_defs import EventKind, ModKind, SuspendPolicy, TypeTag, cmd_def
from protocol_defs import pack_defs
from protocol_defs import tag_lbl, tag_def
import types

import logging
from logging import debug, info, warning, error
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


class COMM:
    HANDSHAKE = b"JDWP-Handshake"
    CMD_FLAG = 0x00
    REPLY_FLAG = 0x80


class JDWPVM:
    PLATFORM_ANDROID = 1
    HEADER_SIZE = 11

    def __init__(self, platform: int = PLATFORM_ANDROID) -> None:
        # TODO Add evironment check like adb
        self.port = 0
        self.host = ""
        self.platform = platform
        self.id = 1
        self.target_id = -1
        self.fieldIDSize = -1
        self.methodIDSize = -1
        self.objectIDSize = -1
        self.referenceTypeIDSize = -1
        self.frameIDSize = -1
        self._classes = {}
        self._event_delegates = {}

    def box_value(self, value: Any, tag: Optional[str] = None) -> Tuple[Any, int]:
        if tag != None:
            return value, tag

        type_name = value.__class__.__name__

        if type_name == 'bytes':
            if len(value) == 1:
                return value, 'byte'
            else:
                raise Exception('Unsupported type value bytes')
        if type_name == 'str':
            return self.create_string(value).objectID, 'objectID'  # 'stringID'
        elif type_name == 'NoneType':
            return value, 'None'
        elif type_name in ('float', 'int'):
            return value, type_name
        elif type_name == 'bool':
            return value, 'boolean'

        if isinstance(value, RefrerenceType):
            return value.referenceTypeID, 'objectID'

        if type(value) == StringReference:
            return value.objectID, 'stringID'
        elif isinstance(value, ObjectReference):
            return value.objectID, 'objectID'

        raise Exception('Unsupported type value')

    def unbox_value(self, value: Tuple[Any, str]) -> Any:
        data, tag = value
        # primary type ret it self
        if tag in ('byte', 'char', 'float', 'double', 'int', 'long', 'short', 'boolean'):
            return data
        elif tag == 'stringID':  # string will auto deref itself
            return self.string_val(data)
        elif tag == 'objectID':
            return ObjectReference(self, data)

        raise Exception('Unsupported type value')
        # elif tag == 'classObjectID':
        #     return ClassType(self, data)
        # else:
        #     return data, tag

    def connect(self, host: str = "127.0.0.1", port: int = 8700) -> None:
        if self.platform == JDWPVM.PLATFORM_ANDROID:
            subprocess.run(['adb', 'shell', 'am', 'set-debug-app',
                            '-w', package_name], stdout=subprocess.DEVNULL)
            subprocess.run(['adb', 'shell', 'monkey', '-p', package_name, '-c',
                            'android.intent.category.LAUNCHER 1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            info("Setup %s in debug mode" % package_name)

            try:
                # adb jdwp will not finish by itself
                subprocess.run(['adb', 'jdwp'], timeout=1, capture_output=True)
            except subprocess.TimeoutExpired as e:
                jdwp_port = int(e.output)

            subprocess.run(['adb', 'forward', 'tcp:%d' %
                            port, 'jdwp:%d' % jdwp_port])
            info("bind jdwp into %s:%d (JDWP port: %d)" %
                 (host, port, jdwp_port))

        self.port = port
        self.jdwp_port = jdwp_port
        self.host = host

        info("Start handshake")
        self._handshake()
        info("Handshake Success")

        self._set_id_size()
        self.get_version()
        self._get_all_classes()

    def _sig_parse(self, s: str) -> list:
        matched = re.match(r"\((?P<param>.*)\)(?P<ret>.*)", s)
        ret_val_str = matched.group('ret')
        params_str = matched.group("param")
        params = re.findall(
            r"(?P<param>\[?[BCDFISJZV]|\[?L[\w/]+;)", params_str)

        return params, ret_val_str

    def javasig_to_pysig(self, str):
        param, ret = self._sig_parse(str)
        return self._sig_to_pysig(param)

    def _sig_to_pysig(self, param):
        type_table = dict(
            B='int',
            C='int',
            D='float',
            F='float',
            I='int',
            S='int',
            J='int',
            Z='bool',
            V='NoneType'
        )

        def __convert(val: str):
            prefix = ""
            if val[0] == '[':
                prefix = "list_"
                val = val[1:]

            if val[0] == 'L':
                if val.endswith('String;'):
                    return prefix + 'str'
                else:
                    return prefix + 'objectID'
            return prefix + type_table[val]

        pysig = ','.join([__convert(i) for i in param])
        return pysig

    def type_to_pysig(self, param):
        def __convert(obj):
            prefix = ""
            if isinstance(obj, list):
                prefix = 'list_'
                obj = obj[0]
            
            type_name = obj.__class__.__name__
            if type_name in ('int', 'float', 'bool', 'NoneType', 'str'):
                return prefix+type_name
            else:
                return prefix+'objectID'

        pysig = ','.join([__convert(i) for i in param])# + '|' + __convert(ret_val)
        return pysig


    def _path_parse(self, s: str) -> Tuple[str, str]:
        i = s.rfind('.')
        if i == -1:
            raise Exception('Cannot parse path')
        return 'L' + s[:i].replace('.', '/') + ';', s[i:][1:]

    def set_break_at_method(self, method_sig: str, methodsig:str=None) -> int:
        class_name, method_name = self._path_parse(method_sig)
        cls_info = self.get_class(class_name)
        method_info = cls_info.get_methodInfo(method_name)

        if methodsig:
            pysig = self.javasig_to_pysig(methodsig)
        else:
            pysig = ''

        ret = self.command('EVT_Set',
                           eventKind=EventKind.BREAKPOINT,
                           suspendPolicy=SuspendPolicy.ALL,
                           modifiers=1,
                           modifiers_list=[
                               dict(
                                   modKind=ModKind.LocationOnly,
                                   loc=(
                                       TypeTag.CLASS, cls_info.referenceTypeID, method_info[pysig]['methodID'], 0)
                               )
                           ]
                           )
        requestID = ret['requestID']
        info('Set break point at %s, requestID: %d' % (method_sig, requestID))
        return requestID

    def _get_all_classes(self) -> None:
        ret_data = self.command('VM_AllClasses')
        for data in ret_data['classes_list']:
            self._classes[data['signature']] = data

    def get_class(self, name: str) -> "ClassType":
        ref_info = self._classes[name]
        return ClassType(self, ref_info['typeID'])

    def get_version(self) -> None:
        ret_data = self.command('VM_Version')

        for k in ret_data:
            info("%s: %s" % (k, ret_data[k]))

    def _handshake(self) -> None:
        s = socket.socket()
        try:
            s.connect((self.host, self.port))
        except socket.error as msg:
            error("Failed to connect: %s" % msg)
            raise Exception("Failed to connect: %s" % msg)
        s.send(COMM.HANDSHAKE)

        if s.recv(len(COMM.HANDSHAKE)) != COMM.HANDSHAKE:
            error("Failed to handshake, Please close AndroidStudio, UE4 and other programs that may occupy ADB before using this program")
            raise Exception("Failed to handshake")
        else:
            self.socket = s

    def _recv_cmd(self) -> Tuple[bytes, Tuple[int, int], int]:
        header = self.socket.recv(JDWPVM.HEADER_SIZE)
        pkt_len, id, flags, cmd_set, cmd = struct.unpack('>IIBBB', header)

        self.target_id = id
        data_len = pkt_len - JDWPVM.HEADER_SIZE
        cmd_sig = (cmd, cmd_set)

        data = b''
        while len(data) < data_len:
            left_size = data_len - len(data)
            data += self.socket.recv(1024 if left_size > 1024 else left_size)

        return data, cmd_sig, id

    def _send_cmd_reply(self, target_id: int, errorcode: int, data: bytes):
        flags = COMM.REPLY_FLAG
        pkt_len = len(data) + JDWPVM.HEADER_SIZE
        pkt_id = target_id
        pkt = struct.pack('>IIBH', pkt_len, pkt_id, flags, errorcode)
        self.socket.sendall(pkt+data)

    def _send_cmd(self, cmd_sig: Tuple[int, int], data: bytes = b'') -> int:
        flags = COMM.CMD_FLAG
        cmd, cmd_set = cmd_sig
        pkt_len = len(data) + JDWPVM.HEADER_SIZE
        pkt_id = self.id
        pkt = struct.pack(">IIBBB%ds" % len(data), pkt_len,
                          pkt_id, flags, cmd_set, cmd, data)
        self.id += 2
        self.socket.sendall(pkt)
        return pkt_id

    def _recv_cmd_reply(self, pkt_id: int) -> bytes:
        header = self.socket.recv(JDWPVM.HEADER_SIZE)
        if header == b'':
            header = self.socket.recv(JDWPVM.HEADER_SIZE)

        pkt_len, id, flags, errcode = struct.unpack('>IIBH', header)
        # TODO Error handling
        if errcode != 0:
            raise Exception('Error! code:%d' % errcode)
        assert flags == COMM.REPLY_FLAG, "Reply Flag is not correct!"
        assert pkt_id == id, "Reply packet is not for sending"
        data_len = pkt_len - JDWPVM.HEADER_SIZE

        data = b''
        while len(data) < data_len:
            left_size = data_len - len(data)
            data += self.socket.recv(1024 if left_size > 1024 else left_size)

        return data

    def _pack_data(self, data_sig: Tuple[int, int], data_dict: Dict[str, Any]) -> Tuple[bytes, int]:
        out_data = b''
        index = 0
        for val_type, val_name in data_sig:
            if val_type.startswith('Repeated'):
                _, len_name = val_type.split()
                length = data_dict[len_name]
                for data in data_dict[len_name+'_list']:
                    packed_data, size = self._pack_data(val_name, data)
                    out_data += packed_data
                    index += size
            elif val_type.startswith('Case'):
                _, case_name = val_type.split()
                case = data_dict[case_name]
                case_data_sig = val_name[case]
                packed_data, size = self._pack_data(case_data_sig, data_dict)
                out_data += packed_data
                index += size
            else:
                packed_data, size = pack_defs[val_type]['pack'](
                    data_dict[val_name])
                out_data += packed_data
                index += size

        assert index == len(out_data), "Data Pack Error"
        return out_data, index

    def _unpack_data(self, data_sig: Tuple[str, Any], data: bytes) -> Tuple[Dict[str, Any], int]:
        index = 0
        data_dict = {}
        for val_type, val_name in data_sig:
            if val_type.startswith('Repeated'):
                _, len_name = val_type.split()
                length = data_dict[len_name]
                tmp_arr = []
                for i in range(length):
                    tmp_data_dict, data_consumed = self._unpack_data(
                        val_name, data[index:])
                    index += data_consumed
                    tmp_arr.append(tmp_data_dict)
                data_dict[len_name+'_list'] = tmp_arr
            elif val_type.startswith('Case'):
                _, case_name = val_type.split()
                case = data_dict[case_name]
                unpacked_data, size = self._unpack_data(
                    val_name[case], data[index:])
                data_dict[case_name+'_val'] = unpacked_data
                index += size
            else:
                unpacked_data, size = pack_defs[val_type]['unpack'](
                    data[index:])
                index += size
                data_dict[val_name] = unpacked_data[0] if len(
                    unpacked_data) == 1 else unpacked_data

        return data_dict, index

    def command(self, cmd_name: str, **kwargs) -> Dict[str, Any]:
        if cmd_name == 'OBJ_InvokeMethod':
            sleep(1)
        cmd = cmd_def[cmd_name]
        data, _ = self._pack_data(cmd['cmd'], kwargs)
        pack_id = self._send_cmd(cmd['sig'], data)

        reply_data = self._recv_cmd_reply(pack_id)
        data, _ = self._unpack_data(cmd['reply'], reply_data)

        return data

    def _set_id_size(self) -> None:
        ret_data = jdwp.command('VM_IDSizes')
        debug('idsize: ' + repr(ret_data))
        for k in ret_data:
            setattr(self, k, ret_data[k])

        protocol_defs.init_IDSIze(ret_data)
        global pack_defs
        pack_defs = protocol_defs.pack_defs

    def vm_resume(self) -> None:
        ret = self.command('VM_Resume')
        info('VM Resumed')

    def wait_for_event(self) -> Tuple[int, List["Event"]]:

        cmd = cmd_def['EVTSET_Composite']

        data, sig, cmd_id = self._recv_cmd()
        assert sig == cmd['sig'], 'Not Event cmd!'

        ret, size = self._unpack_data(cmd['cmd'], data)
        sus_policy = ret['suspendPolicy']
        event_num = ret['events']
        event_list = ret['events_list']
        events = {}

        for event_attr in event_list:
            events[event_attr['eventKind']] = Event(event_attr)

        for delegateKind in self._event_delegates:
            delegates = self._event_delegates[delegateKind]
            if delegateKind in events:
                event = events[delegateKind]
                info('EventKind: %d RequestID: %d triggered.' %
                     (delegateKind, event.requestID))
                should_remove = []
                for i, callback in enumerate(delegates):
                    if callback(event):
                        should_remove.append(i)

                self._event_delegates[delegateKind] = [
                    val for j, val in enumerate(delegates) if j not in should_remove]

        return sus_policy, events

    # callback return true will remove it self, otherwise keep self
    def register_for_event(self, evenKind: int, callback: Callable):
        if evenKind not in self._event_delegates:
            self._event_delegates[evenKind] = []

        self._event_delegates[evenKind].append(callback)

    def clear_event(self, event_kind: int, request_id: int) -> None:
        ret = self.command('EVT_Clear',
                           eventKind=event_kind,
                           requestID=request_id)

    def create_string(self, string: str) -> "StringReference":
        stringID = self.command('VM_CreateString', utf=string)['stringObject']
        return StringReference(self, stringID)

    def string_val(self, objID: int) -> str:
        return self.command('STR_Value', stringObject=objID)['stringValue']


class Event:
    def __init__(self, event_attr: Dict[str, Any]) -> None:
        self.eventKind = event_attr['eventKind']
        event_val = event_attr['eventKind_val']
        for k in event_val:
            self.__setattr__(k, event_val[k])


class VMObj:
    def __init__(self, vm: JDWPVM) -> None:
        self.vm = vm


class RefrerenceType(VMObj):
    def __init__(self, vm: JDWPVM, referenceTypeID: int) -> None:
        super().__init__(vm)
        self.referenceTypeID = referenceTypeID
        self.signature = None
        self.refTypeTag = None
        self.methods = {}
        self.fields = {}

        self._init_methods()
        self._init_fields()

    def _init_methods(self) -> None:
        self.methods = {}
        method_arr = self.vm.command(
            'REF_Methods', refType=self.referenceTypeID)
        for method_info in method_arr['declared_list']:
            name = method_info['name']
            pysig = self.vm.javasig_to_pysig(method_info['signature'])
            if name not in self.methods:
                self.methods[name] = {}
            self.methods[name][pysig] = method_info

    def _init_fields(self) -> None:
        self.fields = {}
        field_arr = self.vm.command('REF_Fields', refType=self.referenceTypeID)
        for field_info in field_arr['declared_list']:
            self.fields[field_info['name']] = field_info


class InterfaceType(RefrerenceType):
    def __init__(self, vm: JDWPVM, referenceTypeID: int) -> None:
        super().__init__(vm, referenceTypeID)
        pass


class ArrayType(RefrerenceType):
    def __init__(self, vm: JDWPVM, referenceTypeID: int) -> None:
        super().__init__(vm, referenceTypeID)
        pass


class ClassType(RefrerenceType):
    def __init__(self, vm: JDWPVM, referenceTypeID: int) -> None:
        super().__init__(vm, referenceTypeID)
        ret = self.vm.command('CLS_Superclass', clazz=self.referenceTypeID)[
            'superclass']
        if ret != 0:
            self.superClass = ClassType(self.vm, ret)
        else:
            self.superClass = None

    def get_methodInfo(self, name: str) -> Optional[int]:
        cur_clz = self
        while cur_clz != None:
            if name in cur_clz.methods:
                return cur_clz.methods[name]
            cur_clz = cur_clz.superClass

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError as e:
            methodsig_dict = self.get_methodInfo(__name)
            if methodsig_dict:
                def _ref_method(thread_id, *arg):
                    pysig = self.vm.type_to_pysig(arg)
                    ret = self.vm.command('CLS_InvokeMethod',
                                          clazz=self.referenceTypeID,
                                          thread=thread_id,
                                          methodID=methodsig_dict[pysig]['methodID'],
                                          options=0,
                                          arguments=len(arg),
                                          arguments_list=arg)
                    # TODO exception handling
                    ret_exception = ret['exception']

                    return self.vm.unbox_value(ret['returnValue'])
                return _ref_method
            raise e

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)


class ObjectReference(VMObj):
    def __init__(self, vm: JDWPVM, objID: int) -> None:
        super().__init__(vm)
        self.objectID = objID
        self.referenceType = self.vm

        self.refTypeTag = -1
        self.referenceType = None
        self._get_reference_type()

        # self.classID = -1
        # self._get_class_id()

    def _get_reference_type(self):
        ret = self.vm.command('OBJ_ReferenceType', object=self.objectID)
        self.refTypeTag = ret['refTypeTag']
        typeID = ret['typeID']
        if self.refTypeTag == TypeTag.CLASS:
            self.referenceType = ClassType(self.vm, typeID)
        elif self.refTypeTag == TypeTag.INTERFACE:
            self.referenceType = InterfaceType(self.vm, typeID)
        elif self.refTypeTag == TypeTag.ARRAY:
            self.referenceType = ArrayType(self.vm, typeID)
        else:
            raise Exception("Unknown Type Tag %d", self.refTypeTag)

    # def _get_class_id(self):
    #     ret = self.vm.command('REF_ClassObject', refType=self.referenceType.referenceTypeID)
    #     self.classID = ret['classObject']

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError as e:
            methods_dict = self.referenceType.get_methodInfo(__name)
            if methods_dict:
                def _ref_method(thread_id, *arg):
                    pysig = self.vm.type_to_pysig(arg)
                    ret = self.vm.command('OBJ_InvokeMethod',
                                          object=self.objectID,
                                          thread=thread_id,
                                          clazz=self.referenceType.referenceTypeID,
                                          methodID=methods_dict[pysig]['methodID'],
                                          options=0,
                                          arguments=len(arg),
                                          arguments_list=[{'arg': self.vm.box_value(i)} for i in arg])
                    # TODO exception handling
                    ret_exception = ret['exception']

                    return self.vm.unbox_value(ret['returnValue'])
                return _ref_method
            raise e


class StringReference(ObjectReference):
    def __init__(self, vm: JDWPVM, objID: int) -> None:
        super().__init__(vm, objID)

    def value(self) -> str:
        return self.vm.string_val(self.objectID)


if __name__ == "__main__":
    package_name = ""
    host = "127.0.0.1"
    jdwp_port = "8888"

    # subprocess.check_call(['python', "jdwp-shellifier.py",
    #     "--target", "127.0.0.1",
    #     "--port", str(client_port),
    #     "--break-on", "android.app.Activity.onResume",#"android.app.LoadedApk.makeApplication",
    #     "--loadlib", soname])

    jdwp = JDWPVM()
    jdwp.connect()

    request_id = jdwp.set_break_at_method("android.app.Activity.onResume")
    #request_id = jdwp.set_break_at_method("android.app.Activity.onPause")
    jdwp.vm_resume()

    def _break_remove(event):
        activity_thread = jdwp.get_class("Landroid/app/ActivityThread;")
        pack_id = activity_thread.currentPackageName(event.thread)
        info('pakid is %s' % pack_id)
        return True

    def exec_cmd(event):
        jdwp.clear_event(EventKind.BREAKPOINT, event.requestID)
        cmd = " "
        runtime_class = jdwp.get_class("Ljava/lang/Runtime;")
        runtimeInst = runtime_class.getRuntime(event.thread)
        ret = runtimeInst.equals(event.thread, cmd)
        ret = runtimeInst.exec(event.thread, cmd)
        ret = runtimeInst.freeMemory(event.thread, cmd)
        return False

    #jdwp.register_for_event(EventKind.BREAKPOINT, _break_remove)
    jdwp.register_for_event(EventKind.BREAKPOINT, exec_cmd)

    while True:
        sus_policy, event_list = jdwp.wait_for_event()

    jdwp.clear_event(EventKind.BREAKPOINT, request_id)
