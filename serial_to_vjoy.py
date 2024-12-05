import serial
import pyvjoy

"""
    Read serial port data incoming from arduino UNO, interpret it and set to virtual joystick
"""

arduino = serial.Serial('COM6', 9600, timeout=1)

joystick = pyvjoy.VJoyDevice(1)
JOYSTICK_AXIS_RANGE = 32767

def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

while True:
    try:
        # Get serial data from arduino
        data = arduino.readline().decode('utf-8').strip().split(";")
        wheel_value = int(data[0])
        accelerator_value = int(data[1])
        brake = int(data[2])

        if data:
            # map the pot wheel value adjusting it to joystick axis range, then set RX and RY values
            x_axis_value = map_value(wheel_value, 0, 1023, 1, JOYSTICK_AXIS_RANGE)
            y_axis_value = JOYSTICK_AXIS_RANGE - x_axis_value

            joystick.set_axis(pyvjoy.HID_USAGE_RX, x_axis_value)
            joystick.set_axis(pyvjoy.HID_USAGE_RY, y_axis_value) 

            # set X value for accelerator
            accelerator_axis_value = map_value(accelerator_value, 0, 1023, 1, JOYSTICK_AXIS_RANGE)
            joystick.set_axis(pyvjoy.HID_USAGE_X, accelerator_axis_value)
   
            # map the virtual buttons
            joystick.set_button(1, brake > 0)

            # debug info
            print(f"| Wheel: {x_axis_value} Accel: { accelerator_value } | Break: {brake} | ")

    except ValueError:
        pass
    except KeyboardInterrupt:
        print("Exiting...")
        break
