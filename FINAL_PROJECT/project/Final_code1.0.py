from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick,Motor,EV3ColorSensor
from time import sleep, time
from math import sqrt
from RGB import color_choosing
import traceback
wait_ready_sensors(True)

LEFT_MOTOR = Motor('A')
RIGHT_MOTOR = Motor('D')
DELIVERY_MOTOR = Motor('C')
PUSHING_MOTOR = Motor('B')

LINE_SENSOR=EV3ColorSensor(1)
COLOR_SENSOR=EV3ColorSensor(2)
TOUCH_SENSOR=TouchSensor(4)
LEFT_MOTOR.set_limits(dps = 500)
RIGHT_MOTOR.set_limits(dps = 500)

TARGET=(170+25)/2
Kp=0.01
Ki=0.0015
Kd=0.02
def real_value(sensor):
    value = sensor.get_value()
    while sensor.get_value()== None or sensor.get_value() ==[0,0,0,0]:
        value=sensor.get_value()
        print(value)
    print(value)
    return value

def PID(value,sign,base_speed):
    integral=0
    derivative=0
    last_error=0
    
    value_b=value[2]
    error=value_b-TARGET
    integral+=error
    derivative=error-last_error
    turn_rate=Kp*error+Ki*integral+Kd*derivative

    left_motor.set_power((base_speed+(sign*turn_rate))*-1)
    right_motor.set_power((base_speed-(sign*turn_rate))*-1) 
    
def delivery_protocol(degrees):
    DELIVERY_MOTOR.set_position(degrees)
    sleep(2)
    PUSHING_MOTOR.set_position(165)
    sleep(0.5)
    PUSHING_MOTOR.set_position(0)
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
def forwards(left_motor,right_motor,greens):
    base_speed=25
    value=real_value(LINE_SENSOR)
    if color_choosing(value[:-1])==4:
        greens+=1
        print('green detected')
        while color_choosing(value[:-1])==4:
            left_motor.set_power(-10)
            right_motor.set_power(-10)
            value=real_value(LINE_SENSOR)
            sleep(0.1)
    if color_choosing(value[:-1])==3:
        left_motor.set_power((base_speed)*-1)
        right_motor.set_power(0)
    PID(value,1,base_speed)
    return greens
def backwards(left_motor,right_motor,input_list):
    base_speed=15
    
    value=real_value(LINE_SENSOR)
    col=real_value(COLOR_SENSOR)
    if color_choosing(value[:-1])==4:
        left_motor.set_power(-10)
        right_motor.set_power(-10)
        while color_choosing(col[:-1])==7:
            left_motor.set_power(-10)
            right_motor.set_power(-10)
            col=real_value(COLOR_SENSOR)
            sleep(0.1)
            print(col)
        print(color_choosing(col[:-1]))
        if color_choosing(col[:-1]) not in input_list:
            input_list.append(color_choosing(col[:-1]))
            left_motor.set_power(0)
            right_motor.set_power(0)
            sleep(0.5)
            left_motor.set_position_relative(-270)
            right_motor.set_position_relative(-270)
            sleep(0.5)
            delivery(color_choosing(col[:-1]))
            sleep(0.5)
            left_motor.set_position_relative(240)
            right_motor.set_position_relative(240)
            sleep(1)
    value=real_value(LINE_SENSOR)
    PID(value,-1,base_speed)
    print(input_list) 

if __name__ == "__main__":
    try:
        greens_detected=0
        deliveries_done=[]
        while True:
            if greens_detected<6:
                greens_detected=forwards(LEFT_MOTOR,RIGHT_MOTOR,greens_detected)
            elif greens_dected == 6:
                left_motor.set_position_relative(-360)
                right_motor.set_position_relative(-360)
                sleep(0.5)
                left_motor.set_position_relative(-500)
                sleep(0.5)
                backwards(LEFT_MOTOR,RIGHT_MOTOR,deliveries_done)
                greens_detected+=1
            else:
                backwards(LEFT_MOTOR,RIGHT_MOTOR,deliveries_done)
            if len(deliveries_done)==6:
                break
    except BaseException as e :
        print ("Done with the program")
        print(e)
        print(traceback.format_exc())
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        reset_brick()
        exit()
