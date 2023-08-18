# IntelliHunt: The Operand Odyssey
# Vyom Devgan

import random
import re

def is_prime(n: int) -> bool:
    '''
    Checks if given integer (n) is prime.
    
    n (int): The number that is given which is checked.
    
    Returns a bool, indicating True if prime, False otherwise.
    '''
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def final_solution() -> int:
    '''
    Generates the final solution for the Nerdle.
    
    A random integer between 1 and 999 is chosen at random.
    That random integer is then checked for primality.
    If the random integer is prime, a new random integer is selected recursively until number is not prime.
    
    Returns a non prime integer between 1 and 999.
    '''
    solution_val = random.randint(1,999)
    if is_prime(solution_val):
        return final_solution
    return solution_val

def operator() -> str:
    '''
    Generates a random arithmetic operator.
    
    A random basic arithmetic operator is selected: addition (+), subtraction (-), multiplication (*), or division (/).
    
    Returns a string representing an arithmetic operator.
    '''
    operators = ['+','-','*','/'] # ['ADDITION', 'SUBTRACTION', 'DIVISION', 'MULTIPLICATION']
    return operators[random.randint(0,3)]
    
def find_solutions(number: int, operation: str) -> list:
    '''
    Generates a list of solutions given a non prime integer and an arithmetic operator.
    
    number (int): The target integer for which solutions need to be found.
    operation (str): The arithmetic operation to use ('+', '-', '*', or '/').
    
    Raises ValueError if an unsupported operation is provided.
    For the division operation, solutions are generated as numerator / denominator = number.

    Returns a list of strings representing solutions in the format "operand operator operand = number".

    Example:
        find_solutions(5, '+') could return ['0 + 5 = 5', '1 + 4 = 5', '2 + 3 = 5'].
    '''
    solutions = []
    if operation == '+':
        for i in range(number + 1):
            j = number - i
            solutions.append(f"{i} + {j} = {number}")
            if len(solutions) == ((number//2)+1):
                break
    elif operation == '-':
        for i in range(number, -1, -1):
            j = i - number
            solutions.append(f"{i} - {j} = {number}")
            if len(solutions) == ((number//2)+1):
                break
    elif operation == '*':
        for i in range(1, int(number ** 0.5) + 1):
            if number % i == 0:
                j = number // i
                solutions.append(f"{i} * {j} = {number}")
                if len(solutions) == ((number//2)+1):
                    break
    elif operation == '/':
        for i in range(1, number + 1):
            j = i * number
            solutions.append(f"{j} / {i} = {number}")
            if len(solutions) == ((number//2)+1):
                break
    return solutions

def solution_finder(final_answer: int, final_operator: str) -> tuple:
    '''
    Finds a solution for a given answer and operator, or regenerate new values and find solutions if an error occurs.
    
    final_answer (int): The target answer for which a solution needs to be found.
    final_operator (str): The arithmetic operator to use ('+', '-', '*', or '/').
    
    Finds a solution for the given final answer and operator using the find_solutions function.
    If the initial attempt fails, new values are generated to ensure a solution can be found.
    
    Returns a tuple that contains the final answer, final operator, and a randomly selected solution string.

    Example:
        solution_finder(10, '+') could return (15, '+', '5 + 10 = 15').
    '''
    try:
        solutions = find_solutions(final_answer, final_operator)
        solve = solutions[random.randint(0,len(solutions)-1)]
    except:
        final_answer = final_solution()
        final_operator = operator()
        solutions = find_solutions(final_answer, final_operator)
        solve = solutions[random.randint(0,len(solutions)-1)]
    return final_answer, final_operator, solve

def eval_check(correct_ans: str, guessed_ans: str) -> bool:
    '''
    Checks if a guessed arithmetic expression evaluates to the correct answer.
    
    correct_ans (str): The correct arithmetic expression in the format "operand operator operand = result".
    guessed_ans (str): The guessed arithmetic expression in the same format as correct_ans.
    
    This function takes a  and a guessed expression as input.
    It evaluates both the correct arithmetic and guessed arithmetic expressions and compares the results to determine if the guessed expression is correct.
    
    Returns a bool, indicating True if the guessed expression evaluates to the correct answer, False otherwise.

    Example:
        eval_check('2 + 3 = 5', '1 + 4 = 5') could return True.
    '''
    solved = correct_ans.split('=')[0]
    guessed = guessed_ans.split('=')[0]
    if eval(solved) == eval(guessed):
        return True
    return False

def solution_checker(correct_ans: str, guessed_ans: str) -> None:
    '''
    Checks guessed arithmetic expression against the correct answer.
    
    correct_ans (str): The correct arithmetic expression in the format "operand operator operand = result".
    guessed_ans (str): The guessed arithmetic expression in the same format as correct_ans.
    
    Identifies correct and incorrect elements by comparing the guessed expression against the correct.
    It also tracks and updates green_list and red_list, which provide information to the player about which integers are in the solution.

    Example:
        solution_checker('2 + 3 = 5', '3 + 1 = 4') would provide feedback about correct and incorrect elements.
    '''
    if eval_check(correct_ans, guessed_ans):
        return 'YOU WIN'
    
    solution_numbers = re.findall(r'\d+', correct_ans)
    solution_result = ''.join(''.join(number) for number in solution_numbers)
    guessed_numbers = re.findall(r'\d+', guessed_ans)
    guessed_result = ''.join(''.join(number) for number in guessed_numbers)
    for i in guessed_result:
        if i in solution_result and i not in green_list:
            green_list.append(i)
            solution_result.replace(i,'')
        else:
            if i not in red_list and i not in green_list:
                red_list.append(i)
    return

def hinter(hints: int) -> str:
    '''
    Provides hints depending on the amount of hints remaining.

    hints (int): The remaining hints count for the player.

    The hints help players get closer to finding the solution to the arithmetic expression.

    Returns a string with a hint message based on the provided hints count.

    Example:
        hinter(1) could return "The operation used in the expression is +."
    '''
    if hints == 0:
        return f'\nThe final answer is of length: {str(len(str(final_answer)))}.\nMeaning there are {str(len(str(final_answer)))} digits in the solution to the expression.'
    elif hints == 1:
        return f'\nThe operation used in the expression is {str(final_operator)}.'
    elif hints == 2:
        return f'\nThe whole solution has this many characters: {str(len(solve))} No Spaces'
    return 'You are out of Hints! Sorry!'

def game() -> str:
    '''
    Play Vyom's Math Game.
    
    Main game loop for Vyom's Math Game. Players need to guess a valid mathematical expression
    that evaluates to the correct answer. They have a limited number of guesses and can use hints to aid their guesses.
    
    Players need to follow rules and hints to come up with a valid mathematical expression.
    
    Hints provide information about correct and incorrect elements in the solution.
    
    Players are allowed a maximum of 3 hints.
    
    Returns a string, message indicating whether the player won or lost the game.

    Example:
        game() could return "You Win!" if the player guesses the correct expression.
    '''
    print('Welcome to Vyom\'s Math Game.'
          '\nIn this game you will have to come up with a mathematical expression that is true.'
          '\nYou will be given 5 tries to guess the whole soltuion.\n'
          '\nHere is some additional information before you begin playing:'
          '\n1. Each expression must be true and must make sense.'
          '\n2. Your solution must include at least two numbes, one operation and one solution.'
          '\n3. You are allowed 3 max hints.'
          '\n4. After each guess, you will be given some information to help you out; Lists of Green & Red'
          '\n5. The list of green numbers are numbers that exist in the correct solution. Meaning that you should use these numbers again in your next guess'
          '\n6. The list of red numbers are numbers that DO NOT exist in the correct solution. Meaning that you should NOT use these numbers again in your next guess')
    first_guess = input("Let\'s Begin!\nEnter your first guess: ").replace(' ','')
    if isinstance(solution_checker(solve, first_guess), str):
        return 'You Win!'
    
    hints = 0
    guesses = 1
    while guesses <= 4:
        print(f'\nIncorrect Guess, here is some information:'
              f'\nThe numbers that are in the solution are: {green_list}'
              f'\nThe numbers that are NOT in the solution are {red_list}')
        next_guess = input('Enter your next guess: ').replace(' ','')
        if next_guess.lower() == 'hint':
            guesses -= 1
            print(hinter(hints))
            hints += 1
            
        elif isinstance(solution_checker(solve, next_guess), str):
            return 'You Win!'
        
        guesses += 1
            
    return "\nYou LOST\n"

if __name__ == "__main__":
    # Initialize game parameters
    final_answer = final_solution()
    final_operator = operator()
    green_list = []
    red_list = []
    
    # Generate solution
    final_answer, final_operator, solve = solution_finder(final_answer, final_operator)
    solve = solve.replace(' ','')
    if '--' in solve:
        solve.replace('--', '+')
        
    # Play the game and display results
    print(game())
    print(f'The correct solution was: {solve}.\n')
    input('Thanks for playing!. Press any key to exit.')
