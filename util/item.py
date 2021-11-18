
from dataclasses import dataclass
from datetime import date
from enum import Enum, auto, unique

@unique
class ItemType(Enum):

    lastUseDate = auto()
    bestBefore = auto()
    wontSpoil = auto()

@dataclass
class Item:

    name: str
    spoilDate: date
    itemType: ItemType

    def getItemType(self):
        return self.itemType

