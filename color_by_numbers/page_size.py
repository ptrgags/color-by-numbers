class DimensionsCalculator:
    """
    Subclasses of this class can calculate things like
    the print area (minus margins) and how many squares of
    a given size fit in the print area.
    """
    def __init__(self, page_dims, margin):
        self.page_size = page_dims
        self.margin = margin

    @property
    def print_area_dims(self):
        """
        Calculate width and height of the print area in points after
        subtracting the margin from each side.

        This returns (width, height) of the page in points.
        """
        raise NotImplementedError

    def grid_size(self, square_size):
        """
        Given the size of a square, calculate how many squares
        fit on the printable area.

        This returns (rows, cols) as integers
        """
        w, h = self.print_area_dims
        cols = int(w // square_size)
        rows = int(h // square_size)
        return (rows, cols)

    def block_size(self, image_dims, square_size):
        """
        Given the grid_dims (calculated from self.grid_size()), calculate
        how many pixels per block in the grid.

        This returns an integer size in pixels/grid square
        """
        raise NotImplementedError

    @classmethod
    def get_size_calculator(cls, image_dims, page_dims, margin):
        w, h = image_dims
        if w >= h:
            return PortraitCalculator(page_dims, margin)
        else:
            return LandscapeCalculator(page_dims, margin)

class PortraitCalculator(DimensionsCalculator):
    @property
    def print_area_dims(self):
        w, h = self.page_size
        return (w - 2 * self.margin, h - 2 * self.margin)

    def block_size(self, image_dims, square_size):
        _, img_cols = image_dims
        _, grid_cols = self.grid_size(square_size)
        return int(img_cols // grid_cols)

class LandscapeCalculator(DimensionsCalculator):
    @property
    def print_area_dims(self):
        w, h = self.page_size
        return (h - 2 * self.margin, w - 2 * self.margin)

    def block_size(self, image_dims, square_size):
        img_rows, _ = image_dims
        grid_rows, _ = self.grid_size(square_size)
        return int(img_rows // grid_rows)
