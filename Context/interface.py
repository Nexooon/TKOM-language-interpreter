from abc import ABCMeta, abstractmethod
from typing_extensions import Self
from typing import Optional, Union, Callable, Dict
from Currency.currency import Currency, Curtype, Dictionary


class ScopeTableInterface(metaclass=ABCMeta):
    parent_scope: Optional[Self]
    _table: 'Dict[str, Union[Callable, int, float, bool, str, Currency, Curtype, Dictionary]]'

    @abstractmethod
    def insert_symbol_function(self, name, value):
        ...

    @abstractmethod
    def insert_symbol_variable(self, name, value):
        ...

    @abstractmethod
    def get_value_function(self, name):
        ...

    @abstractmethod
    def get_value_variable(self, name):
        ...


class ContextInterface(metaclass=ABCMeta):
    _current_scope: ScopeTableInterface

    @abstractmethod
    def enter_scope(self):
        ...

    @abstractmethod
    def leave_scope(self):
        ...

    @abstractmethod
    def insert_symbol_function(self, name, value):
        ...

    @abstractmethod
    def insert_symbol_variable(self, name, value):
        ...

    @abstractmethod
    def get_value_function(self, name):
        ...

    @abstractmethod
    def get_value_variable(self, name):
        ...
