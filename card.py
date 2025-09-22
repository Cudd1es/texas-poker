class Card:
    """
    spade(s): 2s - 10s, Js, Qs, Ks, As
    heart(h): 2h - 10h, Jh, Qh, Kh, Ah
    club(c): 2c - 10c, Jc, Qc, Kc, Ac
    diamond(d): 2d - 10d, Jd, Qd, Kd, Ad
    """

    SUITS = ['s', 'h', 'c', 'd']
    VALUES = list(range(2, 15))
    def __init__(self, suit, value):
        """
        suit: 's', 'h', 'c', 'd'
        value: 2-14, 11 = J, 12 = Q, 13 = K, 14 = A
        """
        self.suit = suit
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __hash__(self):
        return hash((self.suit, self.value))

    def __repr__(self):
        face = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        v = face.get(self.value, str(self.value))
        return f"{v}{self.suit}"

    def to_colored_str(self):
        suit_color = {
            's': '\033[34m',  # Blue
            'h': '\033[31m',  # Red
            'c': '\033[34m',  # Blue
            'd': '\033[31m',  # Red
        }
        color = suit_color.get(self.suit, '\033[0m')
        s = self.__repr__()
        return f"{color}{s}\033[0m"