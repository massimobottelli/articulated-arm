import RPi.GPIO as GPIO
import time
import threading
import sys

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


# Main

if __name__ == '__main__':

    '''angles = [
        [(90, 130), (90, 30), UP],
        [(130, 90), (30, 90), DOWN],
        [(90, 30), (90, 190), UP],
        [(30, 90), (190, 90), DOWN],
    ]

    for i in range(0, len(angles)):

        # explode sublist and tuples
        motor_1_angles, motor_2_angles, pen_position = angles[i]

        motor_1_start_angle, motor_1_end_angle = motor_1_angles
        motor_2_start_angle, motor_2_end_angle = motor_2_angles'''

    # Check if the correct number of arguments is provided
    if len(sys.argv) != 6:
        print("Error: Invalid number of arguments.")
        print(
            "Usage: python robot-arm.py <motor_1_start_angle> <motor_2_start_angle> <motor_1_end_angle> "
            "<motor_2_end_angle> <pen_position_flag>")
        sys.exit(1)

    # Access command-line arguments
    motor_1_start_angle = int(sys.argv[1])
    motor_2_start_angle = int(sys.argv[2])
    motor_1_end_angle = int(sys.argv[3])
    motor_2_end_angle = int(sys.argv[4])
    pen_position_flag = int(sys.argv[5])

    # Validate the pen position flag
    if pen_position_flag == 0:
        pen_position = "UP"
    elif pen_position_flag == 1:
        pen_position = "DOWN"
    else:
        print("Error: Invalid pen position flag.")
        sys.exit(1)

    # Move to target position
    move_arm(motor_1_start_angle, motor_2_start_angle, motor_1_end_angle, motor_2_end_angle, pen_position)

    time.sleep(1)

    # Return to neutral position
    move_arm(motor_1_end_angle, motor_2_end_angle, motor_1_start_angle, motor_2_start_angle, pen_position)

    GPIO.cleanup()
