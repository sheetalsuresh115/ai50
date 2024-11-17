My work on CS50’s Introduction to AI with Python
https://cs50.harvard.edu/ai/

This course explores the concepts and algorithms at the foundation of modern artificial intelligence, diving into the ideas that give rise to technologies like game-playing engines, handwriting recognition, and machine translation. Through hands-on projects, students gain exposure to the theory behind graph search algorithms, classification, optimization, reinforcement learning, and other topics in artificial intelligence and machine learning as they incorporate them into their own Python programs. By course’s end, students emerge with experience in libraries for machine learning as well as knowledge of artificial intelligence principles that enable them to design intelligent systems of their own.


Notes : for future reference

Lecture 0: Search
Concepts
Agent: entity that perceives its environment and acts upon that environment.
State: a configuration of the agent and its environment.
Actions: choices that can be made in a state.
Transition model: a description of what state results from performing any applicable action in any state.
Path cost: numerical cost associated with a given path.
Evaluation function: function that estimates the expected utility of the game from a given state.

Algorithms
DFS (depth first search): search algorithm that always expands the deepest node in the frontier.
BFS (breath first search): search algorithm that always expands the shallowest node in the frontier.
Greedy best-first search: search algorithm that expands the node that is closest to the goal, as estimated by an heuristic function h(n).
A* search: search algorithm that expands node with lowest value of the "cost to reach node" plus the "estimated goal cost".
Minimax: adversarial search algorithm.

Projects
1. Degrees
2. Tic-Tac-Toe
