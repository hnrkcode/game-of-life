from typing import Protocol


class PasteFunc(Protocol):
    def __call__(self, world_pos: tuple[int, int], button: tuple[bool, bool, bool], name: str | None = None) -> None: ...


class Node:
    """Node in the linked list to store a individual pattern in."""

    def __init__(self, data: tuple[str, PasteFunc]) -> None:
        self.data = data
        self.next: Node | None = None
        self.prev: Node | None = None


class PatternSelector:
    """Keeps stored pattern in a circular doubly linked list."""

    def __init__(self, data: tuple[str, PasteFunc] | None = None) -> None:
        self.counter = 0
        self.head: Node | None = None
        self.tail: Node | None = None
        if data:
            self.append(data)
        self.current: Node | None = self.head

    def append(self, data: tuple[str, PasteFunc]) -> int:
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

        if self.tail is None:
            raise ValueError
        self.tail.next = new_node
        new_node.next = self.head
        new_node.prev = self.tail
        self.tail = new_node
        if self.head is None:
            raise ValueError
        self.head.prev = self.tail

        return self.counter

    def next(self) -> None:
        """Go to the next node."""
        if self.current is None:
            raise ValueError
        self.current = self.current.next

    def previous(self) -> None:
        """Go to the previous node."""
        if self.current is None:
            raise ValueError
        self.current = self.current.prev

    def get_current(self) -> tuple[str, PasteFunc]:
        """Get the current node."""
        if not self.current:
            self.current = self.head

        if self.current is None:
            raise ValueError

        name = self.current.data[0]
        func = self.current.data[1]

        return name, func

    def before_current(self, num: int) -> str:
        """Return pattern name n times before active pattern."""
        if self.current is None:
            raise ValueError

        name: Node = self.current

        for _ in range(num):
            if name.next is None:
                raise ValueError
            name = name.next

        return name.data[0]

    def after_current(self, num: int) -> str:
        """Return pattern name n times after active pattern."""
        if self.current is None:
            raise ValueError

        name: Node = self.current

        for _ in range(num):
            if name.prev is None:
                raise ValueError
            name = name.prev

        return name.data[0]
