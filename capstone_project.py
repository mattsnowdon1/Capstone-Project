from random import randint, sample
from rich.console import Console
import sys
console = Console(highlight=False)


def create_grid(n=5):
    '''Create an nxn grid and fill each row with a random number of values between 1-9.
    Positions not assigned a value will remain as 'None'
    Output: 2D list'''
    grid = [[None for _ in range(n)] for _ in range(n)]  # 2D grid of Nones
    for row in grid:
        # Random num of real values on that row
        num_real_in_row = randint(1, n)
        # List of random positions to put real values
        for pos in sample(range(0, n), num_real_in_row):
            row[pos] = {'val': randint(1, 9), 'real': True, 'found': False}

    return grid


def fill_grid(grid):
    '''Go through the 2D list and replace all of the 'None' values with random filler values'''
    for row in grid:
        for i, num in enumerate(row):
            if num == None:
                # row[i] = {'val': 0, 'real': False}
                row[i] = {'val': randint(1, 9), 'real': False}
    return grid


def get_sums(grid):
    '''Calculate the sum of actual values for each row and column
    Output: 2D list'''
    sums = [[], []]
    for rows in grid:
        row_sum = 0
        for num in rows:
            if num['real']:
                row_sum += num['val']
        sums[0].append(row_sum)

    for col_num in range(0, len(grid)):
        col_sum = 0
        for rows in grid:
            if rows[col_num]['real']:
                col_sum += rows[col_num]['val']
        sums[1].append(col_sum)

    return sums


def display_grid(grid, row_sums, col_sums):
    '''Display the current grid with row/column numbers and the sums of rows/columns '''
    console.print('   ', *[str(num).center(2)
                  for num in range(1, len(grid)+1)])
    console.print('  ┌' + '-'*3*len(grid) + '-┐')
    for i, row in enumerate(grid):
        nums_in_row = []
        # for num in row:
        #     nums_in_row.append(num['val'])
        # console.print(i+1, "|", *
        #               [f'{num:<2}' for num in nums_in_row], "|", f"[blue]{row_sums[i]}[/blue]")
        for num in row:
            val = str(num['val']).center(2)
            if num['real'] and num['found']:
                val = f'[bold green4]{val}[/bold green4]'
            nums_in_row.append(val)
        console.print(i+1, "|", *nums_in_row, "|",
                      f"[blue]{row_sums[i]}[/blue]")

    console.print('  └' + '-'*3*len(grid) + '-┘')
    console.print('   ', *[str(num).center(2)
                  for num in col_sums], style='blue')


def intro():
    console.print("Welcome!")
    choice = input("Would you like to see the game instructions? Yes or No ")
    if choice.lower() == "yes":
        console.print("""
[bold magenta]Instructions:[/bold magenta]
- A grid of numbers will be shown.
- Some numbers are REAL and contribute to the row/column sums, but some are fake.
- Your job is to MARK real numbers and CLEAR fake numbers.
- Row and column sums will be shown at the end of the row/column in [bold blue]blue[/bold blue]
- Type commands such as: [dark_orange3]mark 2 3[/dark_orange3] to mark row 2 column 3,
                         [dark_orange3]clear 5 2[/dark_orange3] to clear row 5 column 2.
- Once a number has been correctly marked, it will turn [bold green4]green[/bold green4].
- A number correctly cleared will be removed.
- To quit the game at any time, type [bold red3]quit[/bold red3].
Good luck!
""")


def play_turn(grid, sums):
    # console.print("Here is your grid:")
    display_grid(grid, sums[0], sums[1])
    while True:
        try:
            user_input = input("What is your command? ")
            if user_input.lower() == 'quit':
                sys.exit()
            cmd, row, col = user_input.split()
            row = int(row)-1
            col = int(col)-1
            if cmd.lower() == 'mark':
                console.clear()
                if grid[row][col]['real']:
                    grid[row][col]['found'] = True
                    console.print('Correct!', style='bold green4')
                else:
                    console.print('Incorrect!', style='bold red3')
                break

            elif cmd.lower() == 'clear':
                console.clear()
                if not grid[row][col]['real']:
                    grid[row][col]['val'] = " "
                    console.print('Correct!', style='bold green4')

                else:
                    console.print('Incorrect!', style='bold red3')
                break

            else:
                raise ValueError

        except (ValueError, IndexError):
            console.print("Invalid input, please try again.")


def check_finish(grid):
    for row in grid:
        for num in row:
            if num['real'] and not num['found']:
                return False
    return True


def get_size():
    while True:
        size = input(
            "What size grid would you like to play? Enter a value between 3 and 10: ")
        if size.isdigit() and int(size) >= 3 and int(size) <= 10:
            console.clear()
            console.print("Here is your grid:")
            return int(size)
        else:
            console.print("Invalid input, please try again")


def outro_message(grid, sums):
    display_grid(grid, sums[0], sums[1])
    console.print("You win!")
    choice = input("Would you like to play again? Yes or No: ")
    return True if choice.lower() == 'yes' else False


def main():
    console.clear()
    intro()
    play = True
    while play:

        size = get_size()
        # console.clear()
        grid = create_grid(size)
        grid = fill_grid(grid)
        sums = get_sums(grid)

        finish = False
        while not finish:

            play_turn(grid, sums)
            finish = check_finish(grid)
            # console.clear()
        play = outro_message(grid, sums)


main()

# rconsole.print("[bold green4]Hello World")
