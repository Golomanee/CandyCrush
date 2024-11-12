import random

# Definirea constante pentru valorile bomboanelor
EMPTY = 0
RED = 1
YELLOW = 2
GREEN = 3
BLUE = 4


# Generarea aleatorie a matricei de joc
def generate_board():
    return [[random.choice([RED, YELLOW, GREEN, BLUE]) for _ in range(11)] for _ in range(11)]


# Funcție pentru afișarea matricei într-un mod lizibil
def print_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print("\n")


# Identificarea formațiunilor și calcularea punctajului
def find_matches(board):
    matches = []
    score = 0

    # Verificare linii orizontale și verticale
    for i in range(11):
        for j in range(11):
            # Linie orizontală de 5
            if j <= 6 and board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][
                j + 4] != EMPTY:
                matches.append([(i, j), (i, j + 1), (i, j + 2), (i, j + 3), (i, j + 4)])
                score += 50
            # Linie orizontală de 4
            elif j <= 7 and board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] != EMPTY:
                matches.append([(i, j), (i, j + 1), (i, j + 2), (i, j + 3)])
                score += 10
            # Linie orizontală de 3
            elif j <= 8 and board[i][j] == board[i][j + 1] == board[i][j + 2] != EMPTY:
                matches.append([(i, j), (i, j + 1), (i, j + 2)])
                score += 5

            # Linie verticală de 5
            if i <= 6 and board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == board[i + 4][
                j] != EMPTY:
                matches.append([(i, j), (i + 1, j), (i + 2, j), (i + 3, j), (i + 4, j)])
                score += 50
            # Linie verticală de 4
            elif i <= 7 and board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] != EMPTY:
                matches.append([(i, j), (i + 1, j), (i + 2, j), (i + 3, j)])
                score += 10
            # Linie verticală de 3
            elif i <= 8 and board[i][j] == board[i + 1][j] == board[i + 2][j] != EMPTY:
                matches.append([(i, j), (i + 1, j), (i + 2, j)])
                score += 5

            # Formațiune L de 3x3
            if i <= 8 and j <= 8:
                if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i][j + 1] == board[i][j + 2] != EMPTY:
                    matches.append([(i, j), (i + 1, j), (i + 2, j), (i, j + 1), (i, j + 2)])
                    score += 20
                elif board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i + 1][j] == board[i + 2][j] != EMPTY:
                    matches.append([(i, j), (i, j + 1), (i, j + 2), (i + 1, j), (i + 2, j)])
                    score += 20

            # Formațiune T de 3x3
            if i <= 8 and j <= 8 and board[i][j + 1] == board[i + 1][j + 1] == board[i + 2][j + 1] != EMPTY:
                if board[i + 1][j] == board[i + 1][j + 1] == board[i + 1][j + 2]:
                    matches.append([(i, j + 1), (i + 1, j), (i + 1, j + 1), (i + 1, j + 2), (i + 2, j + 1)])
                    score += 30

    return matches, score


# Eliminarea bomboanelor, aplicarea gravitației și completarea coloanelor cu bomboane noi
def remove_and_apply_gravity(board, matches):
    for match in matches:
        for (i, j) in match:
            board[i][j] = EMPTY

    # Aplicarea gravitației și completarea cu bomboane noi
    for j in range(11):
        empty_spots = 0
        for i in range(10, -1, -1):
            if board[i][j] == EMPTY:
                empty_spots += 1
            elif empty_spots > 0:
                board[i + empty_spots][j] = board[i][j]
                board[i][j] = EMPTY

        # Adăugare bomboane noi în partea de sus pentru a umple spațiile goale
        for i in range(empty_spots):
            board[i][j] = random.choice([RED, YELLOW, GREEN, BLUE])


# Funcție pentru a găsi cea mai bună mișcare disponibilă
def find_best_move(board):
    best_score = 0
    best_move = None

    for i in range(11):
        for j in range(10):
            # Schimbare orizontală
            board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]
            matches, score = find_matches(board)
            if score > best_score:
                best_score = score
                best_move = ((i, j), (i, j + 1))
            board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]

            # Schimbare verticală
            if i < 10:
                board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]
                matches, score = find_matches(board)
                if score > best_score:
                    best_score = score
                    best_move = ((i, j), (i + 1, j))
                board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]

    return best_move, best_score


# Funcția principală pentru rularea unei runde până la atingerea unui scor de 10.000
def play_round():
    board = generate_board()
    total_score = 0
    max_attempts = 1000  # Limită de încercări pentru a evita buclele infinite
    moves = 0

    while total_score < 10000 and max_attempts > 0:
        print("Starea curentă a tablei de joc:")
        print_board(board)

        # Găsirea formațiunilor și calcularea punctajului
        matches, score = find_matches(board)
        if matches:
            remove_and_apply_gravity(board, matches)
            total_score += score
            print(f"Formațiuni găsite și eliminate. Scor curent: {total_score}")
        else:
            # Caută cea mai bună mutare disponibilă
            best_move, best_score = find_best_move(board)
            if best_move and best_score > 0:
                (x1, y1), (x2, y2) = best_move
                board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]
                print(f"Mutare efectuată între ({x1}, {y1}) și ({x2}, {y2}) pentru o formațiune optimă.")
            else:
                print("Nu mai există mutări posibile care să formeze combinații noi.")
                break  # Ieșire din joc dacă nu există mutări utile
        moves += 1
        max_attempts -= 1

    print(f"Scorul total pentru această rundă: {total_score}")
    return total_score, moves


# Simularea a 100 de jocuri și calculul mediei scorului
def simulate_games(num_games=1):
    scores = []
    move_counts = []

    for _ in range(num_games):
        score, moves = play_round()
        scores.append(score)
        move_counts.append(moves)

    average_score = sum(scores) / num_games
    average_moves = sum(move_counts) / num_games

    print(f"Scorurile pentru cele {num_games} jocuri: {scores}")
    print(f"Media scorurilor: {average_score}")
    print(f"Media numărului de mutări: {average_moves}")


# Rularea simulării
simulate_games()
