import random
import re

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def final_solution() -> int:
    solution_val = random.randint(1,999)
    if is_prime(solution_val):
        return final_solution
    return solution_val

def operator() -> str:
        operators = ['+','-','*','/'] # ['ADDITION', 'SUBTRACTION', 'DIVISION', 'MULTIPLICATION']
        return operators[random.randint(0,3)]
    
def find_solutions(number: int, operation: str) -> list:
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
    solved = correct_ans.split('=')[0]
    guessed = guessed_ans.split('=')[0]
    if eval(solved) == eval(guessed):
        return True
    return False

def solution_checker(correct_ans: str, guessed_ans: str) -> None:
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
    if hints == 0:
        return f'\nThe final answer is of length: {str(len(str(final_answer)))}.\nMeaning there are {str(len(str(final_answer)))} digits in the solution to the expression.'
    elif hints == 1:
        return f'\nThe operation used in the expression is {str(final_operator)}.'
    elif hints == 2:
        return f'\nThe whole solution has this many characters: {str(len(solve))} No Spaces'
    return 'You are out of Hints! Sorry!'

def game():
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
    final_answer = final_solution()
    final_operator = operator()
    green_list = []
    red_list = []
    final_answer, final_operator, solve = solution_finder(final_answer, final_operator)
    solve = solve.replace(' ','')
    if '--' in solve:
        solve.replace('--', '+')
    print(game())
    print(f'The correct solution was: {solve}.\n')