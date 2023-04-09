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

BASE_SPEED=15
Kp=0.1
Ki=0.0015
Kd=0.2
target_red=46
target_white=288
target=(170+25)/2

def delivery_protocol(degrees):
    DELIVERY_MOTOR.set_position(degrees)
    sleep(2)
    PUSHING_MOTOR.set_position(130)
    sleep(0.5)
    PUSHING_MOTOR.set_position(-30)
    sleep(0.5)
    DELIVERY_MOTOR.set_position(0)
    
def delivery(color):
    
    if color == 1:
        delivery_protocol(-125)
    elif color == 2:
        delivery_protocol(-210)
    elif color == 3:
        delivery_protocol(-490)
    elif color == 4:
        delivery_protocol(-390)
    elif color == 5:
        delivery_protocol(-570)
    elif color == 6:
        delivery_protocol(-300)
        
def backwards_PID(left_motor,right_motor,greens):
    integral=0
    derivative=0
    last_error=0
    value=LINE_SENSOR.get_value()
    while value == None or value ==[0,0,0,0]:
        value=LINE_SENSOR.get_value()
        print(value)
    if color_choosing(value[:-1])==4:
        while color_choosing(value[:-1])==4:
            if color_choosing(COLOR_SENSOR.get_value()[:-1])!=7:
                left_motor.set_power(5)
                right_motor.set_power(5)
                sleep(0.5)
                left_motor.set_power(0)
                right_motor.set_power(0)
                delivery(color_choosing(COLOR_SENSOR.get_value()[:-1]))
                sleep(0.5)
                left_motor.set_power(5)
                right_motor.set_power(5)
                print('color')
            left_motor.set_power(10)
            right_motor.set_power(10)
            print('green detected')
            value=LINE_SENSOR.get_value()
            while value == None or value ==[0,0,0,0]:
                value=LINE_SENSOR.get_value()

                         
    value_b=value[2]
    error=value_b-target
    integral+=error
    derivative=error-last_error
    turn_rate=Kp*error+Ki*integral+Kd*derivative

    left_motor.set_power((BASE_SPEED-turn_rate)*-1)
    right_motor.set_power((BASE_SPEED+turn_rate)*-1)
    return greens

if __name__ == "__main__":
    try:
        green_detected=0
        while True:
            green_detected=backwards_PID(LEFT_MOTOR,RIGHT_MOTOR,green_detected)
            if green_detected ==6:
                sleep(1)
                LEFT_MOTOR.set_power(0)
                RIGHT_MOTOR.set_power(0)
                sleep(0.5)
                #LEFT_MOTOR.set_position_relative(900)
                #RIGHT_MOTOR.set_position_relative(-900)
                sleep(0.1)
                #LEFT_MOTOR.set_power(0)
                #RIGHT_MOTOR.set_power(0)
                break
            print(green_detected)
            #print(LINE_SENSOR.get_value())
    except BaseException:
        print ("Done with the program")
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        reset_brick()
        exit()
