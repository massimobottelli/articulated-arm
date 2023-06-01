import math
import paho.mqtt.client as mqtt
import config

# Access the constants from the config module
origin_x = config.origin_x
origin_y = config.origin_y
arm_1_length = config.arm_1_length
arm_2_length = config.arm_2_length
broker_ip = config.broker_ip
topic = config.topic
username = config.username
password = config.password

# Constants for drawing X symbol on board
# Parking position
xp = 350
yp = 120

# Top-left corner of board
x0 = 205
y0 = 110

# Size of cell
dx = 30
dy = 30


def find_intersection(x, y):
    dx = x - origin_x
    dy = y - origin_y
    d = (arm_1_length ** 2 - arm_2_length ** 2 + distance ** 2) / (2 * distance)
    h = (arm_1_length ** 2 - d ** 2) ** 0.5
    x1 = origin_x + (d * dx - h * dy) / distance
    y1 = origin_y + (h * dx + d * dy) / distance
    x2 = origin_x + (d * dx + h * dy) / distance
    y2 = origin_y + (-h * dx + d * dy) / distance
    return x1, y1, x2, y2


def find_angles(x1, y1, x2, y2):
    # Calculate angles between lines
    angle_origin_to_intersect = calculate_angle(origin_x, origin_y, x1, y1)
    angle_intersect_to_target = calculate_angle(x1, y1, x2, y2)
    if angle_origin_to_intersect < angle_intersect_to_target:
        relative_angle = 90 + angle_intersect_to_target - angle_origin_to_intersect
    else:
        relative_angle = 90 + angle_intersect_to_target - angle_origin_to_intersect
    return int(angle_origin_to_intersect), int(relative_angle)


def calculate_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    return math.degrees(math.atan2(delta_y, delta_x))


def select_angles(angle1, angle2):
    diff_1 = abs(angle1[0] - 90) + abs(angle2[0] - 90)
    diff_2 = abs(angle1[1] - 90) + abs(angle2[1] - 90)
    if diff_1 > diff_2:
        selected_angle_1 = angle1[0]
        selected_angle_2 = angle2[0]
        selected_intersect_x = intersect_x1
        selected_intersect_y = intersect_y1
    else:
        selected_angle_1 = angle1[1]
        selected_angle_2 = angle2[1]
        selected_intersect_x = intersect_x2
        selected_intersect_y = intersect_y2
    return selected_angle_1, selected_angle_2, selected_intersect_x, selected_intersect_y


def position_to_angle(target_x, target_y):
    global distance, intersect_x1, intersect_y1, intersect_x2, intersect_y2

    # Initialize variables
    angle_1 = [0, 0]
    angle_2 = [0, 0]
    intersect_1 = [0, 0]
    intersect_2 = [0, 0]

    # Find the position of elbow
    distance = ((target_x - origin_x) ** 2 + (target_y - origin_y) ** 2) ** 0.5
    if distance <= arm_1_length + arm_2_length:
        # Find intersections
        intersect_x1, intersect_y1, intersect_x2, intersect_y2 = find_intersection(target_x, target_y)

        # Calculate angles between lines
        angle_1[0], angle_2[0] = find_angles(intersect_x1, intersect_y1, target_x, target_y)
        angle_1[1], angle_2[1] = find_angles(intersect_x2, intersect_y2, target_x, target_y)

        # Select the pair of angles more distant to 90
        final_angle_1, final_angle_2, selected_intercept_x, selected_intercept_y = \
            select_angles(angle_1, angle_2)

        return final_angle_1, final_angle_2


def calc_move_coords(row, col):
    # Create tuple of coordinates to draw X in given cell

    # Initialize arrays
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    p = []

    # Coordinates for arm move #1
    x1.append(xp)
    y1.append(yp)
    x2.append(x0 + row  * dx)
    y2.append(y0 + col * dx)
    p.append(0)

    # Coordinates for arm move #2
    x1.append(x0 + row * dx)
    y1.append(y0 + col * dx)
    x2.append(x0 + (row + 1) * dx)
    y2.append(y0 + (col + 1) * dy)
    p.append(1)

    # Coordinates for arm move #3
    x1.append(x0 + (row + 1) * dx)
    y1.append(y0 + (col + 1) * dy)
    x2.append(x0 + (row + 1) * dx)
    y2.append(y0 + col * dy)
    p.append(0)

    # Coordinates for arm move #4
    x1.append(x0 + (row + 1) * dx)
    y1.append(y0 + col * dy)
    x2.append(x0 + row * dx)
    y2.append(y0 + (col + 1) * dy)
    p.append(1)

    # Coordinates for arm move #5
    x1.append(x0 + row * dx)
    y1.append(y0 + (col + 1) * dy)
    x2.append(xp)
    y2.append(yp)
    p.append(0)

    # Create tuple of moves
    moves = (x1, y1, x2, y2, p)

    return moves


def publish_mqtt(start_angle_1, start_angle_2, end_angle_1, end_angle_2, pen_position_flag):
    try:
        # Publish data over MQTT
        client = mqtt.Client()
        client.username_pw_set(username, password)
        client.connect(broker_ip)
        message = str(start_angle_1) + "," + str(start_angle_2) + "," + str(end_angle_1) + "," + \
                  str(end_angle_2) + "," + str(pen_position_flag)
        client.publish(topic, message)
        client.disconnect()
        return True
    except Exception as e:
        # Handle exceptions
        print("Error:", e)
        return False


# Main

# Select cell to draw
row = 1
col = 1

print("Row: " + str(row) + "; Col: " + str(col))

# Calculate sequence of moves to draw X symbol in selected cell
moves = calc_move_coords(row, col)

# Iterate over sequence
for i in range(len(moves[0])):
    x1, y1, x2, y2, pen = [moves[j][i] for j in range(len(moves))]

    # Calculate angles
    start_angle_1, start_angle_2 = position_to_angle(x1, y1)
    end_angle_1, end_angle_2 = position_to_angle(x2, y2)
    end_angle_1 = 180 - end_angle_1
    end_angle_2 = 180 - end_angle_2

    # Print coordinates and angles
    print ("From " + str(x1) + "," + str(y1) + " -> Angles: " + str(start_angle_1) + "," + str(start_angle_2))
    print ("To " + str(x2) +"," + str(y2) + " -> Angles: " + str(end_angle_1) + "," + str(end_angle_2))
    print ("Pen: " + str(pen))
    print ()

    # Publish data over MQTT
    publish_mqtt(start_angle_1, start_angle_2, end_angle_1, end_angle_2, pen)

