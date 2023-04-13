from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick,Motor,EV3ColorSensor
from time import sleep, time
from math import sqrt
from RGB import color_choosing
from RGB_LINE import color_choosing_LINE
from utils import sound
import traceback
wait_ready_sensors(True)

LEFT_MOTOR = Motor('A')
RIGHT_MOTOR = Motor('D')
DELIVERY_MOTOR = Motor('C')
PUSHING_MOTOR = Motor('B')

LINE_SENSOR=EV3ColorSensor(1)
COLOR_SENSOR=EV3ColorSensor(2)
TOUCH_SENSOR=TouchSensor(3)
LEFT_MOTOR.set_limits(dps = 200)
RIGHT_MOTOR.set_limits(dps = 200)
PUSHING_MOTOR.set_limits(dps=270)
DELIVERY_MOTOR.set_limits(dps = 300)

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=100)

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
    
    if color_choosing_LINE(value[:-1])==4:
        greens+=1
        print('green detected')
        while color_choosing_LINE(value[:-1])==4:
            LEFT_MOTOR.set_power(-15)
            RIGHT_MOTOR.set_power(-15)
            value=real_value(LINE_SENSOR)
            sleep(0.25)
            
    while color_choosing(value[:-1])==1:
        LEFT_MOTOR.set_power(-10)
        RIGHT_MOTOR.set_power(-40)
        value=real_value(LINE_SENSOR)
        
    integral=PID(value,-1,base_speed,integral,derivative,last_error)[0]
    derivative=PID(value,-1,base_speed,integral,derivative,last_error)[1]
    last_error=PID(value,-1,base_speed,integral,derivative,last_error)[2]
    return greens


def backwards(last_value,deliveries_done):
    greens=0
    while True:
        print(greens)
        base_speed=20
        value=real_value(LINE_SENSOR)
        col=real_value(COLOR_SENSOR)
        
        LEFT_MOTOR.set_power(-base_speed)
        RIGHT_MOTOR.set_power(-base_speed)
        
        while color_choosing_LINE(value[:-1]) == 1:
            LEFT_MOTOR.set_power((base_speed+10)*-1)
            RIGHT_MOTOR.set_power(8)
            value=real_value(LINE_SENSOR)
            
        while color_choosing_LINE(value[:-1]) == 3:
            LEFT_MOTOR.set_power(8)
            RIGHT_MOTOR.set_power((base_speed+10)*-1)
            value=real_value(LINE_SENSOR)
        if  color_choosing_LINE(value[:-1]) == 4:
            greens+=1
            while color_choosing_LINE(value[:-1]) == 4:
                value=real_value(LINE_SENSOR)
                print('a')
                sleep(0.1)
                continue
        
        if color_choosing(col[:-1])!=7 and color_choosing(col[:-1]) not in deliveries_done:
            deliveries_done.append(color_choosing(col[:-1]))
            while color_choosing(col[:-1])!=7:
                col=real_value(COLOR_SENSOR)
                value=real_value(LINE_SENSOR)
                if color_choosing_LINE(value[:-1]) == 1:
                    LEFT_MOTOR.set_power((base_speed+15)*-1)
                    RIGHT_MOTOR.set_power(7)
                    value=real_value(LINE_SENSOR)
                if color_choosing_LINE(value[:-1]) == 3:
                    LEFT_MOTOR.set_power(7)
                    RIGHT_MOTOR.set_power((base_speed+15)*-1)
                    value=real_value(LINE_SENSOR)
                if color_choosing_LINE(value[:-1]) == 4:
                    value=real_value(LINE_SENSOR)
                    greens+=1
                    continue
                sleep(0.1)
                print(color_choosing(col[:-1]))
                continue
            if deliveries_done[-1]==4:
                LEFT_MOTOR.set_power(0)
                RIGHT_MOTOR.set_power(0)
                sleep(0.1)
                if color_choosing_LINE(value[:-1]) == 1:
                    LEFT_MOTOR.set_power((base_speed+15)*-1)
                    RIGHT_MOTOR.set_power(7)
                    value=real_value(LINE_SENSOR)
                if color_choosing_LINE(value[:-1]) == 3:
                    LEFT_MOTOR.set_power(7)
                    RIGHT_MOTOR.set_power((base_speed+15)*-1)
                    value=real_value(LINE_SENSOR)
                if color_choosing_LINE(value[:-1]) == 4:
                    value=real_value(LINE_SENSOR)
                    continue
                sleep(1.5)
                LEFT_MOTOR.set_power(0)
                RIGHT_MOTOR.set_power(0)
                sleep(0.1)
                delivery(deliveries_done[-1])
                sleep(0.3)
            elif deliveries_done[-1]==3:
                LEFT_MOTOR.set_power(0)
                RIGHT_MOTOR.set_power(0)
                sleep(0.1)
                if color_choosing_LINE(value[:-1]) == 1:
                    LEFT_MOTOR.set_power((base_speed+15)*-1)
                    RIGHT_MOTOR.set_power(7)
                    value=real_value(LINE_SENSOR)
                if color_choosing_LINE(value[:-1]) == 3:
                    LEFT_MOTOR.set_power(7)
                    RIGHT_MOTOR.set_power((base_speed+15)*-1)
                    value=real_value(LINE_SENSOR)
                if color_choosing_LINE(value[:-1]) == 4:
                    value=real_value(LINE_SENSOR)
                    continue
                sleep(1.5)
                LEFT_MOTOR.set_power(0)
                RIGHT_MOTOR.set_power(0)
                sleep(0.1)
                delivery(deliveries_done[-1])
                sleep(0.3)
            else:
                LEFT_MOTOR.set_power(0)
                RIGHT_MOTOR.set_power(0)
                sleep(0.1)
                delivery(deliveries_done[-1])
                sleep(0.3)
        if  greens == 6 or len(deliveries_done)==6:
            LEFT_MOTOR.set_power(0)
            RIGHT_MOTOR.set_power(0)
            sleep(0.1)
            while len(deliveries_done)!=6:
                if 1 not in deliveries_done:
                    deliveries_done.append(1)
                    delivery(1)
                elif 2 not in deliveries_done:
                    deliveries_done.append(2)
                    delivery (2)
                elif 3 not in deliveries_done:
                    deliveries_done.append(3)
                    delivery (3)
                elif 4 not in deliveries_done:
                    deliveries_done.append(4)
                    delivery (4)
                elif 5 not in deliveries_done:
                    deliveries_done.append(5)
                    delivery (5)
                elif 6 not in deliveries_done:
                    deliveries_done.append(6)
                    delivery (6)
                sleep(0.2)
            break
        sleep(0.1)
            
if __name__ == "__main__":
    try:
        last_value=[]
        deliveries_done=[]
        integral=0
        derivative=0
        last_error=0
        while True:
            if TOUCH_SENSOR.is_pressed():
                SOUND.play()
                SOUND.wait_done()
                greens_detected=0
                while True:
                    greens_detected=forwards(greens_detected,integral,derivative,last_error)
                    print(greens_detected)
                    
                    if greens_detected==6:
                        timeout = time() + 4
                        while True:
                            greens_detected=forwards(greens_detected,integral,derivative,last_error)
                            if time() > timeout:
                                break
                            sleep(0.1)
                        sleep(0.1)
                        
                        LEFT_MOTOR.set_power(0)
                        RIGHT_MOTOR.set_power(0)
                        sleep(1)
                        
                        LEFT_MOTOR.set_power(-30)
                        RIGHT_MOTOR.set_power(30)
                        sleep(2.8)
                        LEFT_MOTOR.set_power(0)
                        RIGHT_MOTOR.set_power(0)
                        sleep(0.2)
                        
                        while True:
                            backwards(last_value,deliveries_done)
                            sleep(0.1)
                            deliveries_done.clear()
                            
                            value=real_value(LINE_SENSOR)
                            while color_choosing_LINE(value)!=6:

                                base_speed=25
                                value=real_value(LINE_SENSOR)
                                col=real_value(COLOR_SENSOR)
                                
                                LEFT_MOTOR.set_power(-base_speed)
                                RIGHT_MOTOR.set_power(-base_speed)
                                
                                while color_choosing_LINE(value[:-1]) == 1:
                                    LEFT_MOTOR.set_power((base_speed+30)*-1)
                                    RIGHT_MOTOR.set_power(7)
                                    value=real_value(LINE_SENSOR)
                                    
                                while color_choosing_LINE(value[:-1]) == 3:
                                    LEFT_MOTOR.set_power(7)
                                    RIGHT_MOTOR.set_power((base_speed+30)*-1)
                                    value=real_value(LINE_SENSOR)
                                    
                                while color_choosing_LINE(value[:-1]) == 4:
                                    value=real_value(LINE_SENSOR)
                                    print('a')
                                    continue
                                value=real_value(LINE_SENSOR)
                                sleep(0.1)
                                
                            sleep(0.1)
                            LEFT_MOTOR.set_power(0)
                            RIGHT_MOTOR.set_power(0)
                            sleep(0.2)
                            LEFT_MOTOR.set_power(-30)
                            RIGHT_MOTOR.set_power(30)
                
                            sleep(2.8)
                            
                            break
                        
                        LEFT_MOTOR.set_power(0)
                        RIGHT_MOTOR.set_power(0)
                        SOUND.play()
                        SOUND.wait_done()
                        break
    except BaseException as e :
        print("Done with the program")
        print(e)
        print(traceback.format_exc())
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        reset_brick()
        exit()


