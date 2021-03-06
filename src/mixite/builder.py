from mixite.coord import CubeCoordinate
from mixite.storage import DefaultHexagonDataStorage
from mixite.grid import HexagonGrid, HexagonGridImpl
from mixite.hex import GridData, HexagonImpl
from mixite.calculator import HexagonGridCalculator
from mixite.layout import GridLayoutStrategy, HexagonGridLayoutStrategy, RectangleGridLayoutStrategy, \
    TriangleGridLayoutStrategy, TrapezoidGridLayoutStrategy


class GridControl:
    """
    This class is a container for the various object required to handle a grid.
    It is produced by GridControlBuilder and maintains references to instances
    of the calculator and the grid itself.
    """

    def __init__(self, hex_grid: HexagonGrid, calculator: HexagonGridCalculator, grid_data: GridData):
        self.hex_grid = hex_grid
        self.calculator = calculator
        self.grid_data = grid_data


class GridControlBuilder:

    def build_rectangle(self, orientation: str, radius: float, width: int, height: int) -> GridControl:
        grid_data = self.build_grid_data(orientation, radius, width, height)
        strategy = RectangleGridLayoutStrategy()
        self.check_size(strategy, width, height)
        grid = HexagonGridImpl(grid_data, DefaultHexagonDataStorage())
        self.populate_storage(grid, grid_data, strategy.fetch_grid_coords(width, height, orientation))
        return GridControl(grid, HexagonGridCalculator(grid), grid_data)

    def build_hexagon(self, orientation: str, radius: float, width: int, height: int) -> GridControl:
        grid_data = self.build_grid_data(orientation, radius, width, height)
        strategy = HexagonGridLayoutStrategy()
        self.check_size(strategy, width, height)
        grid = HexagonGridImpl(grid_data, DefaultHexagonDataStorage())
        self.populate_storage(grid, grid_data, strategy.fetch_grid_coords(width, height, orientation))
        return GridControl(grid, HexagonGridCalculator(grid), grid_data)

    def build_triangle(self, orientation: str, radius: float, width: int, height: int) -> GridControl:
        grid_data = self.build_grid_data(orientation, radius, width, height)
        strategy = TriangleGridLayoutStrategy()
        self.check_size(strategy, width, height)
        grid = HexagonGridImpl(grid_data, DefaultHexagonDataStorage())
        self.populate_storage(grid, grid_data, strategy.fetch_grid_coords(width, height, orientation))
        return GridControl(grid, HexagonGridCalculator(grid), grid_data)

    def build_trapezoid(self, orientation: str, radius: float, width: int, height: int) -> GridControl:
        grid_data = self.build_grid_data(orientation, radius, width, height)
        strategy = TrapezoidGridLayoutStrategy()
        self.check_size(strategy, width, height)
        grid = HexagonGridImpl(grid_data, DefaultHexagonDataStorage())
        self.populate_storage(grid, grid_data, strategy.fetch_grid_coords(width, height, orientation))
        return GridControl(grid, HexagonGridCalculator(grid), grid_data)

    @staticmethod
    def build_grid_data(orientation: str, radius: float, width: int, height: int) -> GridData:
        return GridData(orientation, radius, width, height)

    @staticmethod
    def check_size(strategy: GridLayoutStrategy, width: int, height: int):
        strategy.check_size(width, height)

    @staticmethod
    def populate_storage(grid: HexagonGridImpl, grid_data: GridData, coords: list[CubeCoordinate]):
        for coord in coords:
            hexagon = HexagonImpl(grid_data, coord)
            grid.storage.add_coord_with_data(coord, hexagon)
            grid.hexagons.append(hexagon)
