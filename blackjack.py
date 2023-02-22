'''
 ___   ___
|A  | |## |
| 7 | |###|
|__A| |_##|

♠	Black Spade	&#9824;
♥	Black Heart	&#9829;
♣	Black Club	&#9827;
♦	Black Diamond	&#9830;
♤	White Spade	&#9828;
♡	White Heart	&#9825;
♧	White Club	&#9831;
♢	White Diamond	&#9826

'''

HEART = 9829
SPADE = 9824
CLUB = 9827
DIAMOND = 9830

card_values = (2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'K', 'Q', 'A')

BACKSIDE = [
    ' ___ ',
    '|## |',
    '|###|',
    '|_##|'
]

rules = '''
    Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value.
        (H)it to take another card.
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase your bet
        but must hit exactly one more time before standing.
        In case of a tie, the bet is returned to the player.
        The dealer stops hitting at 17.
'''


def main():
    print(rules)

    money = 5000
    
    while(True):
        if money <= 0:
            from sys import exit
            print("You're broke.")
            print("End of the game.")
            exit()
        print(f"Money: {money}")
        player_bet = get_bet(money)

        while(type(player_bet) == str):
            player_bet = get_bet(money)
        
        game_deck = get_deck()
        dealer_hand = get_hand(game_deck)
        player_hand = get_hand(game_deck)

        display_hand(get_hand_image(dealer_hand, dealer=True))
        display_hand(get_hand_image(player_hand), role='player', score=get_score(player_hand))
        
        money = get_action(dealer_hand=dealer_hand, player_hand=player_hand, bet=player_bet, deck=game_deck, bank=money)




def display_hand(hand_image, role='dealer', score=0):
    number_of_cards = len(hand_image)
    
    if number_of_cards == 2:
        if score == 0:
            print(f'\n{role.upper()}: ???')
        else:
            print(f'\n{role.upper()}: {score}')
        
        print('\n'.join([m+' '+n for m, n in zip((hand_image[0]), hand_image[1])]))
    else:
        new_hand = [[m+' '+n for m, n in zip(hand_image[0], hand_image[1])]]
        new_hand.extend(hand_image[2:]) 
        return display_hand(new_hand, role, score)

def get_hand_image(hand, dealer=False):
    if dealer:
        hand_image = [BACKSIDE]
        hand_image.extend(
            [[' ___ ', 
            f'|{str(card[0]).ljust(3, " ")}|', 
            f'| {chr(card[1])} |', 
            f'|{str(card[0]).rjust(3, "_")}|'] for card in hand[1:]])
        return hand_image

    return [[' ___ ', 
    f'|{str(card[0]).ljust(3, " ")}|', 
    f'| {chr(card[1])} |', 
    f'|{str(card[0]).rjust(3, "_")}|'] for card in hand]

def get_hand(deck):
    return [get_card(deck=deck), get_card(deck=deck)]

def get_card(deck, hit = False):
    from random import choice

    card = choice(deck)
    deck.remove(card)
    if hit:
        print(f"You drew a {card[0]} of {chr(card[1])}")
    return card

def get_deck():
    deck = []
    for card_suit in [HEART, SPADE, CLUB, DIAMOND]:
        for value in card_values:
            deck.append((value, card_suit))
    return deck

def get_score(cards):
    values = [card[0] for card in cards]
    score = 0
    number_of_aces = 0

    for rank in values:
        if type(rank) == int:
            score += rank
        else:
            if rank == 'A':
                number_of_aces += 1
            elif rank in ('K', 'Q', 'J'):
                score += 10
    
    if number_of_aces > 0:
        score += number_of_aces
        if score + 10 <= 21:
            score += 10

    return score

def get_bet(money):
    print(f"How much do you bet? (1-{money}) or QUIT")
    player_bet = input("> ").upper()
    if player_bet == 'QUIT':
        from sys import exit
        print("Bye. See you next time.")
        exit()

    if player_bet.isnumeric():
        if int(player_bet) not in range(1, money+1):
            print(f"Please enter a bet according to your money: a number from 1 to {money}")
            return 'repeat'
        print(f"Bet: {player_bet}")
        return int(player_bet)

    else:
        print(f"Ivalid bet input. Please input a number value in range from 1 to {money}.")
        return 'repeat'
    
def get_action(dealer_hand, player_hand, bet, deck, bank, first_bet=True):
    processing_string = "\x1B[3m--snip-\x1B[0m"

    dealer_score = get_score(dealer_hand)
    player_score = get_score(player_hand)

    if first_bet:
        print("\n (H)it (S)tand (D)ouble down")
    else:
        print("\n (H)it (S)tand")
    
    player_action = input("> ").lower()

    match player_action:
        case 's':
            print(processing_string)     
        
            display_hand(get_hand_image(dealer_hand), score=dealer_score)
            display_hand(get_hand_image(player_hand), role='player', score=player_score)

            if player_score >= dealer_score:
                print(f"\nYou won ${bet}.")
                print(processing_string, '\n')
                bank += bet
                return bank
            else:
                print(f"\nYou lost ${bet}")
                print(processing_string, '\n')
                bank -= bet
                return bank
        case 'h':
            if dealer_score <= 17:
                dealer_card = get_card(deck)
                dealer_hand.append(dealer_card)
                dealer_score = get_score(dealer_hand)

            if dealer_score > 21:
                display_hand(get_hand_image(dealer_hand), score=dealer_score)
                display_hand(get_hand_image(player_hand), role='player', score=player_score)

                print(f"\nYou won ${bet}.")
                print(processing_string, '\n')
                bank += bet
                return bank
            
            player_card = get_card(deck, hit=True)
            print(processing_string)
            player_hand.append(player_card)
            player_score = get_score(player_hand)
            
            if player_score > 21:
                display_hand(get_hand_image(dealer_hand), score=dealer_score)
                display_hand(get_hand_image(player_hand), role='player', score=player_score)

                print(f"\nYou lost ${bet}.")
                print(processing_string, '\n')
                bank -= bet
                return bank
            else:
                display_hand(get_hand_image(dealer_hand, dealer=True))
                display_hand(get_hand_image(player_hand), role='player', score=player_score)
                return get_action(dealer_hand, player_hand, bet, deck, bank, first_bet=False)
        case 'd':
            bet = bet*2
            print("\nYou selected double down. Here's your hit.")
            if dealer_score <= 17:
                dealer_card = get_card(deck)
                dealer_hand.append(dealer_card)
                dealer_score = get_score(dealer_hand)

            if dealer_score > 21:
                display_hand(get_hand_image(dealer_hand), score=dealer_score)
                display_hand(get_hand_image(player_hand), role='player', score=player_score)

                print(f"\nYou won ${bet}.")
                print(processing_string, '\n')
                bank += bet
                return bank
            
            player_card = get_card(deck, hit=True)
            print(processing_string)
            player_hand.append(player_card)
            player_score = get_score(player_hand)  
        
            display_hand(get_hand_image(dealer_hand), score=dealer_score)
            display_hand(get_hand_image(player_hand), role='player', score=player_score)

            if player_score > 21 or player_score < dealer_score:
                print(f"\nYou lost ${bet}")
                print(processing_string, '\n')
                bank -= bet
            else:
                print(f"\nYou won ${bet}.")
                print(processing_string, '\n')
                bank += bet
            return bank
    
    

if __name__ == '__main__':
    main()