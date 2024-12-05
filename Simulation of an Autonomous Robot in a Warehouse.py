Simport pygame
import time
import math
import random
import heapq

# Initialize pygame
pygame.init()

# Constants
WAREHOUSE_WIDTH, WAREHOUSE_HEIGHT = 10, 10  # in meters
SCALE = 60  # Scale factor to enlarge warehouse for display
WINDOW_WIDTH, WINDOW_HEIGHT = WAREHOUSE_WIDTH * SCALE, WAREHOUSE_HEIGHT * SCALE

ROBOT_SPEED = 0.1  # meters per second
MOVE_DURATION = 0.1  # seconds (time for each step)
STOP_DURATION = 2000  # 2000 milliseconds = 2 seconds
START_POSITION = (0, 0)  # Robot starts at (0, 0)
INTERMEDIATE_POSITION = (1, 1)  # First step to move away from (0,0) so it does not travel only in 0 coordinate
DESTINATION = (7, 9)

# Color Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # Color for obstacles

# Display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + 50))  # Extra space for timer display
pygame.display.set_caption("Robot Simulation")
font = pygame.font.Font(None, 36)  # Font for displaying time and messages

# Generate random obstacles inside the warehouse
def generate_obstacles(num_obstacles=5):
    obstacles = []
    while len(obstacles) < num_obstacles:
        x = random.randint(1, WAREHOUSE_WIDTH - 2)
        y = random.randint(1, WAREHOUSE_HEIGHT - 2)
        if (x, y) != START_POSITION and (x, y) != DESTINATION and (x, y) not in obstacles:
            obstacles.append((x, y))
    return obstacles

# Convert warehouse coordinates to pixel coordinates
def to_pixel_coords(position):
    return (position[0] * SCALE, WINDOW_HEIGHT - position[1] * SCALE)

# A* Pathfinding implementation
def a_star(start, end, obstacles):
    grid = [[0 for _ in range(WAREHOUSE_WIDTH)] for _ in range(WAREHOUSE_HEIGHT)]
    for obs in obstacles:
        grid[obs[1]][obs[0]] = 1  # Mark obstacle as blocked

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, end), 0, start))
    closed_list = set()
    came_from = {}
    g_score = {start: 0}
    
    while open_list:
        _, g, current = heapq.heappop(open_list)
        
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        closed_list.add(current)
        
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            
            if 0 <= neighbor[0] < WAREHOUSE_WIDTH and 0 <= neighbor[1] < WAREHOUSE_HEIGHT and neighbor not in closed_list and grid[neighbor[1]][neighbor[0]] != 1:
                tentative_g_score = g + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score, tentative_g_score, neighbor))
    
    return []  # No path found

# Initialize robot
robot_position = list(START_POSITION)

# Main Simulation Loop
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()  # Start time for the timer
destination_reached = False  # Flag to indicate if the robot has reached the destination
initial_wait_done = False  # Flag to track initial 2-second wait
initial_wait_time = 2000  # Initial wait time in milliseconds

# Generate obstacles randomly
obstacles = generate_obstacles()

# Find the shortest path to the destination using A*
path = [INTERMEDIATE_POSITION] + a_star(INTERMEDIATE_POSITION, DESTINATION, obstacles)

last_move_time = pygame.time.get_ticks()
is_paused = False
path_index = 0  # Track current position in the path

while running:
    current_time = pygame.time.get_ticks()

    # Check for events (for quitting)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Wait 2 seconds at the initial position before moving
    if not initial_wait_done:
        if current_time - start_time >= initial_wait_time:
            initial_wait_done = True  # Initial wait is over
            last_move_time = current_time  # Reset move time after initial wait

    # If not paused and the initial wait is done, move the robot
    if initial_wait_done and not is_paused and path and not destination_reached:
        target = path[path_index]
        delta_x = target[0] - robot_position[0]
        delta_y = target[1] - robot_position[1]

        distance = math.sqrt(delta_x**2 + delta_y**2)
        
        if distance < ROBOT_SPEED * MOVE_DURATION:
            # If robot reaches current target, move to next point in the path
            robot_position[0] = target[0]
            robot_position[1] = target[1]
            path_index += 1
            if path_index >= len(path):  # Destination reached
                destination_reached = True
                destination_time = pygame.time.get_ticks()  # Record the time of arrival
        else:
            # Move toward the target point
            step_x = (delta_x / distance) * ROBOT_SPEED * MOVE_DURATION
            step_y = (delta_y / distance) * ROBOT_SPEED * MOVE_DURATION
            robot_position[0] += step_x
            robot_position[1] += step_y
        
        last_move_time = current_time
        is_paused = True

    # Check if the robot should pause for 2 seconds
    if is_paused and current_time - last_move_time >= STOP_DURATION:
        is_paused = False  # End the pause

    # Clear screen
    window.fill(WHITE)

    # Draw warehouse boundaries
    pygame.draw.rect(window, BLACK, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 2)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(window, GREEN, (to_pixel_coords(obstacle)[0] - 5, to_pixel_coords(obstacle)[1] - 5, SCALE // 2, SCALE // 2))

    # Draw destination marker
    pygame.draw.circle(window, RED, to_pixel_coords(DESTINATION), 8)

    # Draw robot at its current position
    pygame.draw.circle(window, BLUE, to_pixel_coords(robot_position), 8)

    # Display the elapsed time
    elapsed_time = (current_time - start_time) / 1000  # Time in seconds
    time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, BLACK)
    window.blit(time_text, (10, WINDOW_HEIGHT + 10))  # Display below the warehouse

    # Display "Destination Reached" message if robot has reached the destination
    if destination_reached:
        message_text = font.render("Destination Reached!", True, RED)
        message_rect = message_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        window.blit(message_text, message_rect)

        # Check if 5 seconds have passed since reaching destination
        if current_time - destination_time >= 5000:
            running = False  # Exit the loop after 5 seconds

    # Update display
    pygame.display.flip()

    clock.tick(60)  # Run at 60 FPS

pygame.quit()
