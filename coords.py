import pygame

# Initialize Pygame
pygame.init()

# Set up the display
board = pygame.display.set_mode((500, 250))
board.fill((255, 255, 255))  # Clear the board

# Parking position
xp = 350
yp = 120

# Top-left corner of board
x0 = 205
y0 = 110

# Size of cell
dx = 30
dy = 30

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

# Main

# Main loop
for row in range(3):
    for col in range(3):

        print()
        print(row, col)

        # Calculate sequence of coordinates for each cell
        moves = calc_move_coords(row, col)

        # Iterate over sequence
        for i in range(len(moves[0])):
            x1, y1, x2, y2, pen = [moves[j][i] for j in range(len(moves))]

            print(x1, y1, x2, y2, pen)

            # Draw line
            if pen == 1:
                pygame.draw.line(board, (0, 0, 0), (x1, y1), (x2, y2), 2)

            # Call function to translate coordinates to angles
            # <function here>

            # Update display
            pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

# Quit Pygame
pygame.quit()