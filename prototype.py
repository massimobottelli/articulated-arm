import pygame
import math

# Initialize Pygame
pygame.init()

# Define the dimensions of the board
board_width = 500
board_height = 250

# Define the origin coordinates
origin_x = 250
origin_y = 10

# Define arms length
arm_1_length = 93
arm_2_length = 140

# Create the white board surface
board = pygame.display.set_mode((board_width, board_height))
pygame.display.set_caption("Robotic Arm Simulation")

board.fill((255, 255, 255))  # Fill the board with white

# Define the font for displaying coordinates
font = pygame.font.Font(None, 20)


def draw_origin():
    board.fill((255, 255, 255))  # Clear the board

    # Draw the origin (initial point) on the board
    pygame.draw.circle(board, (255, 0, 0), (origin_x, origin_y), 3)
    # Draw a circle centered on the origin with a radius of arm_1_length
    pygame.draw.circle(board, (0, 0, 255), (origin_x, origin_y), arm_1_length, 1)


def get_target():
    x, y = pygame.mouse.get_pos()

    # Draw a red dot at clicked position
    pygame.draw.circle(board, (255, 0, 0), (x, y), 3)

    # Draw a circle centered on the clicked point with a radius of arm_2_length
    pygame.draw.circle(board, (0, 0, 255), (x, y), arm_2_length, 1)

    # Display the coordinates on the board near the red dot
    display_coords(x, y, x + 10, y - 10)

    return x, y


def find_intersection(target_x, target_y):
    dx = target_x - origin_x
    dy = target_y - origin_y
    d = (arm_1_length ** 2 - arm_2_length ** 2 + distance ** 2) / (2 * distance)
    h = (arm_1_length ** 2 - d ** 2) ** 0.5
    intersect_x1 = origin_x + (d * dx - h * dy) / distance
    intersect_y1 = origin_y + (h * dx + d * dy) / distance
    intersect_x2 = origin_x + (d * dx + h * dy) / distance
    intersect_y2 = origin_y + (-h * dx + d * dy) / distance

    # Draw the points of intersection
    pygame.draw.circle(board, (255, 0, 0), (int(intersect_x1), int(intersect_y1)), 3)
    pygame.draw.circle(board, (255, 0, 0), (int(intersect_x2), int(intersect_y2)), 3)

    return intersect_x1, intersect_y1, intersect_x2, intersect_y2


def draw_lines(x1, y1, x2, y2):
    # Draw lines from origin to intersection points and from there to the clicked point
    pygame.draw.line(board, (0, 0, 0), (origin_x, origin_y), (x1, y1), 1)
    pygame.draw.line(board, (0, 0, 0), (x1, y1), (x2, y2), 1)


def find_angles(x1, y1, x2, y2):
    # Calculate angles between lines
    angle_origin_to_intersect = calculate_angle(origin_x, origin_y, x1, y1)
    angle_intersect_to_target = calculate_angle(x1, y1, x2, y2)

    relative_angle = 90 + angle_intersect_to_target - angle_origin_to_intersect if angle_origin_to_intersect < angle_intersect_to_target else  180 + angle_intersect_to_target - angle_origin_to_intersect
    
    # Display angles near the respective lines
    display_angle(angle_origin_to_intersect, (origin_x + x1) // 2, (origin_y + y1) // 2)
    display_angle(relative_angle, (x1 + x2) // 2, (y1 + y2) // 2)

    return int(angle_origin_to_intersect), int(relative_angle)


def calculate_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    return math.degrees(math.atan2(delta_y, delta_x))


def display_angle(angle, label_x, label_y):
    # Display angles near the respective lines
    angle_surface = font.render(f"{int(angle)} deg", True, (0, 0, 0))
    angle_rect = angle_surface.get_rect()
    angle_rect.center = (label_x, label_y)
    board.blit(angle_surface, angle_rect)


def display_coords(x, y, label_x, label_y):
    # Display the coordinates on the board near the red dot
    text_surface = font.render(f"({x}, {y})", True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (label_x, label_y)
    board.blit(text_surface, text_rect)


draw_origin()

# Update the display
pygame.display.flip()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                draw_origin()

                target_x, target_y = get_target()

                # Find the points of intersection between the two circles
                distance = ((target_x - origin_x) ** 2 + (target_y - origin_y) ** 2) ** 0.5

                # Check if the circles intersect
                if distance <= arm_1_length + arm_2_length:

                    # Find intersections
                    intersect_x1, intersect_y1, intersect_x2, intersect_y2 = find_intersection(target_x, target_y)

                    # Display the coordinates of the points of intersection on the board
                    display_coords(int(intersect_x1), int(intersect_y1), int(intersect_x1)+10, int(intersect_y1)-10)
                    display_coords(int(intersect_x2), int(intersect_y2), int(intersect_x2)+10, int(intersect_y2)-10)

                    # Draw lines from origin to intersection points and from there to the clicked point
                    draw_lines(intersect_x1, intersect_y1, target_x, target_y)
                    draw_lines(intersect_x2, intersect_y2, target_x, target_y)

                    # Calculate and display angles between lines
                    angle_origin_to_intersect_1, relative_angle_1 = find_angles(intersect_x1, intersect_y1, target_x, target_y)
                    angle_origin_to_intersect_2, relative_angle_2 = find_angles(intersect_x2, intersect_y2, target_x, target_y)

                    # Output to console
                    print (angle_origin_to_intersect_1, relative_angle_1)
                    print (angle_origin_to_intersect_2, relative_angle_2)
                    print()
                    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
