from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick,Motor,EV3ColorSensor
from time import sleep, time
from math import sqrt
from RGB import color_choosing
from RGB_LINE import color_choosing_LINE
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
PUSHING_MOTOR.set_limits(dps=270)
DELIVERY_MOTOR.set_limits(dps = 300)
TARGET=(32+289)/2
Kp=0.08
Ki=0.05
Kd=0.01
def real_value(sensor):
    value = sensor.get_value()
    while value== None or value ==[0,0,0,0]:
        value=sensor.get_value()
        print(value)
    print(value)
    return value

def PID(value,sign,base_speed,integral,derivative,last_error):
    
    value_b=value[0]
    error=value_b-TARGET
    integral+=error
    derivative=error-last_error
    turn_rate=Kp*error+Ki*integral+Kd*derivative
    
    if color_choosing(value[:-1])==1:
        LEFT_MOTOR.set_power(-24)
        RIGHT_MOTOR.set_power(0)
    elif color_choosing(value[:-1])==6:
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
    else:
        LEFT_MOTOR.set_power((base_speed+(sign*turn_rate))*-1)
        RIGHT_MOTOR.set_power((base_speed-(sign*turn_rate))*-1)
    return [integral,derivative,last_error]
    
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
        delivery_protocol(-30)
    elif color == 2:
        delivery_protocol(-130)
    elif color == 3:
        delivery_protocol(-390)
    elif color == 4:
        delivery_protocol(-305)
    elif color == 5:
        delivery_protocol(-480)
    elif color == 6:
        delivery_protocol(-210)
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
            sleep(0.5)
    while color_choosing(value[:-1])==1:
        LEFT_MOTOR.set_power(-10)
        RIGHT_MOTOR.set_power(-40)
        value=real_value(LINE_SENSOR)
    integral=PID(value,-1,base_speed,integral,derivative,last_error)[0]
    derivative=PID(value,-1,base_speed,integral,derivative,last_error)[1]
    last_error=PID(value,-1,base_speed,integral,derivative,last_error)[2]
    return greens
def backwards(last_value,deliveries_done):
    base_speed=15
    value=real_value(LINE_SENSOR)
    col=real_value(COLOR_SENSOR)
    LEFT_MOTOR.set_power(-base_speed)
    RIGHT_MOTOR.set_power(-base_speed)
    last_value=7
    while color_choosing_LINE(value[:-1]) == 1:
        LEFT_MOTOR.set_power((base_speed+25)*-1)
        RIGHT_MOTOR.set_power((base_speed-5)*-1)
        value=real_value(LINE_SENSOR)
        last_value=1
    while color_choosing_LINE(value[:-1]) == 3:
        LEFT_MOTOR.set_power(-(base_speed-5))
        RIGHT_MOTOR.set_power((base_speed+25)*-1)
        value=real_value(LINE_SENSOR)
        last_value=3
    while color_choosing_LINE(value[:-1]) == 4:
        if last_value==1:
            LEFT_MOTOR.set_power((base_speed+25)*-1)
            RIGHT_MOTOR.set_power(-(base_speed-5))
        elif last_value==3:
            LEFT_MOTOR.set_power(-(base_speed-5))
            RIGHT_MOTOR.set_power((base_speed+25)*-1)
        else:
            LEFT_MOTOR.set_power(-base_speed)
            RIGHT_MOTOR.set_power(-base_speed)
        value=real_value(LINE_SENSOR)
    if color_choosing(col[:-1])!=7 and color_choosing(col[:-1]) not in deliveries_done:
        deliveries_done.append(color_choosing(col[:-1]))
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        sleep(0.2)
        LEFT_MOTOR.set_position_relative(-200)
        RIGHT_MOTOR.set_position_relative(-200)
        sleep(0.2)
        delivery(color_choosing(col[:-1]))
        sleep(0.2)
        value=real_value(LINE_SENSOR)
        sleep(0.2)
    print(last_value)
            
if __name__ == "__main__":
    try:
        greens_detected=0
        last_value=99
        deliveries_done=[]
        integral=0
        derivative=0
        last_error=0
        while True:
            backwards(last_value,deliveries_done)
            #print(LINE_SENSOR.get_value())
            #value=real_value(LINE_SENSOR)
            #print(color_choosing_LINE(value[:-1]))
    except BaseException as e :
        print("Done with the program")
        print(e)
        print(traceback.format_exc())
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        reset_brick()
        exit()

