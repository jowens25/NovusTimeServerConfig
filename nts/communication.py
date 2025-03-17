
import serial
import time
import click
import json


# okay a note for you
# write commands and read responses carry data


# packet is a set of bytes
# a string is the parsed bytes

# connect_command = '$CC'
#
#

#
#
# def get_checksum(packet: str) -> str:
#    return packet.split('*')[-1]
#
#
# def str_to_pkt(cmd: str, addr='', data='') -> bytes:
#
#    if addr != '' and data != '':
#        pkt = cmd+','+addr+','+data
#
#    if
#
#    if addr == '':
#        pkt = cmd
#    elif addr == '' and data == '':
#
#        return bytes(cmd + '*' + calculate_checksum(cmd) + '\r\n', 'utf-8')
#         return bytes(cmd + '*' + calculate_checksum(cmd) + '\r\n', 'utf-8')
#
#
# def pkt_to_str(packet: bytes) -> str:
#    return packet.decode("utf-8").removesuffix('\r\n')


# def detect_baudrate(file_descriptor) -> int: str_to_pkt
#  rates = [2000000, 1000000, 500000, 460800, 115200]
#   packet = (connect_command)
#    for rate in rates:
#
#         ser = serial.Serial(file_descriptor, rate, timeout=0.1, exclusive=True)
#         ser.flush()
#         wc = ser.write('$CC')
#         wr = ser.read(32)
#         ser.close()
#
#         if '$' not in str(wr):
#             continue
#         else:
#             print('baud rate: ', rate)
#             return rate
#     print("no device found? ")
# # def check_response(packet: str) -> int:
#    if get_checksum(packet) == calculate_checksum(packet):
#        print("checksum pass")
#        return 0
#    else:
#        return -1

# def test_connection(ser):
#    print
#    data_len = ser.write(make_packet(connect_command))
#
#    if data_len == -1:
#        ser.close()
#        print('write failed')
#        return -1
#    elif data_len != len(make_packet(connect_command)):
#        ser.close()
#        print("write incomplete")
#        return -1
#    try:
#        ser.read(64)
#    except serial.SerialException as e:
#        print("timed out???")
#        return -1


# def simple_write_read(cmd):
#
#    ser = serial.Serial('/dev/ttyUSB0', 1000000, timeout=0.1, exclusive=True)
#    if ser.is_open:
#        print("to write: ", make_packet(cmd))
#        ser.write(make_packet(cmd))
#        response = ser.read(32)
#        print("received: ", response)
#        ser.close()
#
# cmd1 = connect_command
# cmd2 = "$WC,0xB0020000,0x00000000" # ntp disable
# cmd3 = "$WC,0xB0020000,0x00000001" # ntp enable
#
# cmds = [connect_command, cmd2]
# for cmd in cmds:
#    simple_write_read(cmd)
#    print()
#    print()

# def parse_error(err: str) -> int:
#     print(err)
#
#
# def dpk_wrt_rsp(rsp: bytes) -> str:
#     rsp = rsp.decode("utf-8").removesuffix('\r\n')
#     msg, checksum = rsp.split('*')
#     parts = msg.split(',')
#     cmd = parts[0]
#     addr = parts[1]
#
#     if cmd == '$WR':
#         return cmd, addr
#     elif cmd == '$RR':
#         return cmd, addr, parts[2]


# def check_write_response(rsp) -> int:
#
#    cmd, data = dpk_wrt_rsp(rsp)
#
#    if cmd == '$WR':
#        print("WR")
#        print(cmd, data)
#
#    elif cmd == '$ER':
#        parse_error(rsp)
#        print(cmd, data)
#        return -1
#
#    else:
#        print("command not known")
#        return -1


# def write_reg(addr: str, data='0x00000000') -> int:
#    command = '$WC'
#    file_descriptor = "/dev/ttyUSB0"
#    timeout = 0.1
#    baudrate = detect_baudrate(file_descriptor)
#
#    ser = serial.Serial(file_descriptor, baudrate,
#                        timeout=timeout, exclusive=True)
#
#    ser.write(str_to_pkt(command, addr))
#    response = pkt_to_str(ser.read(32))
#    ser.close()
#    print(response)


def calculate_checksum(packet: str) -> int:
    '''calculate check sum of command and address str'''
    # print("check sum of: ", packet)
    checksum = 0
    for c in packet[1:]:  # don't use the $
        if c == '*':
            break
        checksum = checksum ^ ord(c)
    return f"{checksum:0{2}x}"


def int_to_hex_str_8(addr: int) -> str:
    return f"0x{addr:08x}"


def prepend_read_cmd(addr: str) -> str:
    cmd = '$RC'
    return cmd+','+addr


def append_cr_lf(cmd_addr: str) -> str:
    cr_lf = '\r\n'
    return cmd_addr + cr_lf


def str_to_bytes(cmd_addr: str) -> bytes:
    return bytes(cmd_addr, 'utf-8')


def int_addr_to_read_packet(addr: int) -> bytes:
    return str_to_bytes(append_cr_lf(
        prepend_read_cmd(int_to_hex_str_8(addr))))


def read_reg(addr: int) -> int:
    # entered from cmd line? something like:  $ nts read /dev/ttyUSB0 config
    file_descriptor = "/dev/ttyUSB0"
    timeout = 0.01
    # baudrate = detect_baudrate(file_descriptor)

    ser = serial.Serial(file_descriptor, 1000000,
                        timeout=timeout, exclusive=True)

    packet = int_addr_to_read_packet(addr)
    print(packet)
    ser.write(packet)
    response = ser.read(32)
    ser.close()
    print(response)
    response = response.decode(
        "utf-8").removesuffix('\r\n').split(',')[2].split('*')[0]

    return int(response, 16)


def read_config() -> int:

    for i in range(256):
        TempConfig = {}
        response = read_reg(
            (0x00000000 + ((i * Ucm_Config_BlockSize) + Ucm_Config_TypeInstanceReg)))
        if (True):

            if ((i == 0) and
                    ((((response >> 16) & 0x0000FFFF) != Ucm_CoreConfig_ConfSlaveCoreType) or
                     (((response >> 0) & 0x0000FFFF) != 1))):

                print("not a conf block at the address expected")
                break

            elif (response == 0):
                break

            else:

                TempConfig["type"] = cores.get(
                    str(((response >> 16) & 0x0000FFFF)))
                TempConfig["core_type"] = ((response >> 16) & 0x0000FFFF)
                TempConfig["core_instance_nr"] = ((response >> 0) & 0x0000FFFF)

        else:
            break

        response = read_reg(
            (0x00000000 + ((i * Ucm_Config_BlockSize) + Ucm_Config_BaseAddrLReg)))
        if (True):
            TempConfig["address_range_low"] = response

        else:
            break

        response = read_reg(
            (0x00000000 + ((i * Ucm_Config_BlockSize) + Ucm_Config_BaseAddrHReg)))
        if (True):
            TempConfig["address_range_high"] = response

        else:
            break

        response = read_reg(
            (0x00000000 + ((i * Ucm_Config_BlockSize) + Ucm_Config_IrqMaskReg)))
        if (True):
            TempConfig["interrupt_mask"] = response

        else:
            break

        CoreConfig[i] = TempConfig

    return 0

    # nts enable ntp does something like this


Ucm_Config_BlockSize = 16
Ucm_Config_TypeInstanceReg = 0x00000000
Ucm_Config_BaseAddrLReg = 0x00000004
Ucm_Config_BaseAddrHReg = 0x00000008
Ucm_Config_IrqMaskReg = 0x0000000C

# first high = 268435455
# first low  = 0
Ucm_CoreConfig_ConfSlaveCoreType = 1
core_types = {}
core_types["Ucm_CoreConfig_ConfSlaveCoreType"] = Ucm_CoreConfig_ConfSlaveCoreType
core_types["Ucm_CoreConfig_ClkClockCoreType"] = 2
core_types["Ucm_CoreConfig_ClkSignalGeneratorCoreType"] = 3
core_types["Ucm_CoreConfig_ClkSignalTimestamperCoreType"] = 4
core_types["Ucm_CoreConfig_IrigSlaveCoreType"] = 5
core_types["Ucm_CoreConfig_IrigMasterCoreType"] = 6
core_types["Ucm_CoreConfig_PpsSlaveCoreType"] = 7
core_types["Ucm_CoreConfig_PpsMasterCoreType"] = 8
core_types["Ucm_CoreConfig_PtpOrdinaryClockCoreType"] = 9
core_types["Ucm_CoreConfig_PtpTransparentClockCoreType"] = 10
core_types["Ucm_CoreConfig_PtpHybridClockCoreType"] = 11
core_types["Ucm_CoreConfig_RedHsrPrpCoreType"] = 12
core_types["Ucm_CoreConfig_RtcSlaveCoreType"] = 13
core_types["Ucm_CoreConfig_RtcMasterCoreType"] = 14
core_types["Ucm_CoreConfig_TodSlaveCoreType"] = 15
core_types["Ucm_CoreConfig_TodMasterCoreType"] = 16
core_types["Ucm_CoreConfig_TapSlaveCoreType"] = 17
core_types["Ucm_CoreConfig_DcfSlaveCoreType"] = 18
core_types["Ucm_CoreConfig_DcfMasterCoreType"] = 19
core_types["Ucm_CoreConfig_RedTsnCoreType"] = 20
core_types["Ucm_CoreConfig_TsnIicCoreType"] = 21
core_types["Ucm_CoreConfig_NtpServerCoreType"] = 22
core_types["Ucm_CoreConfig_NtpClientCoreType"] = 23
core_types["Ucm_CoreConfig_ClkFrequencyGeneratorCoreType"] = 25
core_types["Ucm_CoreConfig_SynceNodeCoreType"] = 26
core_types["Ucm_CoreConfig_PpsClkToPpsCoreType"] = 27
core_types["Ucm_CoreConfig_PtpServerCoreType"] = 28
core_types["Ucm_CoreConfig_PtpClientCoreType"] = 29
core_types["Ucm_CoreConfig_PhyConfigurationCoreType"] = 10000
core_types["Ucm_CoreConfig_I2cConfigurationCoreType"] = 10001
core_types["Ucm_CoreConfig_IoConfigurationCoreType"] = 10002
core_types["Ucm_CoreConfig_EthernetTestplatformType"] = 10003
core_types["Ucm_CoreConfig_MinSwitchCoreType"] = 10004
core_types["Ucm_CoreConfig_ConfExtCoreType"] = 20000

cores = {}

for k, v in core_types.items():
    cores[str(v)] = k

CoreConfig = {}

print(read_config())

with open('config.json', 'w') as cfg:
    json.dump(CoreConfig, cfg)
    cfg.close()
    print(CoreConfig)

# cmd  | data
# -----------
# CC   | 0  |
# WC   | 1  |
# WR   | 0  |
# RC   | 0  |
# RR   | 1  |

# cmds lead to responses
# CC -> CR or ER or None
# WC -> WR or ER or None
