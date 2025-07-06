# 🧠 Maze Solver Robot Simulation 🔍🤖

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green?logo=pygame)
![Platform](https://img.shields.io/badge/Platform-Mac%20%7C%20Windows%20%7C%20Linux-lightgrey)

> An interactive robot simulation built in Python using **Pygame**. It simulates a robot exploring a maze **blind**, mapping it, and solving it using **A*** path planning in real-time with animations and dual-grid visualization.

---

## Features

- Dual Grid Visualization (Real Maze vs Robot’s Perspective)
- Randomized **Maze Generation** 
- **Blind Exploration** via BFS-like frontier expansion
- **A*** Pathfinding Algorithm for optimal path planning
- Fully animated robot movement and UI elements
- **Keyboard control scheme**

---

## Controls (Also rendered on screen)

| Key | Action              |
|-----|---------------------|
| `E` | Explore the maze (blind robot scan) |
| `P` | Plan shortest path using A*        |
| `R` | Reset and regenerate the maze       |

---

## Algorithms Implemented

- **Randomized DFS** for maze generation (with odd-index carving)
- **Breadth-First Search** style for blind exploration mapping
- **A* (A-Star) Search** for pathfinding with Manhattan heuristic
- **Node-based Grid System** for clean animation

---

 ## How It Works

1. Grid Setup
A 25x25 grid is drawn twice: one represents the actual maze and the other is the robot's discovered map.

2. Maze Generation
Randomized DFS creates a fully connected maze with start and end nodes chosen at random (odd indices only).

3. Robot Exploration
The robot "sees" only what's immediately around it, maps walls, and discovers the environment using BFS.

4. Path Planning
Once the environment is mapped, the A* algorithm computes the shortest path from start to end.

5. Dual Visualization
The left grid shows the real maze; the right shows what the robot discovers.

---

## Concepts Covered

- Graph traversal and pathfinding
- Heuristic search (Manhattan distance)
- Robotics mapping (SLAM-style logic without sensors)
- Visualization and simulation in Pygame

---

 ## Future Enhancements

- Diagonal movement support (if a certain robot supports it
- Weighted cells or terrain cost
- Obstacle dynamics (moving walls/obstacles)
- Custom map loading
