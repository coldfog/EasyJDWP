import socket
import struct
import subprocess
import protocol_defs
from protocol_defs import EventKind, ModKind, SuspendPolicy, TypeTag, cmd_def
from protocol_defs import pack_defs
from protocol_defs import tag_def

import logging
from logging import debug, info, warning, error
from sys import flags
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


class COMM:
    HANDSHAKE = b"JDWP-Handshake"
    CMD_FLAG = 0x00
    REPLY_FLAG = 0x80


class MetaObj:
    def __getattribute__(self, __name):
        pass

    def __setattr__(self, __name, __value):
        pass


class MetaClass(MetaObj):

    def __init__(self, jdwp, ref_info):
        self.class_info = ref_info
        self._methods = {}
        self._field = {}
        self._jdwp = jdwp

    def new(self):
        pass


class JDWP:
    PLATFORM_ANDROID = 1
    HEADER_SIZE = 11

    def __init__(self, platform=PLATFORM_ANDROID) -> None:
        # TODO Add evironment check like adb
        self.port = 0
        self.host = ""
        self.platform = platform
        self.id = 1
        self.target_id = -1;
        self.fieldIDSize = -1
        self.methodIDSize = -1
        self.objectIDSize = -1
        self.referenceTypeIDSize = -1
        self.frameIDSize = -1
        self._classes = {}

    def connect(self, host="127.0.0.1", port=8700):
        if self.platform == JDWP.PLATFORM_ANDROID:
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

    def _path_parse(self, s):
        i = s.rfind('.')
        if i == -1:
            raise Exception('Cannot parse path')
        return 'L' + s[:i].replace('.', '/') + ';', s[i:][1:]

    def set_break_at_method(self, method_sig):
        class_name, method_name = self._path_parse(method_sig)
        cls_info = self.get_class(class_name)
        method_info = cls_info['methods'][method_name]

        ret = self.command('EVT_Set',
                     eventKind=EventKind.BREAKPOINT,
                     suspendPolicy=SuspendPolicy.ALL,
                     modifiers=1,
                     modifiers_list=[
                         dict(
                             modKind=ModKind.LocationOnly,
                             loc=(
                                 TypeTag.CLASS, cls_info['typeID'], method_info['methodID'], 0)
                         )
                     ]
                     )
        requestID = ret['requestID']
        info('Set break point at %s, requestID: %d'% (method_sig, requestID))
        return requestID

    def _get_all_classes(self):
        ret_data = self.command('VM_AllClasses')
        for data in ret_data['classes_list']:
            self._classes[data['signature']] = data

    def get_class(self, name):
        ref_info = self._classes[name]
        if 'methods' not in ref_info:
            ref_info['methods'] = {}
            method_arr = self.command(
                'REF_Methods', refType=ref_info['typeID'])['declared_list']
            for method_info in method_arr:
                ref_info['methods'][method_info['name']] = method_info


        return ref_info

    def get_version(self):
        ret_data = self.command('VM_Version')

        for k in ret_data:
            info("%s: %s" % (k, ret_data[k]))

    def _handshake(self):
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

    def _recv_cmd(self):
        header = self.socket.recv(JDWP.HEADER_SIZE)
        pkt_len, id, flags, cmd_set, cmd = struct.unpack('>IIBBB', header)

        self.target_id = id
        data_len = pkt_len - JDWP.HEADER_SIZE
        cmd_sig = (cmd, cmd_set)

        data = b''
        while len(data) < data_len:
            left_size = data_len - len(data)
            data += self.socket.recv(1024 if left_size > 1024 else left_size)

        return data, cmd_sig, id

    def _send_cmd_reply(self, target_id, errorcode, data):
        flags = COMM.REPLY_FLAG
        pkt_len = len(data) + JDWP.HEADER_SIZE
        pkt_id = target_id
        pkt = struct.pack('>IIBH', pkt_len, pkt_id, flags, errorcode)
        self.socket.sendall(pkt+data)


    def _send_cmd(self, cmd_sig, data=b''):
        flags = COMM.CMD_FLAG
        cmd, cmd_set = cmd_sig
        pkt_len = len(data) + JDWP.HEADER_SIZE
        pkt_id = self.id
        pkt = struct.pack(">IIBBB%ds" % len(data), pkt_len,
                          pkt_id, flags, cmd_set, cmd, data)
        self.id += 2
        self.socket.sendall(pkt)
        return pkt_id

    def _recv_cmd_reply(self, pkt_id):
        header = self.socket.recv(JDWP.HEADER_SIZE)
        pkt_len, id, flags, errcode = struct.unpack('>IIBH', header)
        # TODO Error handling
        if errcode != 0:
            raise Exception('Error! code:%d' %errcode)
        assert flags == COMM.REPLY_FLAG, "Reply Flag is not correct!"
        assert pkt_id == id, "Reply packet is not for sending"
        data_len = pkt_len - JDWP.HEADER_SIZE

        data = b''
        while len(data) < data_len:
            left_size = data_len - len(data)
            data += self.socket.recv(1024 if left_size > 1024 else left_size)

        return data

    def _pack_data(self, data_sig, data_dict):
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

    def _unpack_data(self, data_sig, data):
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

    def command(self, cmd_name, **kwargs):
        cmd = cmd_def[cmd_name]
        data, _ = self._pack_data(cmd['cmd'], kwargs)
        pack_id = self._send_cmd(cmd['sig'], data)

        reply_data = self._recv_cmd_reply(pack_id)
        data, _ = self._unpack_data(cmd['reply'], reply_data)
        return data

    def _set_id_size(self):
        ret_data = jdwp.command('VM_IDSizes')
        debug('idsize: ' + repr(ret_data))
        for k in ret_data:
            setattr(self, k, ret_data[k])

        protocol_defs.init_IDSIze(ret_data)
        global pack_defs
        pack_defs = protocol_defs.pack_defs

    def vm_resume(self):
        ret = self.command('VM_Resume')
        info('VM Resumed')

    def wait_for_event(self):
        cmd = cmd_def['EVTSET_Composite']

        data, sig, cmd_id = self._recv_cmd()
        assert sig == cmd['sig'], 'Not Event cmd!'

        ret, size = self._unpack_data(cmd['cmd'], data)
        sus_policy = ret['suspendPolicy']
        event_num = ret['events']
        event_list = ret['events_list']
        events = []
        for event_attr in event_list:
            events.append(Event(event_attr))
        return sus_policy, events
    
class Event:
    def __init__(self, event_attr):
        self.eventKind = event_attr['eventKind']
        event_val = event_attr['eventKind_val']
        for k in event_val:
            self.__setattr__(k, event_val[k])

if __name__ == "__main__":
    package_name = ""
    host = "127.0.0.1"
    jdwp_port = "8888"

    # subprocess.check_call(['python', "jdwp-shellifier.py",
    #     "--target", "127.0.0.1",
    #     "--port", str(client_port),
    #     "--break-on", "android.app.Activity.onResume",#"android.app.LoadedApk.makeApplication",
    #     "--loadlib", soname])

    jdwp = JDWP()
    jdwp.connect()

    runtime_class = jdwp.get_class("Ljava/lang/Runtime;")
    request_id = jdwp.set_break_at_method("android.app.Activity.onResume")
    jdwp.vm_resume()
    sus_policy, event_list = jdwp.wait_for_event()
    for event in event_list:
        if event.eventKind == EventKind.BREAKPOINT:
            info(event)
    info(ret)
