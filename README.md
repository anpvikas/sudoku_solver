# sudoku_solver
Sudoku Solver implemented in Python, using NumPy

# Sudoku Solver


This ReadME file explains the approach taken in order to write a program in python language to solve sudoku puzzles of varying difficulty levels. The submitted code is an attempt to implement the Constraint Satisfaction Problem algorithm using the backtracking method from the text-book (Russell, S., and Norvig, P. 2009. . Artificial Intelligence: a modern approach. Pearson).

On a broader level, the code has been divided into groups of functions as shown below:
1. Variables (Blank Cells) Related Functions
2. Domain Calculation Functions
3. Constraint Check Functions
4. Backtrack Related Functions
5. Inference Related Functions
6. Main Function 


The first step towards solving a sudoku puzzle is to identify all the variables (blank-cell), in this case, all the cells with value 0 assinged on the board. Various small functions have been written to extract the information about all the variables occuring on the board, in a specific row, column and box. The basic idea for implementing these functions was to get the whole board, row, column or box and then identify the cells where the assigned value is 0, and append them into a list as tuples having the co-ordinates of each variable. Example - code to get the row variables: 

```
def get_row_variables(board, row, column):
    row_variables = []
    row_vars = np.where(board[row, :] == 0)

    for i in range(len(row_vars[0])):
        row_variables.append((row, row_vars[0][i]))

    return row_variables
```

Below is the list of functions written to fetch details about the sudoku board variables (Variables Related Functions):

| Function Name                            | Function Description                                                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| get_variables(board)                     | Takes board as input and returns position of all board variables (blank-cells) as a list-of-tuples of x and y co-ordinate |
| get_row_variables(board, row, column)    | Takes board and variable's position as input and returns position of all variables in a row as a list-of-tuples           |
| get_column_variables(board, row, column) | Takes board and variable's position as input and returns position of all variables in a column as a list-of-tuples        |
| get_box(board, row, column)              | Takes board and variable's position as input and returns corresponding 3*3 Box                                            |
| get_box_variables(board, row, column)    | Takes board and variable's position as input and returns position of all variables in a box as a list-of-tuples           |
  
<br>
The second step is to get the domains of the identified variables. For calculating the domains, the approach is similar to that of getting the details of variables. Various small functions were written to get the domains of variables occuring in a row, column or box, and then creating another function (get_variable_domain) which combines all of these domains into a single domain by taking numpy set instersections. Another funcion (get_domain) takes the board and list of variables and returns the list of domains for the input variables. A variable domain is defined initially that has values from 1 to 9 and the row, column and box domains are calculated using this domain variable by taking numpy set difference. Example - code to get row domain:

```
def get_row_domain(board, row):
    return np.setdiff1d(domain, board[row, :])
```
<br>

Below is the list of functions written to fetch the domains (Domain Calculation Functions):

| Function Name                           | Function Description                                                                                        |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| get_row_domain(board, row)              | Takes board and variable's row as input and returns a list of domain values for the given row               |
| get_column_domain(board, column)        | Takes board and variable's column as input and returns a list of domain values for the given column         |
| get_box_domain(board, row, column)      | Takes board and variable's row & column as input and returns a list of domain values for the given box      |
| get_variable_domain(board, row, column) | Takes board and variable's row & column as input and returns a list of domain values for the given variable |
| get_domain(board, variables)            | Takes board and variables as input and returns a list of domain values for the given variables              |

<br>
After finding variables and calculating their domains, next step is to check the constraints for row, column and box. These functions return either true or false and tell whether a domain value can be assigned to a variable or not, by checking row, column and box constraints (of not repeating a value in a row, column and box). Separate fucntions have been written to check the row, column and box onstraints and a function (check_constraints) has been written to combine all the constraints and apply these combined constraints over a given row-column position on the board. Another function (check_board) has been written to verify if the board satisfies all the constraints. Example - code to check row constraints:

```
def check_row_constraint(board, row, column):
    row_data = board[row, :]
    count = len(row_data[row_data == board[row, column]])

    return count == 1
```
<br>

Below is the list of functions written to check the constraints (Constraints Check Functions):
| Function Name                               | Function Description                                                                                                  |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| check_row_constraint(board, row, column)    | Takes board and row, column as input and returns True or False by checking row constraints                            |
| check_column_constraint(board, row, column) | Takes board and row, column as input and returns True or False by checking column constraints                         |
| check_box_constraint(board, row, column)    | Takes board and row, column as input and returns True or False by checking box constraints                            |
| check_constraints(board, row, column)       | Takes board and row, column as input and returns True or False by checking all row, column and box constraints        |
| check_board(board)                          | Takes board as input and returns True or False by checking all values on the board calling check_constraints function |

<br>

Having minimum required functionalities in place, next step is to start with the implementation of backtracking algorithm. The algorithm steps are commented in the submitted code as well to display the flow of code execution as per the algorithm.  
<br>
To begin with the backtracking algorithm, first it is required to declare a backtrack function which takes board, variables, domains as input and either returns a solution or failure. Inside the funciton body, first check if there are any variables left to assign domain value or not. If all the variables have been assigned a domain value then it means the board can be returned as solution. Next step is to select an unassigned variable for which MRV (minimum-remaining-values) is implemented, which chooses the variable with least domain values associated. After the variable has been selected, iterate over all of its domain values to make domain value assignments. But there is a condition before assignment, that the assignment must be consistent. To check the consistency of assignment, a function (check_constraints_before_assignment) is written which takes board, row, column and value (domain value to be assigned) as input and returns True or False after checking all the constraints for domain value assignment before making actual assignment. If the function (check_constraints_before_assignment) returns True, then the domain value is assigned on the board. This function (check_constraints_before_assignment) is again a combination of three other functions (check_row_contraint_before_assignment, check_column_constraint_before_assignment, and check_box_constraint_before_assignment) which are written to check the row, column and box constraints before making the assignment. Example - code to check row constraints before assignment:

```
def check_row_contraint_before_assignment(board, row, value):
    row_data = board[row, :]
    return len(row_data[row_data == value]) == 0
```

Below is the list of functions written related to backtrack (Backtrack Related Functions):
| Function Name                                                     | Function Description                                                                                             |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| check_row_contraint_before_assignment(board, row, value)          | Takes board, row, value as input and returns True or False by checking row constraints                           |
| check_column_constraint_before_assignment(board, column, value)   | Takes board, column, value as input and returns True or False by checking column constraints                     |
| check_box_constraint_before_assignment(board, row, column, value) | Takes board, row, column, value as input and returns True or False by checking box constraints                   |
| check_constraints_before_assignment(board, row, column, value)    | Takes board, row, column, value as input and returns True or False by checking all constraints before assignment |
| backtrack(board, variables, domains)                              | Takes board, variables, domains as input and returns a solution or failure                                       |

<br>
After making assignment, inferences can be made for this assignment of domain value, which is done by writing another function (get_inference). The function (get_inference) takes a copy of current board, row, column and assigned value as input and then tries to make inferences in order to solve the puzzle. The purpose of the function (get_inference) is to check the consequences of assigning the value on the board and tell what values can now be placed in the connected variables. Connected variables refers to the variables present in the row, column or box of the variable which is assgined in the aglorithm's previous step. This raises a new requirement to write functions to get the connected variables and their domains. Two functions (get_connected_variables and get_connected_variables_domain) are written to get these details. The reason for writing get_inferences function is to check if there are any single values that can be directly assigned to the connected variables after the assignment made in the previous step of the algorithm. This is the place to implement forward checking, which is a way to get the inference one step ahead. 
Example - code to get the connected variables:

```
def get_connected_variables(board, row, column):
    connected_vars = []
    connected_variables = np.array([])

    # Creating single list of tuples of row, column and box variables
    connected_vars = get_row_variables(board, row, column) + get_column_variables(
        board, row, column) + get_box_variables(board, row, column)

    # Converting to numpy array and returning unique numpy array
    connected_variables = connected_vars

    return np.unique(connected_variables, axis=0)
```

Below is the list of funcitons written related to inferences(Inference Related Functions):

| Function Name                                       | Function Description                                                                            |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| get_connected_variables(board, row, column):        | Takes board and row, column as input and returns combined list of tuples of connected variables |
| get_connected_variables_domain(board, row, column): | Takes board and row, column as input and returns combined domain of all connected variables     |




The flow of code execution for getting inferences is presented below: 

- Make assignment of the consistent value to the board in the previous step, and 
- Once the assignment is made, call the inferences method to check for those variables to which single values can be directly assigned and store them in a queue to return to the calling function (bactrack)
- Now do a forward checking by iterating over the collected single values to find more single values in their connected variables. 
- Once the inferences from the assignment and the inferences from forward checking are done, return the list of inferences (containing single values, which is a tuple of variable position and domain value) to the calling function (backtrack).

This is a repeating process of collecting single values for the connected variables of connected variables by iterating over the previously collected single values.
The aim is to collect as many single values as it can to make the domain value assignment to variables easy, which will result in solving the sudoku puzzle.  


Once the inferences list is received by the calling function (backtrack), and if there are values in the list, an iteration is perfomed over each value in the inference list and assignments are made to the board variables. After each assignment the get_variables and get_domain functions are called which get the new reduced list of variables and domains after the assignment was made. Now the backtrack function is called recursively to process the new reduced list of variables and domains. The result is returned as solution if it is not a failure , else failure is returned (-1 in failure case) and all the assigned value from inferences are reverted back to 0.



Finally, we need a funciton which returns the bactrack function and it gets called by the main function (sudoku_solver) which executes the program.

### Code execution flow:

1. sudoku_solver(sudoku) CALLS solve_by_backtrack(sudoku, variables, domains)

2. solve_by_backtrack(sudoku, variables, domains) RETURNS backtrack(board, variables, domains)

3. backtrack(board, variables, domains)
   - Takes all the board variables and their domains as input 
   - Return board if all vairables are assinged
   - Selec the variable with least domain values by implementing MRV
   - Iterate over the domain values of the selected variable
     - Check all the constraints before assigning value to a variable
     - Assign value to the board variable
     - Create a copy of the board to pass to get inference function
       - Get the connected variables
       - Get the connected variable's domains
       - Iterate over the domains to collect single values
       - Iterate over single value 
         - Add them to inferences list
         - Assign values to the board copy
         - Get the new list of connected variables and domains
           - Iterate over the the connected variable's domains of the single_values
             - If more single values found then add to the single values list
     - Backtrack function receives the inferences list
     - Iterate over the inferences list to make value assignments to the variables
     - Get the new reduced list of variables and domains and recursively call the backtrack method
     - Return the result solution if not failure, else, revert the values assigned by inferences to 0 
