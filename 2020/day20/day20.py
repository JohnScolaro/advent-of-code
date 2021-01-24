'''
Solutions for the Advent of Code - Day 20
'''

class Tile(object):
    def __init__(self, tile_id: int, image: list):
        # The ID of the tile
        self.tile_id = tile_id
        # The image on the tile as it was created. No rotations or flips factored in.
        self.raw_image = image
        # The image with flips and orientations factored in.
        self.image = image
        # Orientation of image. Each increment = 90 clockwise turn.
        self.orientation = 0
        # Whether the image is flipped along the y axis or not.
        self.flipped = False

    def get_edge(self, edge: tuple) -> str:
        """
        Return edge as a string
        
        Args:
            edge (tuple):   (1, 0) = right
                            (-1, 0) = left
                            (0, 1) = top
                            (0, -1) = bottom

        Edge is always read from left to right, or from top to bottom.
        """
        pass

    def get_id(self) -> int:
        """ Returns the Tile's ID """
        return self.tile_id

    def get_image(self) -> list:
        return self.image

    def get_raw_image(self) -> list:
        return self.raw_image

class PictureBoard(object):
    def __init__(self, all_tiles: list):
        """
        Initialises the picture board.

        Args:
            all_tiles list(Tile): A list of all Tile objects
        """
        # Set of all unplaced tiles to iterate though
        self.unplaced_tiles = set(all_tiles)
        # Dict of tiles mapping tile ID to tile object
        self.all_tiles = {}
        for t in all_tiles:
            self.all_tiles[t.get_id()] = t

        # Dict of tile ID's to their locations. Only in this dictionary if they are placed.
        self.tile_locations = {}
        # Dict of tile locations to the border strings that matching tiles could have.
        # self.outside_edge[(1, 1)] = {(0, -1): "xxxxxxxx", (-1, 0): "yyyyyyyy"}
        # The empty space at (1, 1) is bordered by xxxxxxxx on the bottom edge and
        # yyyyyyyy on the left edge.
        self.outside_edges = {}

    def place_all_tiles(self) -> None:
        pass

    def place_single_tile(self) -> None:
        pass
    
    def part_a(self) -> int:
        """ Return the product of all the corner image ID's """
        return 0


def read_input(file_name: str):
    lines = []
    with open(file_name, 'r') as fb:
        for line in fb:
            lines.append(line.strip().replace('Tile ', '').replace(':', ''))

    tiles = {}
    for x in range(len(lines) // 12):
        tile_id = int(lines[x * 12])
        tiles[tile_id] = Tile(tile_id, lines[(x * 12) + 1: x * 12 + 11])

    return tiles
    

if __name__ == "__main__":
    tiles = read_input('input.txt')
    
    for t in tiles:
        print(tiles[t].get_raw_image())