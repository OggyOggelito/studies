class Card:
    def __init__(self, value, suit):
        valid_value = list(range(2, 15))
        valid_suit = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.value_to_name = { 
                        14: "Ace",
                        13: "King",
                        12: "Queen",
                        11: "Jack"
        }
        self.name_to_value = {
                            "Ace": 14,
                            "King": 13,
                            "Queen": 12,
                            "Jack": 11
        }
        if value not in valid_value and value not in self.value_to_name.values():
            self.value = None
        else:
            if value in self.name_to_value.keys():
                value = self.name_to_value[value]
                 
            self.value = value
        if suit not in valid_suit:
            self.suit = None
        else:
            self.suit = suit
        
    def print_card_info(self):
        if self.value in self.value_to_name.keys():
            self.value = self.value_to_name[self.value]
        print(f"{self.value} of {self.suit}")
      
if __name__ == "__main__":
    four_of_diamonds = Card(4, "Diamonds")
    jack_of_clubs = Card('Jack', "Clubs")
    eight_of_spades = Card(8, "Spades")
    ace_of_hearts = Card('Ace', "Hearts")
    four_of_diamonds.print_card_info()
    jack_of_clubs.print_card_info()
    eight_of_spades.print_card_info()
    ace_of_hearts.print_card_info()

        