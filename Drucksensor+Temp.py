import smbus
import time

# AMS5812 I2C address is 0x78(120)
addr = 0x3C

# Create I2C bus
bus = smbus.SMBus(1)

def convert_to_float(msb, lsb):
    value = (msb << 8) + lsb
    if value >= 32768:
        value = value - 65536
    return value

def read_sensor_data():
    # Request 4 bytes of data
    data = bus.read_i2c_block_data(addr, 0, 4)

    # Convert the data
    pressure = convert_to_float(data[0], data[1])
    temp = convert_to_float(data[2], data[3])

    pressure = ((pressure - 3277.0) / ((26214.0) / 30.0)) - 15.0
    c_temp = ((temp - 3277.0) / ((26214.0) / 110.0)) - 25.0
    f_temp = (c_temp * 1.8) + 32

    return pressure, c_temp, f_temp

def main():
    try:
        while True:
            pressure, c_temp, f_temp = read_sensor_data()

            # Output data
            print("Pressure: {} PSI".format(pressure))
            print("Temperature in Celsius: {} C".format(c_temp))
            print("Temperature in Fahrenheit: {} F".format(f_temp))
            print()

            time.sleep(0.5)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
