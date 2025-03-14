import serial
import time


with open("config_output.txt", "w") as output:
    with open("PtpGmNtpServer.ucm", "r") as conf:

        ser = serial.Serial('/dev/ttyUSB0', 1000000, timeout=1)

        for line in conf:
            if ser.is_open:
                line = line.strip('\n')
                print(line)
                ser.write(bytes(line+'\r\n', 'utf-8'))
                time.sleep(0.01)
                response = ser.read_all()

                if "$ER" in str(response):
                    input()
                    break

                output.write(line+'\n')
                output.write(str(response)+'\n')
