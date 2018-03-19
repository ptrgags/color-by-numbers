class DimensionsCalculator:
    """
    Subclasses of this class can calculate things like
    the print area (minus margins) and how many squares of
    a given size fit in the print area.
    """
    def __init__(self, paper_dims, margin):
        # This is the size of the paper in portrait orientation.
        # self.postscript_dims is the page size for postscript which could
        # be either
        self.paper_dims = paper_dims
        self.margin = margin

    @property
    def postscript_dims(self):
        """
        Dimensions to use in the Postscript file in points.
        This could be either portrait or landscape.
        """
        raise NotImplementedError

    @property
    def print_area_dims(self):
        """
        Calculate width and height of the print area in points after
        subtracting the margin from each side.

        This returns (width, height) of the page in points.
        """
        w, h = self.postscript_dims
        return (w - 2 * self.margin, h - 2 * self.margin)

    def points_per_pixel(self, image):
        """
        Calculate the number of points per pixel
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
        rows, cols = image_dims
        if rows >= cols:
            return PortraitCalculator(page_dims, margin)
        else:
            return LandscapeCalculator(page_dims, margin)

class PortraitCalculator(DimensionsCalculator):
    @property
    def postscript_dims(self):
        # the paper is already right side up in portrait orientation!
        return self.paper_dims

    def points_per_pixel(self, image):
        _, cols = image.shape
        x_points, _ = self.print_area_dims
        print(f'{x_points} {cols} {x_points / cols}')
        return x_points / cols

    def block_size(self, image_dims, square_size):
        _, img_cols = image_dims
        _, grid_cols = self.grid_size(square_size)
        return int(img_cols // grid_cols)

class LandscapeCalculator(DimensionsCalculator):
    @property
    def postscript_dims(self):
        # for landscape we need to swap the paper dimensions
        w, h = self.paper_dims
        return h, w

    def points_per_pixel(self, image):
        rows, _ = image.shape
        _, y_points = self.print_area_dims
        print(f'{y_points} {rows} {y_points / rows}')
        return y_points / rows

    def block_size(self, image_dims, square_size):
        img_rows, _ = image_dims
        grid_rows, _ = self.grid_size(square_size)
        return int(img_rows // grid_rows)
