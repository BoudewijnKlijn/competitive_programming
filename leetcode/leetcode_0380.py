import random


class RandomizedSet:

    def __init__(self):
        self.items_dict = dict()
        self.items_list = list()
        self.n = 0

    def insert(self, val: int) -> bool:
        if val in self.items_dict:
            return False
        else:
            self.items_list.append(val)
            self.items_dict[val] = self.n  # store list index
            self.n += 1
            return True

    def remove(self, val: int) -> bool:
        if val in self.items_dict:
            idx = self.items_dict[val]
            self.items_list[idx] = self.items_list[-1]
            self.items_dict[self.items_list[idx]] = idx
            self.items_list.pop()
            del self.items_dict[val]
            self.n -= 1
            return True
        else:
            return False

    def getRandom(self) -> int:
        return random.choice(self.items_list)


# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
