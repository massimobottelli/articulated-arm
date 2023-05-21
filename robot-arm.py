import RPi.GPIO as GPIO
import time
import threading

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
        time.sleep(0.05)

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
    move_servo(motor_pin, start_angle, end_angle, 10)


def move_arm(start_1, end_1, start_2, end_2, pen_status):
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


# Main

if __name__ == '__main__':

    angles = [
        (90, 130), (90, 30), UP,
        (130, 90), (30, 90), DOWN,
        (90, 30), (90, 190), UP,
        (30, 90), (190, 90), DOWN,
    ]

    # Iterate over the array two by two
    for i in range(0, len(angles), 3):
        angle1 = angles[i]
        angle2 = angles[i + 1]
        pos = angles[i + 2]

        start_angle_1, end_angle_1 = angle1
        start_angle_2, end_angle_2 = angle2

        move_arm(start_angle_1, end_angle_1, start_angle_2, end_angle_2, pos)

    GPIO.cleanup()

