from util.item import Item, ItemType
from util.fridge import Fridge
from datetime import date


def main():
    f = Fridge("My Fridge")
    egg = Item("egg", date(2021, 11, 19), ItemType.lastUseDate)
    f.addItem(egg)
    print(f.getContent())

if __name__ == '__main__':
    main()