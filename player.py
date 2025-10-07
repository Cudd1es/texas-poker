from math import floor


class Player:
    def __init__(self, name:str, position):
        self.name = name
        self.position = position
        self.hand = []
        self.chips = 1000
        self.is_human = False
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


class AIPlayer(Player):
    def __init__(self, name: str, position):
        super().__init__(name, position)
        self.is_human = False

    def ask_bet(self, current_bet: int, winrate = -1):
        raised = False
        call_amount = current_bet - self.current_bet
        print(f"my winrate is {winrate}, chips left: {self.chips}, analyzing...")
        # all in strategy
        if winrate > 0.8:
            print("I will all in")
            all_in_chips = self.all_in()
            return 0, all_in_chips
        # fold strategy
        elif winrate < 0.15:
            print("I will fold")
            self.fold()
            return -1, 0
        # raise strategy
        elif winrate > 0.5:
            if (self.current_bet > 0 and call_amount == 0) or raised:
                print("I will check")
                return 1, 0
            raise_amount = max(5, floor(self.chips * 0.1))
            if self.chips <= current_bet + raise_amount:
                print("I will all in")
                all_in_chips = self.all_in()
                return 0, all_in_chips
            else:
                bet = call_amount + raise_amount
                self.bet(bet)
                raised = True
                return 1, bet
        # call/check strategy
        else:
            if call_amount == 0:
                print("I will check")
                return 1, 0
            if self.chips <= call_amount or self.chips <= 5:
                print("I will all in")
                all_in_chips = self.all_in()
                return 0, all_in_chips
            else:
                print("I will call")
                self.bet(call_amount)
                return 1, call_amount


class HumanPlayer(Player):
    def __init__(self, name:str, position):
        super().__init__(name, position)
        self.is_human = True
    def ask_bet(self, current_bet:int, winrate = -1):
        """
        returns:
        flag: status signal, -1: fold, 0: all in, 1: bet/check/call
        bet: value of chips amount for bet
        """
        call_amount = current_bet - self.current_bet
        if self.is_all_in:
            return 0, 0
        elif self.folded:
            return -1, 0
        else:
            while True:
                print(f"current chips: {self.chips}, current bet: {current_bet}, call needed: {call_amount}")
                action = input(f"{self.name}, enter the bet for this round ('c' to call, 'k' to check, 'a' to all in, 'f' to fold): ")
                if action == "f":
                    self.fold()
                    return -1, 0
                elif action == "a":
                    all_in_chips = self.all_in()
                    return 0, all_in_chips
                elif action == "c":
                    if call_amount > self.chips:
                        print("not enough chips")
                        continue
                    else:
                        self.bet(call_amount)
                        return 1, call_amount
                elif action == "k":
                    if call_amount == 0:
                        return 1, 0
                    else:
                        print("you need to call or fold")
                        continue
                elif action.isdigit():
                    bet_amount = int(action)
                    if bet_amount < call_amount:
                        print("bet must be higher than call amount")
                        continue
                    if bet_amount >self.chips:
                        print("not enough chips")
                        continue
                    self.bet(bet_amount)
                    return 1, bet_amount
                else:
                    print(f"[x] please enter a valid bet.")