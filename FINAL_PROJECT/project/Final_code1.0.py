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
LEFT_MOTOR.set_limits(dps = 500)
RIGHT_MOTOR.set_limits(dps = 500)

BASE_SPEED=25

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
def forwards_PID(left_motor,right_motor,greens):
    integral=0
    derivative=0
    last_error=0
    target=(170+25)/2
    Kp=0.01
    Ki=0.0015
    Kd=0.02
    
    value=LINE_SENSOR.get_value()
    while value == None or value ==[0,0,0,0]:
        value=LINE_SENSOR.get_value()
        print(value)
    print(value)
    if color_choosing(value[:-1])==4:
        greens+=1
        print('green detected')
        while color_choosing(value[:-1])==4:
            left_motor.set_power(-10)
            right_motor.set_power(-10)
            value=LINE_SENSOR.get_value()
            while value == None or value ==[0,0,0,0]:
                value=LINE_SENSOR.get_value()
            print(greens)
            sleep(0.1)
    if color_choosing(value[:-1])==3:
        left_motor.set_power((BASE_SPEED)*-1)
        right_motor.set_power(0)
    value_b=value[2]
    error=value_b-target
    integral+=error
    derivative=error-last_error
    turn_rate=Kp*error+Ki*integral+Kd*derivative

    left_motor.set_power((BASE_SPEED+turn_rate)*-1)
    right_motor.set_power((BASE_SPEED-turn_rate)*-1) 
    return greens
def backwards_PID(left_motor,right_motor,input_list):
    integral=0
    derivative=0
    last_error=0
    target_b=(285+32)/2
    Kp=0.1
    Ki=0
    Kd=0
    value=LINE_SENSOR.get_value()
    while value == None or value ==[0,0,0,0]:
        value=LINE_SENSOR.get_value()
        print(value)
    print(value)
    col=COLOR_SENSOR.get_value()
    while col == None or col ==[0,0,0,0]:
        col=COLOR_SENSOR.get_value()
        print(col)
    print(col)
    if color_choosing(value[:-1]==4:             
        if color_choosing(col[:-1])!=7 and color_choosing(col[:-1]) not in input_list:
            input_list.append(color_choosing(col[:-1]))
            left_motor.set_power(0)
            right_motor.set_power(0)
            sleep(0.5)
            left_motor.set_position_relative(-270)
            right_motor.set_position_relative(-270)
            sleep(0.5)
            delivery(color_choosing(col[:-1]))
            sleep(0.5)
            left_motor.set_position_relative(180)
            right_motor.set_position_relative(180)
            sleep(1)
    if len(input_list)==6:
        left_motor.set_power(0)
        right_motor.set_power(0)
        break
                         
    value_b=value[0]
    error=value_b-target_b
    integral+=error
    derivative=error-last_error
    turn_rate=Kp*error+Ki*integral+Kd*derivative

    left_motor.set_power((BASE_SPEED+turn_rate)*-1)
    right_motor.set_power((BASE_SPEED-turn_rate)*-1)
    print(input_list) 

if __name__ == "__main__":
    try:
        greens_detected=0
        deliveries_done=[]
        while True:
            backwards_PID(LEFT_MOTOR,RIGHT_MOTOR,deliveries_done)           
          
            
            
            
            


    except BaseException:
        print ("Done with the program")
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        reset_brick()
        exit()

