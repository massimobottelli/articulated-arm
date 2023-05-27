import pygame
import math

# Initialize Pygame
pygame.init()

# Define the dimensions of the board
board_width = 500
board_height = 250

# Define the origin coords
origin_x = 250
origin_y = 10

# Define arms length
arm_1_length = 93
arm_2_length = 140

# Create the white board surface
board = pygame.display.set_mode((board_width, board_height))
pygame.display.set_caption("Robotic Arm Simulation")

board.fill((255, 255, 255))  # Fill the board with white

# Define the font for displaying coords
font = pygame.font.Font(None, 20)


def draw_origin():
    # Draw the origin (initial point) on the board
    pygame.draw.circle(board, (255, 0, 0), (origin_x, origin_y), 3)
    # Draw a circle centered on the origin with a radius of arm_1_length
    pygame.draw.circle(board, (0, 0, 255), (origin_x, origin_y), arm_1_length, 1)


def draw_lines(x1, y1, x2, y2):
    # Draw lines from origin to intersection points and from there to the clicked point
    pygame.draw.line(board, (0, 0, 0), (origin_x, origin_y), (x1, y1), 1)
    pygame.draw.line(board, (0, 0, 0), (x1, y1), (x2, y2), 1)


def find_angles(x1, y1, x2, y2):
    # Calculate angles between lines
    angle_origin_to_intersect1 = calculate_angle(origin_x, origin_y, x1, y1)
    angle_intersect1_to_mouse = calculate_angle(x1, y1, x2, y2)

    # Display angles near the respective lines
    display_angle(angle_origin_to_intersect1, (origin_x + x1) // 2, (origin_y + y1) // 2)
    display_angle(angle_intersect1_to_mouse, (x1 + x2) // 2, (y1 + y2) // 2)


def display_angle(angle, label_x, label_y):
    # Display angles near the respective lines
    angle_surface = font.render(f"{int(angle)} deg", True, (0, 0, 0))
    angle_rect = angle_surface.get_rect()
    angle_rect.center = (label_x, label_y)
    board.blit(angle_surface, angle_rect)


def display_coords(x, y, label_x, label_y):
    # Display the coords on the board near the red dot
    text_surface = font.render(f"({x}, {y})", True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (label_x, label_y)
    board.blit(text_surface, text_rect)


def calculate_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    return math.degrees(math.atan2(delta_y, delta_x))


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
                board.fill((255, 255, 255))  # Clear the board
                draw_origin()

                target_x, target_y = pygame.mouse.get_pos()
                relative_x = target_x - origin_x
                relative_y = target_y - origin_y

                # Draw a red dot at clicked position
                pygame.draw.circle(board, (255, 0, 0), (target_x, target_y), 3)

                # Draw a circle centered on the clicked point with a radius of arm_2_length
                pygame.draw.circle(board, (0, 0, 255), (target_x, target_y), arm_2_length, 1)

                # Display the coords on the board near the red dot
                display_coords(target_x, target_y, target_x + 10, target_y - 10)

                # Find the points of intersection between the two circles
                distance = ((target_x - origin_x) ** 2 + (target_y - origin_y) ** 2) ** 0.5
                if distance <= arm_1_length + arm_2_length:  # Check if the circles intersect
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

                    # Display the coords of the points of intersection on the board
                    display_coords(int(intersect_x1), int(intersect_y1), int(intersect_x1)+10, int(intersect_y1)-10)
                    display_coords(int(intersect_x2), int(intersect_y2), int(intersect_x2)+10, int(intersect_y2)-10)

                    # Draw lines from origin to intersection points and from there to the clicked point
                    draw_lines(intersect_x1, intersect_y1, target_x, target_y)
                    draw_lines(intersect_x2, intersect_y2, target_x, target_y)

                    # Calculate and display angles between lines
                    find_angles(intersect_x1, intersect_y1, target_x, target_y)
                    find_angles(intersect_x2, intersect_y2, target_x, target_y)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
