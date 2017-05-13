# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

A: Adding a new constraint: No squares in the same unit, outside the two naked twins squares, can contain the twin values

1. Given the rules of Sudoku, each unit can contain only one instance of a digit.
2. The Naked Twins represents two boxes from the same unit that permit the same two values.
3. Given that one of the twins will take first value, and the other the second,
all the other boxes from that unit are not permitted to use them.
4. If a Naked Twins Pair exists in a Unit, then we can infer that for all the other peers
from that unit, there is the constraint that they are not permitted to use the values of the naked twins.
5. So we eliminate the naked twins values from the list of possible values of all the other boxes contained
in that particular unit.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Updating the primary constraint to: A digit must occur once and only once in each unit, including the diagonal ones.

1. Add the 2 new diagonal units to the unit list.
2. Then the primary constraint of Sudoku, must be applied to the 2 diagonal units also: a digit must occur once and only once in each unit.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

