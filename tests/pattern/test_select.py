import pytest
from gameoflife.pattern.select import Node, PatternSelector


def test_node():
    node = Node(data=None)

    assert node.data == None
    assert node.next == None
    assert node.prev == None


def test_init_pattern_selector():
    def fn(name):
        return name

    selector = PatternSelector(("test", fn))

    assert selector.get_current() == ("test", fn)
    assert selector.counter == 1


def test_pattern_selector():
    selector = PatternSelector()

    assert selector.counter == 0
    assert selector.head == None
    assert selector.tail == None
    assert selector.current == selector.head
    assert not isinstance(selector.head, Node)

    def fn(name):
        return name

    # First entry.
    assert selector.append(("test_1", fn)) == 1

    assert isinstance(selector.head, Node)
    assert selector.get_current() == ("test_1", fn)

    with pytest.raises(ValueError):
        selector.before_current(1)

    with pytest.raises(ValueError):
        selector.after_current(1)

    selector.next()
    assert selector.get_current() == ("test_1", fn)

    selector.next()
    assert selector.get_current() == ("test_1", fn)

    selector.next()
    assert selector.get_current() == ("test_1", fn)

    # Second entry.
    assert selector.append(("test_2", fn)) == 2

    for n in range(1, 4):
        assert selector.append((f"test_{n + 2}", fn)) == n + 2

    assert selector.counter == 5

    selector.next()
    assert selector.get_current() == ("test_2", fn)

    selector.next()
    assert selector.get_current() == ("test_3", fn)

    selector.next()
    assert selector.get_current() == ("test_4", fn)

    selector.next()
    assert selector.get_current() == ("test_5", fn)

    selector.next()
    assert selector.get_current() == ("test_1", fn)

    selector.previous()
    assert selector.get_current() == ("test_5", fn)

    selector.previous()
    assert selector.get_current() == ("test_4", fn)

    assert selector.before_current(3) == "test_2"
    assert selector.after_current(3) == "test_1"
