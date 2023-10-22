class Node:
    """Node in the linked list to store a individual pattern in."""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class PatternSelector:
    """Keeps stored pattern in a circular doubly linked list."""

    def __init__(self, data=None):
        self.counter = 0
        self.head = None
        self.tail = None
        if data:
            self.append(data)
        self.current = self.head

    def append(self, data):
        """Add data to the circular doubly linked list."""
        # Store the data in a new node.
        new_node = Node(data)

        # Keep track of how many nodes are stored in the list.
        self.counter += 1

        # If the linked list is empty.
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return self.counter

        self.tail.next = new_node
        new_node.next = self.head
        new_node.prev = self.tail
        self.tail = new_node
        self.head.prev = self.tail

        return self.counter

    def next(self):
        """Go to the next node."""
        self.current = self.current.next

    def previous(self):
        """Go to the previous node."""
        self.current = self.current.prev

    def get_current(self):
        """Get the current node."""
        if not self.current:
            self.current = self.head

        name = self.current.data[0]
        func = self.current.data[1]

        return name, func

    def before_current(self, num):
        """Return pattern name n times before active pattern."""
        name = self.current

        for _ in range(num):
            name = name.next

        if name is None:
            raise ValueError

        return name.data[0]

    def after_current(self, num):
        """Return pattern name n times after active pattern."""
        name = self.current

        for _ in range(num):
            name = name.prev

        if name is None:
            raise ValueError

        return name.data[0]
