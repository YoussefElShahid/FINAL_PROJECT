from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick, Motor, EV3ColorSensor
from time import sleep
from RGB import color_choosing
from RGB_LINE import color_choosing_LINE
import traceback

# Initialize sensors and motors
wait_ready_sensors(True)
LEFT_MOTOR = Motor('A')
RIGHT_MOTOR = Motor('D')
DELIVERY_MOTOR = Motor('C')
PUSHING_MOTOR = Motor('B')
LINE_SENSOR = EV3ColorSensor(1)
COLOR_SENSOR = EV3ColorSensor(2)
TOUCH_SENSOR = TouchSensor(4)

# Set motor limits
LEFT_MOTOR.set_limits(dps=500)
RIGHT_MOTOR.set_limits(dps=500)
PUSHING_MOTOR.set_limits(dps=270)
DELIVERY_MOTOR.set_limits(dps=300)

# PID control parameters
TARGET = (32 + 289) / 2
Kp = 0.08
Ki = 0.05
Kd = 0.01

# Get valid sensor value
def real_value(sensor):
    value = sensor.get_value()
    while value == None or value == [0, 0, 0, 0]:
        value = sensor.get_value()
    return value

# PID control function
def PID(value, sign, base_speed, integral, derivative, last_error):
    value_b = value[0]
    error = value_b - TARGET
    integral += error
    derivative = error - last_error
    turn_rate = Kp * error + Ki * integral + Kd * derivative

    color = color_choosing(value[:-1])
    if color == 1:
        LEFT_MOTOR.set_power(-24)
        RIGHT_MOTOR.set_power(0)
    elif color == 6:
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
    else:
        LEFT_MOTOR.set_power((base_speed + (sign * turn_rate)) * -1)
        RIGHT_MOTOR.set_power((base_speed - (sign * turn_rate)) * -1)

    return [integral, derivative, last_error]

# Perform delivery based on color
def delivery(color):
    degree_map = {
        1: -30,
        2: -130,
        3: -390,
        4: -305,
        5: -480,
        6: -210,
    }
    if color in degree_map:
        delivery_protocol(degree_map[color])

# Delivery protocol
def delivery_protocol(degrees):
    DELIVERY_MOTOR.set_position_relative(degrees)
    sleep(2)
    PUSHING_MOTOR.set_position(120)
    sleep(1.5)
    PUSHING_MOTOR.set_position(0)
    sleep(1.5)
    DELIVERY_MOTOR.set_power(35)
    sleep(2)
    DELIVERY_MOTOR.set_power(0)

# Move robot backwards
def backwards():
    base_speed = 15
    value = real_value(LINE_SENSOR)
    col = real_value(COLOR_SENSOR)
    LEFT_MOTOR.set_power(-base_speed)
    RIGHT_MOTOR.set_power(-base_speed)
    while True:
        color_line = color_choosing_LINE(value[:-1])
        if color_line == 1:
            LEFT_MOTOR.set_power((base_speed + 25) * -1)
            RIGHT_MOTOR.set_power((base_speed - 5) * -1)
        elif color_line == 3:
            LEFT_MOTOR.set_power(-(base_speed - 5))
            RIGHT_MOTOR.set_power((base_speed + 25) * -1)
        elif color_line == 4:
            break
        else:
            LEFT_MOTOR.set_power(-base_speed)
            RIGHT_MOTOR.set_power(-base_speed)
        value = real_value(LINE_SENSOR)

    detected_color = color_choosing(col[:-1])
    if detected_color != 7 and detected_color not in deliveries_done:
        deliveries_done.append(detected_color)
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        sleep(0.2)
        LEFT_MOTOR.set_position_relative(-200)
        RIGHT_MOTOR.set_position_relative(-200)
        sleep(0.2)
        delivery(detected_color)
        sleep(0.2)

# Main function
if __name__ == "__main__":
    try:
        deliveries_done = []
        while True:
            backwards()
    except BaseException as e:
        print("Done with the program")
        print(e)
        print(traceback.format_exc())
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        reset_brick()
        exit()
