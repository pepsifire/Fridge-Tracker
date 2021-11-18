from dataclasses import dataclass, field
from typing import List
from .item import Item


@dataclass
class Fridge:

    name: str
    items: List[Item] = field(default_factory=list)

    def addItem(self, item):
        self.items.append(item)
    
    def removeItem(self, item):
        self.items.remove(item)

    def getContent(self):
        return self.items