import RPi.GPIO as GPIO
import time
import threading
import sys
import paho.mqtt.client as mqtt
import config

# Access the constants from the config module
broker_ip = config.broker_ip
topic = config.topic
username = config.username
password = config.password

MOTOR_1 = 12
MOTOR_2 = 13
MOTOR_3 = 18

UP = [90, 100]
DOWN = UP[::-1]


def move_servo(motor_pin, start_angle, end_angle, res):
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pin, GPIO.OUT)

    # Create PWM object at 50 Hz frequency
    servo_pwm = GPIO.PWM(motor_pin, 50)

    # Start the PWM signal at 0% duty cycle (neutral position)
    servo_pwm.start(0)

    # Determine the step
    step = int((end_angle - start_angle) / res)

    # Loop from start_angle to end_angle
    for angle in range(start_angle, end_angle + step, step):
        goto_angle(servo_pwm, angle)
        time.sleep(0.1)

        # Clean up GPIO
    servo_pwm.stop()


def goto_angle(pwm, angle):
    # Calculate duty cycle based on angle
    duty_cycle = 2.0 + (angle / 18)

    # Set the position of the servo motor
    pwm.ChangeDutyCycle(duty_cycle)


def pen(direction):
    motor_pin = MOTOR_3
    start_angle = direction[0]
    end_angle = direction[1]
    resolution = 10
    move_servo(motor_pin, start_angle, end_angle, resolution)


def move_arm(start_1, start_2, end_1, end_2, pen_status):
    # Move pen
    pen(pen_status)
    time.sleep(0.5)

    # Calculate the resolution
    res = int(min(abs(end_1 - start_1), abs(end_2 - start_2)) / 2)

    # Create two threads for moving the servos concurrently
    thread1 = threading.Thread(target=move_servo, args=(MOTOR_1, start_1, end_1, res))
    thread2 = threading.Thread(target=move_servo, args=(MOTOR_2, start_2, end_2, res))

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    time.sleep(0.5)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        print("Listening...")
        client.subscribe(topic)
    else:
        print("Connection failed. RC:", rc)


def on_message(client, userdata, msg):
    start_angle_1, start_angle_2, end_angle_1, end_angle_2, pen_position_flag = map(
        int, msg.payload.decode().split(",")
    )

    # Validate the pen position flag
    if pen_position_flag == 0:
        pen_position = UP
    elif pen_position_flag == 1:
        pen_position = DOWN
    else:
        print("Error: Invalid pen position flag.")
        sys.exit(1)

    # Move to target position
    move_arm(start_angle_1, start_angle_2, end_angle_1, end_angle_2, pen_position)

    print(
        "start angle 1:" + str(start_angle_1) + ", start_angle_2: " + str(start_angle_2)
    )
    print("end angle 1:" + str(end_angle_1) + ", end angle 2: " + str(end_angle_2))
    print("Pen: " + str(pen_position))
    print()
    GPIO.cleanup()


# Main
if __name__ == "__main__":
    # Receive the angles via MQTT listener
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_ip)
    client.loop_forever()
