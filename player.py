class Player:
    def __init__(self, name:str, position, is_human=False):
        self.name = name
        self.position = position
        self.hand = []
        self.chips = 100
        self.is_human = is_human
        self.folded = False
        self.is_all_in = False
        self.current_bet = 0

    def bet(self, amount):
        if amount > self.chips:
            print("not enough chips")
            return False
        self.chips -= amount
        self.current_bet += amount
        return True

    def win_chips(self, amount):
        self.chips += amount

    def fold(self):
        self.folded = True

    def all_in(self):
        all_in_chips = self.chips
        self.bet(self.chips)
        self.is_all_in = True
        return all_in_chips

    def reset_for_new_round(self):
        self.folded = False
        self.is_all_in = False
        self.current_bet = 0
        self.hand = []

    def __repr__(self):
        return f"Player({self.name}, chips={self.chips}, hand={self.hand}, folded={self.folded})"

    def ask_bet(self, current_bet:int):
        """
        returns:
        flag: status signal, -1: fold, 0: all in, 1: bet
        bet: value of chips amount for bet
        """
        if self.is_all_in:
            return 0, current_bet
        elif self.folded:
            return -1, current_bet
        else:
            while True:
                print(f"current chips: {self.chips}, current bet: {current_bet}")
                bet = input(f"{self.name}, please enter the bet for this round ('c' to check 'a' to all in, 'f' to fold): ")
                if bet.isalpha():
                    if bet.lower() == 'a':
                        all_in_chips = self.all_in()
                        return 0, all_in_chips
                    elif bet.lower() == 'f':
                        self.fold()
                        return -1, 0
                    elif bet.lower() == 'c':
                        if current_bet == 0:
                            print("please enter a valid bet.")
                            continue
                        else:
                            if current_bet > self.chips:
                                print("not enough chips")
                                continue
                            else:
                                self.bet(current_bet)
                                return 1, current_bet
                    else:
                        print(f"[x] please enter a valid bet.")
                elif bet.isdigit():
                    bet = int(bet)
                    if bet < current_bet:
                        print("raise must be higher than current bet")
                        continue
                    elif bet > self.chips:
                        print("not enough chips")
                        continue
                    else:
                        self.bet(bet)
                        return 1, bet