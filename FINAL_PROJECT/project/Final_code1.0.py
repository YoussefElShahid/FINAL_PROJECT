from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick,Motor,EV3ColorSensor
from time import sleep, time
from math import sqrt
from RGB import color_choosing
wait_ready_sensors(True)

LEFT_MOTOR = Motor('A')
RIGHT_MOTOR = Motor('D')
DELIVERY_MOTOR = Motor('B')
PUSHING_MOTOR = Motor('C')

LINE_SENSOR=EV3ColorSensor(2)
COLOR_SENSOR=EV3ColorSensor(1)
TOUCH_SENSOR=TouchSensor(3)

BASE_SPEED=20

def forwards(left_motor,right_motor):
    value=LINE_SENSOR.get_value()
    color=color_chossing(value)
    if color == 1:
        left_motor.set_power(BASE_SPEED)
        right_motor.set_power(BASE_SPEED+20)
    elif color == 3:
        left_motor.set_power(BASE_SPEED+20)
        right_motor.set_power(BASE_SPEED)
    else:
        left_motor.set_power(BASE_SPEED)
        right_motor.set_power(BASE_SPEED)
        
def backwards(left_motor,right_motor):
    value=LINE_SENSOR.get_value()
    color=color_chossing(value)
    if color == 1:
        left_motor.set_power(BASE_SPEED+20)
        right_motor.set_power(BASE_SPEED)
    elif color == 3:
        left_motor.set_power(BASE_SPEED)
        right_motor.set_power(BASE_SPEED+20)
    else:
        left_motor.set_power(BASE_SPEED)
        right_motor.set_power(BASE_SPEED)
        
        
def timed_loop_motor():
    endtime=time.time()+1
    while(time.time()<endtime):
        PUSHING_MOTOR.set_power(20)
        
        
def delivery_protocol(degrees):
    DELIVERY_MOTOR.set_position(degrees)
    sleep(0.5)
    timed_loop_motor()
    sleep(0.5)
    DELIVERY_MOTOR.set_position(0)

def delivery(color):
    if color == 1:
        delivery_protocol(60)
    elif color == 2:
        delivery_protocol(90)
    elif color == 3:
        delivery_protocol(120)
    elif color == 4:
        delivery_protocol(150)
    elif color == 5:
        delivery_protocol(180)
    elif color == 6:
        delivery_protocol(210)

def run():
    try:
        while True:
            if TOUCH_SENSOR.is_pressed():
                deliveries_done=0
                while True:
                    forwards(LEFT_MOTOR,RIGHT_MOTOR)
                
                    color = color_choosing(COLOR_SENSOR.get_value())
                    if color != 7:
                        LEFT_MOTOR.set_power(0)
                        RIGHT_MOTOR.set_power(0)
                        delivery(color)
                        deliveries_done+=1
                    if deliveries_done == 6:
                        sleep(0.5)
                        LEFT_MOTOR.set_position(-360)
                        RIGHT_MOTOR.set_position(360)
                        sleep(0.5)
                        while color_choosing(LINE_SENSOR.get_value()) != 6:
                            backwards()
                        LEFT_MOTOR.set_position(-360)
                        RIGHT_MOTOR.set_position(360)
                        break
    except BaseException:
        print ("Done with the program")
        LEFT_MOTOR.set_power(0)
        RIGHT_MOTOR.set_power(0)
        reset_brick()
        output_file.close()
        exit()

if __name__ == "__main__":
    run()
        
