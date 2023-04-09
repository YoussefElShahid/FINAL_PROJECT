from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick,Motor,EV3ColorSensor
from time import sleep, time
from math import sqrt
from RGB import color_choosing
wait_ready_sensors(True)

LEFT_MOTOR = Motor('A')
RIGHT_MOTOR = Motor('D')
DELIVERY_MOTOR = Motor('C')
PUSHING_MOTOR = Motor('B')

LINE_SENSOR=EV3ColorSensor(1)
COLOR_SENSOR=EV3ColorSensor(2)
TOUCH_SENSOR=TouchSensor(4)
BASE_SPEED=20
DELIVERY_MOTOR.set_limits(dps = 300)
PUSHING_MOTOR.set_limits(dps = 270)
        
        
        
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
    
def delivery(color):
    if color == 1:
        delivery_protocol(-50)
    elif color == 2:
        delivery_protocol(-130)
    elif color == 3:
        delivery_protocol(-420)
    elif color == 4:
        delivery_protocol(-320)
    elif color == 5:
        delivery_protocol(-510)
    elif color == 6:
        delivery_protocol(-225)
        
def run():
    try:
        while True:
            if TOUCH_SENSOR.is_pressed():
                color = int(input('What is the color?'))
                delivery(color)
                sleep(0.5)
    except BaseException:
        print ("Done with the program")
        reset_brick()
        exit()


if __name__ == "__main__":
    try:
        run()
    except BaseException:
        print ("Done with the program")
        reset_brick()
        exit()