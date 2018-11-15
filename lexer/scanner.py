
class Scanner:
    """Provides methods for scanning text"""

    def __init__(self, text):
        self.__text = text
        self.__pos = 0
        self.__start = 0

    def read(self):
        """Read next symbol, return None if input text ended"""
        ch = self.peek()
        if ch is not None:
            self.__pos += 1
        return ch

    def unread(self):
        """Move current position one symbol backward if it's possible"""
        self.__pos = max(self.__pos - 1, 0)

    def peek(self):
        """Get current symbol without moving current position"""
        if self.__pos >= len(self.__text):
            return None
        return self.__text[self.__pos]

    def prev(self):
        """Get previous symbol for lookback, return None if it's begging of the text input"""
        if self.__pos <= 0:
            return None
        return self.__text[self.__pos - 1]

    def read_until(self, valid):
        """Move current position until symbol is in valid symbols"""
        while True:
            ch = self.read()
            if ch is None:
                break

            if ch not in valid:
                self.unread()
                break

    def ignore(self):
        """Move token's start position to the current position, ignoring previous token symbols"""
        self.__start = self.__pos

    def extract(self):
        """Get current token and move start of next token to current position"""
        value = self.__text[self.__start:self.__pos]
        self.__start = self.__pos
        return value
