class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class MyLinkedList:

    def __init__(self):
        self.head = None

    def __str__(self):
        vals = list()
        node = self.head
        while node:
            vals.append(node.val)
            node = node.next
        return str(vals)

    @staticmethod
    def show(func):
        def inner(self, *args, **kwargs):
            print("before", self)
            res = func(self, *args, **kwargs)
            print("after", self)
            return res

        return inner

    # @show
    def get(self, index: int) -> int:
        i = 0
        node = self.head
        try:
            while i < index:
                node = node.next
                i += 1
            return node.val
        except AttributeError:
            return -1

    # @show
    def addAtHead(self, val: int) -> None:
        tmp = self.head
        self.head = Node(val)
        self.head.next = tmp

    # @show
    def addAtTail(self, val: int) -> None:
        node = self.head
        if node is None:
            self.head = Node(val)
            return
        while node.next:
            node = node.next
        node.next = Node(val)

    # @show
    def addAtIndex(self, index: int, val: int) -> None:
        if index == 0:
            self.addAtHead(val)
            return

        i = 0
        node = self.head
        try:
            while i + 1 < index:
                node = node.next
                i += 1
            new_node = Node(val)
            new_node.next = node.next
            node.next = new_node
        except AttributeError:
            return

    # @show
    def deleteAtIndex(self, index: int) -> None:
        if index == 0:
            if self.head:
                self.head = self.head.next
            return

        i = 0
        node = self.head
        try:
            while i + 1 < index:
                node = node.next
                i += 1

            node.next = node.next.next
        except AttributeError:
            return


# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)
