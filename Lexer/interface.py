from abc import ABCMeta, abstractmethod


class Lexer(metaclass=ABCMeta):

    @abstractmethod
    def get_next_token(self):
        ...
