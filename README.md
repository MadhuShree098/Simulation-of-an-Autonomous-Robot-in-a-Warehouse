# Simulation-of-an-Autonomous-Robot-in-a-Warehouse
This project demonstrates an autonomous robot navigating a 10x10 meter rectangular warehouse environment using Python and the Pygame library.

1. **Overview**
The robot moves from an initial position (0, 0) to the destination (7, 9), adhering to specified constraints, such as movement speed, pause duration, obstacle avoidance, and boundary limits.

**2.	Constraints & Specifications:**
1.	Warehouse Dimensions: 10 x 10 meters.
2.	Robot Speed: 0.1 meters per second.
3.	Movement Duration: 0.1 seconds followed by a 2-second pause after each move.
4.	Obstacle: The robot detects and navigates around randomly placed obstacles.
5.	Pathfinding: The robot calculates the shortest path to its destination, using A* search algorithm to avoid obstacles efficiently.
6.	Boundary Constraints: The robot remains within the warehouse boundaries at all times.
7.	Simulation and Display: Visual representation of the warehouse, robot movement, obstacles, elapsed time, and completion message.

**3.	Libraries and Dependencies:**The following libraries are used in this project:
Pygame: For graphical simulation, visualization of the robot, obstacles, and warehouse layout.
Random: To randomly place obstacles in different locations each time the program runs.
Time: To manage timing and delays for movement and pauses.
Math: For calculations involving movement and distance.
Heapq: For implementing the priority queue in the A* algorithm, optimizing pathfinding.

**4.	Program Enhancements and Features:**
This implementation includes several enhancements beyond basic movement:
A.	A* Algorithm for Pathfinding:
The A* algorithm calculates the shortest path from the start to the destination while avoiding obstacles.
It optimizes movement to reduce time and ensure efficient navigation in a constrained warehouse environment.
B.	Randomized Obstacles:
Obstacles are randomly generated each time the simulation is run, increasing the challenge and realism of pathfinding.
Obstacles are represented as smaller green squares, distinct from the robot and destination.
C.	Elapsed Time Display:
The time elapsed since the simulation started is displayed in the window.
This feature provides a clear measure of simulation progress and robot efficiency.
D.	"Destination Reached!" Display:
Upon reaching the destination, the program displays a "Destination Reached!" message in the centre of the window.
This message remains visible for 5 seconds before the program automatically exits.

**5.	Pseudocode and Logic Breakdown:**
* The following pseudocode summarizes the overall logic and flow of the program:
 1. Initialize the warehouse, robot, and display with constants and Pygame settings.
 2. Generate random obstacles within warehouse boundaries, avoiding start and destination points.
 3. Define the A* pathfinding algorithm to calculate the shortest path while avoiding obstacles.
 4. Main simulation loop:
Move the robot one step toward the target along the calculated path.
Pause for 2 seconds after each step.
Detect obstacles and recalculate path if blocked.
 5. Display elapsed time and robot’s position.
 6. Upon reaching the destination:
Display "Destination Reached!" for 5 seconds.
End the simulation.


**6.	Conclusion:**

This Python simulation successfully models an autonomous robot navigating a warehouse while adhering to specified constraints. By incorporating A* pathfinding and random obstacles, I have ensured that the robot can intelligently avoid obstacles and find the shortest path to its destination. The inclusion of real-time time tracking, a destination reached message, and the ability to handle random obstacles further enhances the simulation’s realism and functionality.

