import socket
import struct
import subprocess
from protocol_defs import cmd_def

import logging
from logging import debug, info, warning, error
from sys import flags
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


class COMM:
    HANDSHAKE = b"JDWP-Handshake"
    CMD_FLAG = 0x00
    REPLY_FLAG = 0x80



class JDWP:
    PLATFORM_ANDROID = 1
    HEADER_SIZE = 11

    def __init__(self, platform=PLATFORM_ANDROID) -> None:
        # TODO Add evironment check like adb
        self.port = 0
        self.host = ""
        self.platform = platform
        self.id = 1

    def connect(self, host="127.0.0.1", port=8700):
        if self.platform == JDWP.PLATFORM_ANDROID:
            subprocess.run(['adb.exe', 'shell', 'am', 'set-debug-app',
                        '-w', package_name], stdout=subprocess.DEVNULL)
            subprocess.run(['adb.exe', 'shell', 'monkey', '-p', package_name, '-c',
                        'android.intent.category.LAUNCHER 1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            info("Setup %s in debug mode" % package_name)

            try:
                # adb jdwp will not finish by itself
                subprocess.run('adb jdwp', timeout=1, capture_output=True)
            except subprocess.TimeoutExpired as e:
                jdwp_port = int(e.output)

            subprocess.run(['adb', 'forward', 'tcp:%d' %
                        port, 'jdwp:%d' % jdwp_port])
            info("bind jdwp into %s:%d (JDWP port: %d)" % (host, port, jdwp_port))

        self.port = port
        self.jdwp_port = jdwp_port
        self.host = host

        info("Start handshake")
        self._handshake()
        info("Handshake Success")

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

    def _set_id_size(self):
        pass

    def _send_cmd(self, cmd_sig, data=b''):
        flags = COMM.CMD_FLAG
        cmd, cmd_set = cmd_sig
        pkt_len = len(data) + JDWP.HEADER_SIZE
        pkt = struct.pack(">IIBBB%ds" % len(data), pkt_len, self.id, flags, cmd_set, cmd, data)
        self.id += 2
        self.socket.sendall(pkt)

    def _reply_cmd(self):
        header = self.socket.recv(JDWP.HEADER_SIZE)
        pkt_len, id, flags, errcode = struct.unpack('>IIBH', header)
        assert flags == COMM.REPLY_FLAG, "Reply Flag is not correct!"
        data_len = pkt_len - JDWP.HEADER_SIZE

        data = b''
        while len(data) < data_len:
            left_size = data_len - len(data)
            data += self.socket.recv(1024 if left_size > 1024 else left_size)

        return data

    def _pack_data(self, data_sig, data_dict):
        pack_format = ">"
        pack_data = []
        for val_name, val_type in data_sig:
            pack_format += val_type
            pack_data.append(data_dict[val_name])

        return struct.pack(pack_format, *pack_data)

    def _unpack_data(self, data_sig, data):
        pack_format = ">"
        pack_name = []
        for val_name, val_type in data_sig:
            pack_format += val_type
            pack_name.append(val_name)

        data_arr = struct.unpack(pack_format, data)
        data_dict = {}
        for name, val in zip(pack_name, data_arr):
            data_dict[name] = val
        return data_dict

    def command(self, cmd_name, callback, **kwargs):
        cmd = cmd_def[cmd_name]
        data = self._pack_data(cmd['cmd'], kwargs)
        self._send_cmd(cmd['sig'], data)

        reply_data = self._reply_cmd()
        return self._unpack_data(cmd['reply'], reply_data)




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
    debug(jdwp.command('IDSizes', lambda x:x))
