
import serial
import time
import click

connect_command = '$CC'

def calculate_checksum(packet: str) -> int:
    print("check sum of: ", packet)
    checksum = 0
    for c in packet[1:]: # don't use the $
        if c == '*':
            break
        checksum = checksum ^ ord(c)
    return f"{checksum:0{2}x}"


def get_checksum(packet: str) -> str:
    return packet.split('*')[-1]

def fmt_rsp(response: bytes) -> str:
    return response.decode("utf-8").removesuffix('\r\n')

def fmt_pkt(cmd_addr_data: str) -> bytes: 
    return bytes(cmd_addr_data + '*' + calculate_checksum(cmd_addr_data) + '\r\n', 'utf-8')


def mk_pkt(cmd: str, addr='', data='') -> int:
    if addr == '':
        return fmt_pkt(cmd)
    elif data == '':
        return fmt_pkt(cmd+','+addr)
    else:
        return fmt_pkt(cmd+','+addr+','+data)


def detect_baudrate(file_descriptor) -> int:
    rates = [2000000, 1000000, 500000, 460800, 115200]
    packet = fmt_pkt(connect_command)
    for rate in rates:

        ser = serial.Serial(file_descriptor, rate, timeout=0.1, exclusive=True)
        ser.flush()
        wc = ser.write(packet)
        wr = ser.read(32)
        ser.close()

        if '$' not in str(wr):
            continue
        else:
            print('baud rate: ', rate)
            return rate

def check_response(packet: str) -> int:
    if get_checksum(packet) != calculate_checksum(packet):

        print("not the right check sum?")
        return -1
    else:
        return 0

#def test_connection(ser):
#    
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


#def simple_write_read(cmd):
#    
#    ser = serial.Serial('/dev/ttyUSB0', 1000000, timeout=0.1, exclusive=True)
#    if ser.is_open:
#        print("to write: ", make_packet(cmd))
#        ser.write(make_packet(cmd))
#        response = ser.read(32)
#        print("received: ", response)
#        ser.close()
#
#cmd1 = connect_command
#cmd2 = "$WC,0xB0020000,0x00000000" # ntp disable
#cmd3 = "$WC,0xB0020000,0x00000001" # ntp enable
#
#cmds = [connect_command, cmd2]
#for cmd in cmds:
#    simple_write_read(cmd)
#    print()
#    print()





    

def read_reg(addr: str, data = '0x00000000') -> int:

    command = '$RC' # when you read register you always use this command
    file_descriptor = "/dev/ttyUSB0" # entered from cmd line? something like:  $ nts read /dev/ttyUSB0 config
    timeout = 0.1
    baudrate = detect_baudrate(file_descriptor)

    ser = serial.Serial(file_descriptor, baudrate, timeout=timeout, exclusive=True)
    ser.write(mk_pkt(command, addr, ''))
    response = ser.read(64)
    print(response)
    if check_response(fmt_rsp(response)) > 0:

        ser.close()
        print(response)
    # ser = serial.Serial(file_descriptor, baud_rate, timeout, excluseive=True)

    # init vars
    # lock port
    # append command
    # append addr
    # calculate check sum
    # append *
    # append checksum
    # append /r
    # append /n
    # write serial
    # check write success
    # check response
    # read serial
    # check data
    # convert to normal str
    # calculate checksum
    # unlock port
    return 0
# def write_reg(addr: int, data: int) -> int:


print(read_reg('0xB0020000', '0x00000000'))


