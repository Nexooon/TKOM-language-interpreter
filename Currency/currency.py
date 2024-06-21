from typing import Union, Dict
from dataclasses import dataclass
from Interpreter.reference import Reference


@dataclass
class Curtype:
    value: str

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        if isinstance(other, Curtype):
            return self.value == other.value
        return False


@dataclass
class Currency:
    value: Union[int, float]
    type: Curtype

    def __post_init__(self):
        if isinstance(self.value, int):
            self.value = float(self.value)

    def __str__(self):
        return f'{self.value:.2f} {self.type}'

    def __repr__(self):
        return f'{self.value:.2f} {self.type}'

    def set_value(self, new_value):
        if type(new_value) not in [int, float]:
            raise TypeError("cur.set_value() accepts only int or float.")
        self.value = float(new_value)


@dataclass
class Entry:
    name: str
    value: Currency


@dataclass
class Dictionary:
    storage: 'Dict[str, Currency]'

    def __iter__(self):
        for item in self.storage.items():
            yield Reference(Entry(name=item[0], value=item[1]))

    def __str__(self):
        return f"{self.storage}"

    def add(self, name, value):
        if type(name) is not str or type(value) is not Currency:
            raise TypeError("Dictionary accepts only str and cur")
        if self.storage.get(name):
            raise ValueError("This name already exists.")
        self.storage[name] = value

    def get(self, arg):
        if type(arg) is str:
            ret = self.storage.get(arg)
            if not ret:
                raise ValueError(f"get(\"{arg}\") - No such name in dictionary.")
            return self.storage.get(arg)
        if type(arg) is Curtype:
            new_dict = {}
            for key in self.storage:
                val = self.storage[key]
                if val.type == arg:
                    new_dict[key] = val
            return Dictionary(new_dict)
        raise TypeError("Expected str or curtype")
