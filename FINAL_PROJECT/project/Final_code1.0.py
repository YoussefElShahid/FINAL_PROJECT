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
#PUSHING_MOTOR.set_limits(dps=150)

TARGET=(21+184)/2
Kp=0.1
Ki=0.08
Kd=0
def real_value(sensor):
    value = sensor.get_value()
    while value== None or value ==[0,0,0,0]:
        value=sensor.get_value()
        print(value)
    print(value)
    return value

def PID(value,sign,base_speed,integral,derivative,last_error):
    
    value_b=value[2]
    error=value_b-TARGET
    integral+=error
    derivative=error-last_error
    turn_rate=Kp*error+Ki*integral+Kd*derivative
    
    if color_choosing(value[:-1])==3:
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(-18)
    else:
        LEFT_MOTOR.set_power((base_speed+(sign*turn_rate))*-1)
        RIGHT_MOTOR.set_power((base_speed-(sign*turn_rate))*-1)
    return [integral,derivative,last_error]
    
def delivery_protocol(degrees):
    DELIVERY_MOTOR.set_position(degrees)
    sleep(2)
    PUSHING_MOTOR.set_position(155)
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
def forwards(greens,integral,derivative,last_error):
    base_speed=25
    value=real_value(LINE_SENSOR)
    print(value)
    if color_choosing(value[:-1])==4:
        greens+=1
        print('green detected')
        while color_choosing(value[:-1])==4:
            LEFT_MOTOR.set_power(-10)
            RIGHT_MOTOR.set_power(-10)
            value=real_value(LINE_SENSOR)
            sleep(0.1)
    integral=PID(value,1,base_speed,integral,derivative,last_error)[0]
    derivative=PID(value,1,base_speed,integral,derivative,last_error)[1]
    last_error=PID(value,1,base_speed,integral,derivative,last_error)[2]
    return greens
def backwards(input_list,integral,derivative,last_error):
    base_speed=13
    trigger=0
    value=real_value(LINE_SENSOR)
    col=real_value(COLOR_SENSOR)
    if color_choosing(value[:-1])==4:
        trigger+=1
        while color_choosing(value[:-1])==4:
            LEFT_MOTOR.set_power(-base_speed)
            RIGHT_MOTOR.set_power(-base_speed)
            value=real_value(LINE_SENSOR)
    if trigger == 1:
        col=real_value(COLOR_SENSOR)
        while color_choosing(col)==7:
            col=real_value(COLOR_SENSOR)
        print(color_choosing(col[:-1]))
        if color_choosing(col[:-1]) not in input_list:
            input_list.append(color_choosing(col[:-1]))
            LEFT_MOTOR.set_power(0)
            RIGHT_MOTOR.set_power(0)
            sleep(0.5)
            LEFT_MOTOR.set_position_relative(-200)
            RIGHT_MOTOR.set_position_relative(-200)
            sleep(0.5)
            delivery(color_choosing(col[:-1]))
            sleep(1)
            trigger-=1
            LEFT_MOTOR.set_position_relative(150)
            RIGHT_MOTOR.set_position_relative(150)
    value=real_value(LINE_SENSOR)
    integral=PID(value,1,base_speed,integral,derivative,last_error)[0]
    derivative=PID(value,1,base_speed,integral,derivative,last_error)[1]
    last_error=PID(value,1,base_speed,integral,derivative,last_error)[2]
    print(input_list) 

if __name__ == "__main__":
    try:
        greens_detected=0
        deliveries_done=[]
        integral=0
        derivative=0
        last_error=0
        while True:
            '''if greens_detected<6:
                greens_detected=forwards(greens_detected)
            elif greens_dected == 6:
                LEFT_MOTOR.set_position_relative(-360)
                RIGHT_MOTOR.set_position_relative(-360)
                sleep(0.5)
                LEFT_MOTOR.set_position_relative(-500)
                sleep(0.5)
                backwards(deliveries_done)
                greens_detected+=1
            else:
                backwards(deliveries_done)
            if len(deliveries_done)==6:
                break'''
            backwards(deliveries_done,integral,derivative,last_error)
            #print(LINE_SENSOR.get_value())
            #value=real_value(LINE_SENSOR)
    except BaseException as e :
        print("Done with the program")
        print(e)
        print(traceback.format_exc())
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        reset_brick()
        exit()

