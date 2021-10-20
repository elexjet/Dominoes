import random

def dominos_set():
    global full_domino_set
    full_domino_set = []

    for i in range(7):
        for j in range(7):
            if i <= j:
                full_domino_set.append([i,j])
    return full_domino_set

def player_hand(full_domino_set):
    hand = []

    random.shuffle(full_domino_set)

    for i in range(7):
        global stock_pieces
        piece = random.choice(full_domino_set)     # Select a random domino in the full_domino_set
        hand.append(piece)                         # Add the selected domino in the player's hand
        full_domino_set.remove(piece)
        stock_pieces = full_domino_set
    return hand

def next_player_move():
    global snake
    global status
    snake = []
    status = ""

    biggest_computer_hand = max(computer_hand)
    biggest_player_hand = max(player_hand)

    if biggest_computer_hand > biggest_player_hand:
        snake = [biggest_computer_hand]
        status = "player"
        computer_hand.remove(biggest_computer_hand)
    else:
        snake = [biggest_player_hand]
        status = "computer"
        player_hand.remove(biggest_player_hand)

def player_pieces():
    print(70 * "=")
    print(f'Stock size: {len(stock_pieces)}')
    print(f'Computer pieces: {len(computer_hand)}')
    print()
    print_snake()    # Call function print_snake and prints Domino snake in correct format
    print()
    print("Your pieces:")
    for i in range(len(player_hand)):
        print(f'{i+1}:{player_hand[i]}')
    print()
    if (status == "player" and len(player_hand) > 0 and len(computer_hand) != 0 and len(stock_pieces) !=0):
        print("Status: It's your turn to make a move. Enter your command.")
        actions()
    elif (status == "computer" and len(computer_hand) > 0 and len(player_hand) != 0 and len(stock_pieces) !=0):
        print("Status: Computer is about to make a move. Press Enter to continue...")
        actions()
    elif len(player_hand) == 0:
        print("Status: The game is over. You won!")
        exit()
    elif len(computer_hand) == 0:
        print("Status: The game is over. The computer won!")
        exit()
    elif len(stock_pieces) == 0:
        print("Status: The game is over. It's a draw!")
        exit()

def actions():
    global action
    global valid_action
    action = input()
    try:
        if status == "computer" and action == "":
            play_computer()
        elif status == "computer" and action != "":
            raise ValueError
        else:
            valid_action = int(action)
            if valid_action < -len(player_hand) or valid_action > len(player_hand):
                raise ValueError
            else:
                play_player()

    except ValueError:
        print("Invalid input. Please try again.")
        actions()

def play_player():
    global status
    global play
    index = valid_action
    if status == "player" and len(player_hand) == 0:
        player_pieces()
    elif status == "player" and len(player_hand) > 0:
        if index < 0:
            index = -index
            play = player_hand[index - 1]
            if snake[0][0] == play[1]:
                player_hand.remove(play)
                snake.insert(0, play)
            elif snake[0][0] == play[0]:
                player_hand.remove(play)
                play.reverse()
                snake.insert(0, play)
            else:
                print("Illegal move. Please try again.")
                actions()
        elif index > 0:
            play = player_hand[index - 1]
            if snake[-1][-1] == play[0]:
                player_hand.remove(play)
                snake.append(play)
            elif snake[-1][-1] == play[1]:
                player_hand.remove(play)
                play.reverse()
                snake.append(play)
            else:
                print("Illegal move. Please try again.")
                actions()
        elif index == 0:
            random.shuffle(stock_pieces)
            if len(stock_pieces) != 0:
                play = stock_pieces.pop()
                player_hand.append(play)
    status = "computer"
    player_pieces()

def play_computer():
    global status
    global play
    if status == "computer" and action == "":
        total_pieces = computer_hand + snake

        # https://www.geeksforgeeks.org/python-convert-a-nested-list-into-a-flat-list/
        # Convert a nested list into a flat list
        all_numbers = []
        def reemovNestings(input_list):
            for i in input_list:
                if type(i) == list:
                    reemovNestings(i)
                else:
                    all_numbers.append(i)

        reemovNestings(total_pieces)

        ########################################################################
        # Print in 'Count' format
        dictionary_count = {}
        for freq in range(7):
            if freq in all_numbers:
                dictionary_count[freq] = all_numbers.count(freq)

        ########################################################################
        # Generate Computer Scores
        dictionary_scores = {}
        for index, sublist in enumerate(computer_hand):
            sub_sum = 0
            for element in sublist:
                sub_sum += dictionary_count[element]
            dictionary_scores[index] = sub_sum

        ########################################################################
        # Sort Computer Hand Scores in Descending Order
        # https://stackabuse.com/how-to-sort-dictionary-by-value-in-python
        sorted_dict = {}
        sorted_keys = reversed(sorted(dictionary_scores, key=dictionary_scores.get))

        for w in sorted_keys:
            sorted_dict[w] = dictionary_scores[w]

        ########################################################################
        # AI Computer
        for key, value in sorted_dict.items():

            # Try domino [2,0] on LH of snake [0,4] in correct order, ie. [2,0][0,4]
            domino = computer_hand[key]
            if snake[0][0] == computer_hand[key][-1]:
                computer_hand.remove(domino)
                snake.insert(0, domino)
                break
            # Try domino [0,2] on LH of snake [0,4] in reverse order, ie. [0,2][0,4]
            elif snake[0][0] == computer_hand[key][0]:
                computer_hand.remove(domino)
                domino.reverse()
                snake.append(domino)
                break
            # Try domino [4,1] on LH of snake [0,4] in correct order, ie. [0,4][4,1]
            elif snake[-1][-1] == computer_hand[key][-1]:
                computer_hand.remove(domino)
                domino.reverse()
                snake.append(domino)
                break
            # Try domino [1,4] on LH of snake [0,4] in reverse order, ie. [0,4][1,4]
            elif snake[-1][-1] == computer_hand[key][0]:
                computer_hand.remove(domino)
                snake.append(domino)
                break
        else:
            random.shuffle(stock_pieces)
            if len(stock_pieces) != 0:
                play = stock_pieces.pop()
                computer_hand.append(play)
            elif len(computer_hand) == 0:
                status = "player"
                player_pieces() # call function to print game status

    status = "player"
    player_pieces()

def print_snake():
    if len(snake) < 6:
        print(unpack(snake))
    elif len(snake) >= 6:
        first_3_elements = [snake[i-1] for i in range(1, 4)]
        last_3_elements = [snake[-i] for i in reversed(range(1, 4))]
        print(f'{unpack(first_3_elements)}...{unpack(last_3_elements)}')

def unpack(s):
    return "".join(map(str, s))

#------------------------------------------------------------------------------------------
###### Excution of game
# Function calls
# Generate full domino set of 28 pairs of dominos
all_stock_pieces = dominos_set()
# Shuffle all stock pieces
random.shuffle((all_stock_pieces))
# Generate computer hand of 7 dominos
computer_hand = player_hand(all_stock_pieces)
# Generate computer hand of 7 dominos
player_hand = player_hand(all_stock_pieces)
# Determine which player has the largest domino (double or non double) and prints Snake and Status of the player who is to make the next move
next_player_move()
# Play game
player_pieces()

print(f'Domino snake: {snake}')

