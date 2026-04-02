from gameoflife import settings
from gameoflife.board.cell import Cell


def test_init_color_is_alive(cell: Cell) -> None:
    assert cell.color == settings.ALIVE


def test_init_generation(cell: Cell) -> None:
    assert cell.generation == 0


def test_first_generation_color(cell: Cell) -> None:
    first_time = True

    for gen in range(1, 5):
        if first_time:
            cell.generation = gen
            first_time = False

        assert cell.generation == gen
        cell.next_gen()
        assert cell.color == settings.GEN1


def test_second_generation_color(cell: Cell) -> None:
    first_time = True

    for gen in range(5, 10):
        if first_time:
            cell.generation = gen
            first_time = False

        assert cell.generation == gen
        cell.next_gen()
        assert cell.color == settings.GEN2


def test_third_generation_color(cell: Cell) -> None:
    first_time = True

    for gen in range(10, 50):
        if first_time:
            cell.generation = gen
            first_time = False

        assert cell.generation == gen
        cell.next_gen()
        assert cell.color == settings.GEN3


def test_fourth_generation_color(cell: Cell) -> None:
    first_time = True

    for gen in range(50, 100):
        if first_time:
            cell.generation = gen
            first_time = False

        assert cell.generation == gen
        cell.next_gen()
        assert cell.color == settings.GEN4


def test_fifth_generation_color(cell: Cell) -> None:
    first_time = True

    for gen in range(100, 150):
        if first_time:
            cell.generation = gen
            first_time = False

        assert cell.generation == gen
        cell.next_gen()
        assert cell.color == settings.GEN5
