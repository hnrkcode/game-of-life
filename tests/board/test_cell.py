from gameoflife import settings
from gameoflife.board.cell import Cell


def test_init_color_is_alive(cell: Cell) -> None:
    assert cell.color == settings.ALIVE


def test_cell_size(cell: Cell) -> None:
    size = (settings.CELL_SIZE, settings.CELL_SIZE)
    assert cell.rect.size == size


def test_cell_position(cell: Cell) -> None:
    assert cell.rect.topleft == (260, 50)


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
        cell_color = tuple(cell.image.get_at((0, 0)))
        assert cell_color == (*settings.GEN1, 255)


def test_second_generation_color(cell: Cell) -> None:
    first_time = True

    for gen in range(5, 10):
        if first_time:
            cell.generation = gen
            first_time = False

        assert cell.generation == gen
        cell.next_gen()
        cell_color = tuple(cell.image.get_at((0, 0)))
        assert cell_color == (*settings.GEN2, 255)


def test_third_generation_color(cell: Cell) -> None:
    first_time = True

    for gen in range(10, 50):
        if first_time:
            cell.generation = gen
            first_time = False

        assert cell.generation == gen
        cell.next_gen()
        cell_color = tuple(cell.image.get_at((0, 0)))
        assert cell_color == (*settings.GEN3, 255)


def test_fourth_generation_color(cell: Cell) -> None:
    first_time = True

    for gen in range(50, 100):
        if first_time:
            cell.generation = gen
            first_time = False

        assert cell.generation == gen
        cell.next_gen()
        cell_color = tuple(cell.image.get_at((0, 0)))
        assert cell_color == (*settings.GEN4, 255)


def test_fifth_generation_color(cell: Cell) -> None:
    first_time = True

    for gen in range(100, 150):
        if first_time:
            cell.generation = gen
            first_time = False

        assert cell.generation == gen
        cell.next_gen()
        cell_color = tuple(cell.image.get_at((0, 0)))
        assert cell_color == (*settings.GEN5, 255)
