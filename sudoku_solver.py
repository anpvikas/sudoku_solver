import numpy as np


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    # YOUR CODE HERE

    variables = get_variables(sudoku)
    domains = get_domain(sudoku, variables)

    solved_sudoku = solve_by_backtrack(sudoku, variables, domains)

    if not check_board(sudoku):
        sudoku.fill(-1)
        return sudoku

    if isinstance(solved_sudoku, int):
        sudoku.fill(-1)
        return sudoku

    return solved_sudoku


domain = np.arange(1, 10)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                        MAIN FUNCTION                       #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


def solve_by_backtrack(board, variables, domains):
    return backtrack(board, variables, domains)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                       BACTRACK FUNCTION                    #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#------------------------------------------------------------#
#         Function to find solution or return failure        #
#------------------------------------------------------------#
#  - Takes board, variables and domains as input             #
#  - Returns a solution or failure                           #
#------------------------------------------------------------#


#----------------------------Algorithm------------------------------#
# function BACKTRACK(assignment, csp) return a solution or failure  #
# ------------------------------------------------------------------#
def backtrack(board, variables, domains):

    # Define failure as -1
    failure = -1

    #---------------------Algorithm----------------------#
    #  if assignment is complete then return assignment  #
    #----------------------------------------------------#
    # Return board if all vairables are assinged
    if len(variables) == 0:
        return board

    # Last variable to assign
    if len(variables) == 1:
        row, column = variables[0]
        board[row, column] = domains[0][0]
        return board

    #--------------Algorithm---------------#
    # var ← SELECT_UNASSIGNED_VARIABLE(csp) #
    # -------------------------------------#
    # Implementing MRV by selecting the variable with least domain values
    min_len = min(map(len, domains))
    for i, domain in enumerate(domains):
        if len(domain) == min_len:
            variable = variables[i]
            # Unpacking variable
            row, column = variable
            # Selected variable's domain
            domain_values = domain
            break

    #---------------------------Algorithm----------------------------#
    # for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do #
    #----------------------------------------------------------------#
    # Iterating over the domain values of the selected variable
    for value in domain_values:
        # List to hold the inferences
        inferences = []

        #-----------------Algorithm-------------------#
        # if value is consistent with assignment then #
        #---------------------------------------------#
        # Checking all the constraints before assigning value to a variable
        if check_constraints_before_assignment(board, row, column, value):

            #------------Algorithm------------#
            # add {var=value} to assignment   #
            #---------------------------------#
            # Assigning value to the board variable
            board[row, column] = value
            # Creating a copy of the board to pass to inference function
            board_cpy = board.copy()

            #----------------Algorithm----------------#
            # inferences ←INFERENCE(csp, var , value) #
            #-----------------------------------------#
            # Passing the board copy to the get inferences
            inferences = get_inference(board_cpy, row, column, value)

            #---------------Algorithm-----------------#
            # if inferences != failure then           #
            #-----------------------------------------#
            if inferences != failure:
                for inference in inferences:
                    variable, variable_value = inference
                    #-----------Algorithm----------#
                    # add inferences to assignment #
                    #------------------------------#
                    board[variable[0], variable[1]] = variable_value[0]

                variables = get_variables(board)
                domains = get_domain(board, variables)

                #-------------Algorithm--------------#
                # result ← BACKTRACK(assignment, csp) #
                #------------------------------------#
                result = backtrack(board, variables, domains)

                #---------Algorithm----------#
                # if result != failure then  #
                #    return result           #
                #----------------------------#
                if not isinstance(result, int):
                    return result

        #---------------------Algorithm-----------------------#
        # remove {var = value} and inferences from assignment #
        #-----------------------------------------------------#
        board[row, column] = 0
        if isinstance(inferences, int):
            return -1
        for inference in inferences:
            variable, variable_value = inference
            board[variable[0], variable[1]] = 0

    #----Algorithm----#
    # return failure  #
    #-----------------#
    return failure

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                 INFERENCE RELATED FUNCTIONS                #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#------------------------------------------------------------#
#     Function to get all inferences of a board variable     #
#------------------------------------------------------------#
#  - Takes board, row, column, value at row-column as input  #
#  - Returns a list of tuples with variable's position       #
#    and domains                                             #
#------------------------------------------------------------#


def get_inference(board, row, column, value):
    failure = -1

    # List to hold the inferences
    inferences = []
    # List to hold all the single values that can be directly assigned
    single_values = []

    # Getting the connected variables
    variables = get_connected_variables(board, row, column)
    # Getting the connected variable's domains
    domains = get_connected_variables_domain(board, row, column)

    # Iterating over the domain
    for i, domain in enumerate(domains):
        variable = variables[i]
        # Unpacking row and column from variable
        row, column = variable

        # Checking if the domian has single value and appending to the single_values list
        if len(domains[i][0]) == 0:
            return -1

        if len(domain[0]) == 1:
            single_values.append((variable, domain))

    # Iterating over the single_values list
    while len(single_values) != 0:
        s_value = single_values.pop(0)
        # Unpacking variable and domain as s_var and s_val
        s_var, s_val = s_value
        # Unpacking s_var as row and column
        row, column = s_var

        # Adding single values to the inferences list
        inferences.append((s_var, s_val))
        # Assinging the value to the board
        board[row, column] = s_val[0]

        #------------------------------#
        # Implementing forward checking#
        #------------------------------#
        # Getting the connected variables of the single_values
        variables = get_connected_variables(board, row, column)
        # Getting the connected variable's domains of the single_values
        domains = get_connected_variables_domain(board, row, column)

        # Iterating over the the connected variable's domains of the single_values
        for domain in domains:
            # If the domain is emoty then return blank list
            if len(domain[0]) == 0:
                return []
            # If the domain has single value then append it to single_values list
            if len(domain[0]) == 1:
                single_values.append((variable, domain))

        break
    return inferences

#------------------------------------------------------------#
#  Function to get all connected variable's combined domain  #
#------------------------------------------------------------#
#  - Takes board and variables's position as input           #
#  - Returns combined domain of all connected variables      #
#    Connected variables means all the variables in the      #
#    respective row, column and box for a given variable     #
#    position                                                #
#------------------------------------------------------------#


def get_connected_variables_domain(board, row, column):
    domain = []
    variables = get_connected_variables(board, row, column)
    for variable in variables:
        row = variable[0]
        column = variable[1]
        var = [(row, column)]

        domain.append(get_domain(board, var))

    return domain


#------------------------------------------------------------#
#           Function to get all connected variables          #
#------------------------------------------------------------#
#  - Takes board and variables's position as input           #
#  - Returns combined list of tuples of connected variables  #
#    Connected variables means all the variables in the      #
#    respective row, column and box for a given variable     #
#    position on board                                       #
#------------------------------------------------------------#


def get_connected_variables(board, row, column):
    connected_vars = []
    connected_variables = np.array([])

    # Creating single list of tuples of row, column and box variables
    connected_vars = get_row_variables(board, row, column) + get_column_variables(
        board, row, column) + get_box_variables(board, row, column)

    # Converting to numpy array and returning unique numpy array
    connected_variables = connected_vars

    return np.unique(connected_variables, axis=0)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                 BACKTRACK RELATED FUNCTIONS                #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#------------------------------------------------------------#
#     Function to check all constraints before assigning     #
#     a variable value on the board                          #
#------------------------------------------------------------#
#  - Takes board, row, column, value at row-column as input  #
#  - Returns True/ False after checking all constraints      #
#------------------------------------------------------------#


def check_constraints_before_assignment(board, row, column, value):
    return np.all([check_row_contraint_before_assignment(board, row, value),
                   check_column_constraint_before_assignment(
        board, column, value),
        check_box_constraint_before_assignment(
        board, row, column, value)])

#------------------------------------------------------------#
#     Function to check Row constraints before assigning     #
#     a variable value on the board                          #
#------------------------------------------------------------#
#  - Takes board, row, value as input                        #
#  - Returns True/ False after checking row constraints      #
#------------------------------------------------------------#


def check_row_contraint_before_assignment(board, row, value):
    row_data = board[row, :]
    return len(row_data[row_data == value]) == 0

#------------------------------------------------------------#
#     Function to check Column constraints before assigning  #
#     a variable value on the board                          #
#------------------------------------------------------------#
#  - Takes board, column, value as input                     #
#  - Returns True/ False after checking column constraints   #
#------------------------------------------------------------#


def check_column_constraint_before_assignment(board, column, value):
    column_data = board[:, column]
    return len(column_data[column_data == value]) == 0


#------------------------------------------------------------#
#     Function to check Box constraints before assigning     #
#     a variable value on the board                          #
#------------------------------------------------------------#
#  - Takes board, row, column as input                       #
#  - Returns True/ False after checking box constraints      #
#------------------------------------------------------------#
def check_box_constraint_before_assignment(board, row, column, value):
    box_data = get_box(board, row, column)
    return len(box_data[box_data == value]) == 0


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#         VARIABLES (BLANKS CELLS) RELATED FUNCTIONS         #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#------------------------------------------------------------#
#              Function to get all board variables           #
#------------------------------------------------------------#
#  - Takes board as input                                    #
#  - Returns a list of tuples with variable's position       #
#------------------------------------------------------------#

def get_variables(board):

    return np.array(list(zip(np.where(board == 0)[0], np.where(board == 0)[1])))


#------------------------------------------------------------#
#               Function to get Row variables                #
#------------------------------------------------------------#
#  - Takes board and variables's position as input           #
#  - Returns list of tuples of row variables                 #
#------------------------------------------------------------#


def get_row_variables(board, row, column):

    row_variables = []
    row_vars = np.where(board[row, :] == 0)

    for i in range(len(row_vars[0])):
        row_variables.append((row, row_vars[0][i]))

    return row_variables

#------------------------------------------------------------#
#               Function to get Column variables             #
#------------------------------------------------------------#
#  - Takes board and variables's position as input           #
#  - Returns list of tuples of column variables              #
#------------------------------------------------------------#


def get_column_variables(board, row, column):

    column_variables = []
    col_vars = np.where(board[:, column] == 0)

    for i in range(len(col_vars[0])):
        column_variables.append((col_vars[0][i], column))

    return column_variables

#------------------------------------------------------------#
#                Function to get Box variables               #
#------------------------------------------------------------#
#  - Takes board and variables's position as input           #
#  - Returns list of tuples of box variables                 #
#------------------------------------------------------------#


def get_box_variables(board, row, column):
    box_variables = []

    for x in range(3*(row//3), 3+3*(row//3)):
        for y in range(3*(column//3), 3+3*(column//3)):
            if board[x, y] == 0:
                box_variables.append((x, y))

    return box_variables


#------------------------------------------------------------#
#                Function to identify 3*3 Box                #
#------------------------------------------------------------#
#  - Takes board and variables's position as input           #
#  - Returns box for the given variable's position           #
#------------------------------------------------------------#
def get_box(board, row, column):
    return board[3*(row//3):3+3*(row//3), 3*(column//3):3+3*(column//3)]


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                 DOMAIN CALCULATION FUNCTIONS               #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#------------------------------------------------------------#
#        Function to get domain of all board variables       #
#------------------------------------------------------------#
#  - Takes board and board variables as input                #
#  - Returns a list of domains for all input variables       #
#------------------------------------------------------------#
def get_domain(board, variables):
    domain = []
    for variable in variables:
        row, column = variable
        domain.append(get_variable_domain(board, row, column))

    return domain

#------------------------------------------------------------#
#              Function to get a variable's domain           #
#------------------------------------------------------------#
#  - Takes board and variable's position as input            #
#  - Returns a list of combined domains for given variable   #
#    by taking intresection of row, column and box domains   #
#------------------------------------------------------------#


def get_variable_domain(board, row, column):

    intersection_row_column = np.intersect1d(
        get_row_domain(board, row), get_column_domain(board, column))
    return np.intersect1d(intersection_row_column, get_box_domain(board, row, column))

#------------------------------------------------------------#
#                 Function to get Row domain                 #
#------------------------------------------------------------#
#  - Takes board and variable's row as input                 #
#  - Returns a list of domains for given varialbe by taking  #
#    set difference of domain and row                        #
#------------------------------------------------------------#


def get_row_domain(board, row):
    return np.setdiff1d(domain, board[row, :])


#------------------------------------------------------------#
#                 Function to get Column domain              #
#------------------------------------------------------------#
#  - Takes board and variable's column as input              #
#  - Returns a list of domains for given varialbe by taking  #
#    set difference of domain and column                     #
#------------------------------------------------------------#
def get_column_domain(board, column):

    return np.setdiff1d(domain, board[:, column])

#------------------------------------------------------------#
#                  Function to get Box domain                #
#------------------------------------------------------------#
#  - Takes board and variable's row and column as input      #
#  - Returns a list of domains for given varialbe by taking  #
#    set difference of domain and box                        #
#------------------------------------------------------------#


def get_box_domain(board, row, column):
    box = get_box(board, row, column)
    return np.setdiff1d(domain, box)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                 CONSTRAINTS CHECK FUNCTIONS                #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#------------------------------------------------------------#
#             Function to check Board constraints            #
#------------------------------------------------------------#
#  - Takes board as input                                    #
#  - Returns true or false, after checking all constraints   #
#------------------------------------------------------------#


def check_board(board):
    rows, columns = board.shape
    for row in range(rows):
        for column in range(columns):
            if not check_constraints(board, row, column):
                return False

    return True

#------------------------------------------------------------#
#    Function to check Row, Column and Board constraints     #
#------------------------------------------------------------#
#  - Takes board, row and column as input                    #
#  - Returns true or false for combined constraints for      #
#    Row, Column and Box                                     #
#------------------------------------------------------------#


def check_constraints(board, row, column):
    return np.all([check_column_constraint(board, row, column),
                   check_row_constraint(board, row, column), check_box_constraint(
                       board, row, column)
                   ])

#------------------------------------------------------------#
#               Function to check Row constraints            #
#------------------------------------------------------------#
#  - Takes board, row and column as input                    #
#  - Returns true or false, if count == 1                    #
#------------------------------------------------------------#


def check_row_constraint(board, row, column):
    row_data = board[row, :]
    count = len(row_data[row_data == board[row, column]])

    return count == 1

#------------------------------------------------------------#
#            Function to check Column constraints            #
#------------------------------------------------------------#
#  - Takes board, row and column as input                    #
#  - Returns true or false, if count == 1                    #
#------------------------------------------------------------#


def check_column_constraint(board, row, column):
    column_data = board[:, column]
    count = len(column_data[column_data == board[row, column]])

    return count == 1

#------------------------------------------------------------#
#             Function to check Box constraints              #
#------------------------------------------------------------#
#  - Takes board, row and column as input                    #
#  - Returns true or false, if count == 1                    #
#------------------------------------------------------------#


def check_box_constraint(board, row, column):
    box_data = get_box(board, row, column)
    count = len(box_data[box_data == board[row, column]])

    return count == 1
