from selenium import webdriver
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--lang=vi')  
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.sudoku.net/vi/')
sleep(10) 

sudoku_data = driver.execute_script("""
    var b = [];

    var table = document.getElementById("sudoku");

    for (var i = 0; i < table.rows.length; i++) {
        var row = [];
        for (var j = 0; j < table.rows[i].cells.length; j++) {
            var cellValue = table.rows[i].cells[j].innerText.trim();
            row.push(cellValue === "" || isNaN(cellValue) ? 0 : parseInt(cellValue));
        }
        b.push(row);
    }

    return b;
""")

def is_valid_move(board, row, col, num):
    
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def find_empty_cell(board):
    
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col

    return None

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True  

    row, col = empty_cell

    for num in range(1, 10):
        if is_valid_move(board, row, col, num):

            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

sudoku_board = sudoku_data

if solve_sudoku(sudoku_board):
    print("Sudoku đã được giải:")
    for row in sudoku_board:
        print(row)
    
    driver.execute_script("""
        var a = document.getElementById("sudoku");
        var b = """ + str(sudoku_board) + """;

        for (let i = 0; i < 9; i++){
            for (let j = 0; j < 9; j++){
                a.rows[i].cells[j].innerText = b[i][j];
            }
        }
    """)
else:
    print("Không có giải pháp cho Sudoku này.")

sleep(60)

driver.quit()
