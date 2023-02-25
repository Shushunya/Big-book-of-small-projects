rules = """
In these traditional Japanese dice game, two dice are rolled in a bamboo cup by the dealer sitting on the floor. 
The player must guess if the dice total to an even (cho) or odd (han) number.
"""

after_bet = """
The dealer swirls the cup and you hear the rattle of dice.
The dealer slams the cup on the floor, still covering the dice and asks for your bet.
"""

asking_for_bet = 'CHO (even) or HAN (odd)?'.center(50)

def roll():
    from random import randint
    dice1 = randint(1, 6)
    dice2 = randint(1, 6)
    return dice1, dice2

def get_bet(money, first_try=True):
    
    if first_try:
        print(f"You have {money} mon. How much do you bet? (or QUIT)")
    
    player_input = input("> ").upper()

    if player_input == 'QUIT':
        from sys import exit
        print("Bye. See you.")
        exit()

    if player_input.isnumeric():
        if int(player_input) not in range(1, money+1):
            print(f"Please enter a bet according to your money: a number from 1 to {money}")
            return get_bet(money, first_try=False)
        return int(player_input)
    else:
        print(f"Ivalid bet input. Please input a number value in range from 1 to {money}.")
        return get_bet(money, first_try=False)

def play_game(money):
    JAPANESE_NUMBERS = {
        1 : 'ICHI',
        2 : 'NI',
        3 : 'SAN',
        4 : 'SHI',
        5 : 'GO',
        6 : 'ROKU'}

    bets = {"CHO" : 0, "HAN" : 1}
    win = False

    bet = get_bet(money)
    dice1, dice2 = roll()
    dice_sum = (dice1 + dice2)%2
    print(after_bet)
    while(True):
        print(asking_for_bet)
        player_guess = input("> ").upper()
        if player_guess in ('CHO', 'HAN'):
            guess = bets[player_guess]
            break
    
    if guess == dice_sum:
        win = True

    print("The dealer lifts the cup to reveal:")
    print(f"{JAPANESE_NUMBERS[dice1]} - {JAPANESE_NUMBERS[dice2]}".center(50))
    print(f"{dice1} - {dice2}".center(50))
    
    if win == True:
        print(f"You won! You take {bet} mon.")
        dealer_fee = bet // 10
        money += bet
        print(f"The house collects a {dealer_fee} mon fee.")
        money -= dealer_fee
    else:
        print(f"You lost {bet} mon.")
        money -= bet
    return money
    

def main(purse=5000):
    print(rules)
    print()
    while(purse > 0):
        purse = play_game(purse)
    print("You are broke. End of the game.")
    from sys import exit
    exit()


if __name__ == '__main__':
    print("You can enter your amount of money. Default is 5000.")
    player_money = input("> ")
    if player_money.isdecimal():
        main(int(player_money))
    else:
        main()