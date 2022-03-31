import numpy as np
import random


class Card:

    def __init__(self, symbol, suit):
        self.symbol = self.set_symbol(symbol)
        self.value = self.set_value(symbol)
        self.suit = self.set_suit(suit)

    def set_suit(self, suit):
        if suit == 'Diamond':
            return '\u2666'
        elif suit == 'Heart':
            return '\u2665'
        elif suit == 'Club':
            return '\u2663'
        else:
            return '\u2660'

    def set_value(self, symbol):
            if symbol > 10:
                if symbol == 14:
                    return 11
                else:
                    return 10
            else:
                return symbol

    def set_symbol(self, symbol):
            if symbol < 11:
                return symbol
            elif symbol == 11:
                return 'J'
            elif symbol == 12:
                return 'Q'
            elif symbol == 13:
                return 'K'
            else:
                return 'A'



def create_full_deck():
    l_suit = ('Diamond','Heart','Club','Spade')
    deck = []

    for i in range(2,15):
        for j in l_suit:
            deck.append(Card(i,j))

    np_deck = np.array(deck)
    random.shuffle(np_deck)
    return np_deck

class Hand:

    def __init__(self, deck):
        self.hand = self.create_start_hand(deck)

    def create_start_hand(self, deck):
        np_deck = np.array(random.choices(deck, k = 2) )
        return np_deck

    def return_deck_after_taking_card(self,deck):
        deck = deck[np.isin(deck,self.hand) == False]
        return deck

    def print_player_cards(self):
        for i in self.hand:
            print(str(i.symbol) + i.suit,end = " ")

    def add_card(self, deck):
        self.hand = np.append(self.hand, random.choice(deck))

    def calculate_hand(self):
        ### Calculating 2 results because Ace can be 1 or 11
        result = 0
        result2 = 0
        for i in self.hand:
            if(i.symbol == 'A'):
                result += i.value
                result2 += i.value - 10
            else:
                result += i.value
                result2 += i.value
        if result <= 21:
            return result
        else:
            return result2


def print_hands(player_hand, dealer_hand):
    print('Your cards are:')
    player_hand.print_player_cards()
    print('\nThe dealer is dealt:\n' + str(dealer_hand.hand[0].symbol) + dealer_hand.hand[0].suit + ', Unknown')



def Choice(player_hand, deck):
    # function for player choice
    decision = 0
    while (decision != 'stay') & (decision != 'hit'):
        decision = input("Would you like to stay or hit:\n")
    if decision == 'stay':
        return 'stay'
    else:
        player_hand.add_card(deck)


def betting(p_money):
    print('You have', str(p_money) + '$')
    while True:
        try:
            bet = int(input('Place your bet: '))
            if bet > p_money:
                print("You don't have enough money")
                betting(p_money)
            if bet < 1:
                print('The minimum bet is 1$')
                betting(p_money)
            else:
                return bet
        except ValueError:
            print("Oops! That's incorrect value! Try again.")

def Round(deck, p_money):

    bet = betting(p_money)
    player_cards = Hand(deck)
    deck = player_cards.return_deck_after_taking_card(deck)
    dealer_cards = Hand(deck)
    deck = dealer_cards.return_deck_after_taking_card(deck)
    # checking if player has BlackJack on start hand:
    if player_cards.calculate_hand() == 21:
        print_hands(player_cards, dealer_cards)
        dealer_cards.print_player_cards()
        if dealer_cards.calculate_hand() == 21:
            dealer_cards.print_player_cards()
            print('You tie. The bet has been returned.')
            return p_money
        else:
            print('\nYou win ' + str(bet) + '$')
            return (int(p_money + bet))


    while player_cards.calculate_hand() < 21:
        print_hands(player_cards,dealer_cards)
        x = Choice(player_cards, deck)
        if x == 'stay':
            pl_value = player_cards.calculate_hand()
            print('The dealer has:')
            dealer_cards.print_player_cards()
            while dealer_cards.calculate_hand() < 17:
                print('\nThe dealer hits.')
                dealer_cards.add_card(deck)
                dealer_cards.return_deck_after_taking_card(deck)
                print('Now the dealer has:')
                dealer_cards.print_player_cards()
            dl_value = dealer_cards.calculate_hand()
            if dl_value > 21:
                print('\nThe dealer busts, you win ' + str(bet) + '$')
                return (int(p_money + bet))
            print('\nThe dealer stays.')
            if dl_value < pl_value:
                print('You win '+ str(bet) + '$')
                return (int(p_money + bet))
            elif dl_value == pl_value:
                print('You tie. The bet has been returned.')
                return p_money
            else:
                print('You lose ' + str(bet) + '$')
                return (int(p_money - bet))

        deck = player_cards.return_deck_after_taking_card(deck)
    print_hands(player_cards,dealer_cards)

    if player_cards.calculate_hand() == 21:
        if dealer_cards.calculate_hand() == 21:
            print('\nYou tie. The bet has been returned.')
            return p_money
        else:
            print('\nYou win ' + str(bet) + '$')
            return (int(p_money + bet))
    else:
        print("Your hand value is over 21 and you lose " + str(bet) + "$")
        return (int(p_money - bet))


def start_game():
    print('Welcome to Black Jack! For the start you get 1000$. Try to multiply this cash as much as you can!')
    deck = create_full_deck()
    p_money = 1000
    while p_money > 0:
        p_money = Round(deck,p_money)
    print("You've ran out of money. Please restart the game to try again.")

start_game()


