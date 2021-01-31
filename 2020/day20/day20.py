'''
Solutions for the Advent of Code - Day 20

Two findings make this problem signifigantly easier.

1: The first thing I checked when doing this puzzle was to see if there are
multiple image sections with the same edges. If there are not, then this
greatly reduces the problem space. It turns out that all different edges are
on no more than two blocks.

2: I also checked to see if there are any palendromic edges (that is, when
reversed, the edge stays the same). There are not, so when searching for a
match, if you find a single matching edge, the piece is guarenteed to be the
correct one.

Note: Really feeling the pain of not having unit tests here.
'''

import copy

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
        if edge == (1, 0): # Right
            return ''.join(x[-1] for x in self.image)
        elif edge == (-1, 0): # Left
            return ''.join(x[0] for x in self.image)
        elif edge == (0, 1): # Top
            return self.image[0]
        elif edge == (0, -1): # Bottom
            return self.image[-1]
        else:
            raise Exception("Invalid edge of: {} received".format(edge))

    def get_all_edges(self) -> set:
        return set([self.get_edge((-1, 0)), self.get_edge((1, 0)), self.get_edge((0, 1)), self.get_edge((0, -1))])

    def get_id(self) -> int:
        """ Returns the Tile's ID """
        return self.tile_id

    def get_image(self) -> list:
        return self.image

    def flip_image(self) -> None:
        """ Update the flip variable and generate a new image """
        self.flipped = not self.flipped
        self.image = self.update_image()

    def rotate_image(self) -> None:
        """ Update the rotation variable and generate a new image """
        self.orientation += 1
        if self.orientation == 4:
            self.orientation = 0
        self.image = self.update_image()

    def update_image(self) -> list:
        """
        Generates a new image based on the raw image and it's flips/
        rotations.
        """
        new_image = copy.deepcopy(self.raw_image)
        if self.flipped:
            new_image = [''.join(reversed(row)) for row in self.raw_image]
        
        for _ in range(self.orientation):
            new_image = self.perform_rotation(new_image)
        return new_image

    def perform_rotation(self, image):
        size = len(image)
        new_image = ['' for x in range(size)]
        for row in range(size):
            for col in reversed(range(size)):
                new_image[row] += image[col][row]
        return new_image

class PictureBoard(object):
    def __init__(self, all_tiles: dict):
        """
        Initialises the picture board.

        Args:
            all_tiles list(Tile): A list of all Tile objects
        """

        # Set of all unplaced tiles to iterate though
        self.unplaced_tiles = set(all_tiles.values())
        # Dict of tiles mapping tile ID to tile object
        self.all_tiles = {}
        for t in all_tiles:
            self.all_tiles[all_tiles[t].get_id()] = all_tiles[t]

        # Dict of tile ID's to their locations. Only in this dictionary if they are placed.
        self.tile_locations = {}

        # Dict of open spaces on the board for possible tile placements.
        # Key is coordinates, value is dict of edges that must match. 
        # (x, y): {(0, 1): 'xxxxxx', (0, -1): 'yyyyyy}} 
        self.open_tile_positions = {}
        self.open_tile_positions[(0, 0)] = {}

    def get_all_open_edges(self) -> set:
        open_edges = set()
        for edges_dict in list(self.open_tile_positions.values()):
            for edge in list(edges_dict.values()):
                open_edges.add(edge)
        return open_edges

    def place_all_tiles(self) -> None:
        """ Assuming no tiles are currently placed, place all tiles one by one. """
        # Place first tile at origin.
        initial_tile_id = next(iter(self.all_tiles))
        initial_tile = self.all_tiles[initial_tile_id]
        self.place_single_tile((0, 0), initial_tile_id)

        # Place more tiles until all placed.
        while len(self.unplaced_tiles) != 0:
            possible_location, tile_id = self.get_placable_tile()
            self.place_single_tile(possible_location, tile_id)


    def place_single_tile(self, location: tuple, tile_id: int) -> None:
        """
        Place a tile and handle the updating of internal tile state when
        placing a tile.
        """
        tile = self.all_tiles[tile_id]

        # Add tile to tile_locations
        self.tile_locations[tile_id] = location

        # Add new open_tile_positions
        x = location[0]
        y = location[1]
        possible_open_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for possible_open_position in possible_open_positions:
            if possible_open_position not in self.open_tile_positions:
                if possible_open_position not in self.tile_locations.values():
                    self.open_tile_positions[possible_open_position] = {}
        
        # Add edges to open tiles. Only add them if there isn't already a tile in the position.
        if (x + 1, y) not in self.tile_locations.values():
            self.open_tile_positions[(x + 1, y)][(-1, 0)] = tile.get_edge((1, 0))
        if (x - 1, y) not in self.tile_locations.values():
            self.open_tile_positions[(x - 1, y)][(1, 0)] = tile.get_edge((-1, 0))
        if (x, y + 1) not in self.tile_locations.values():
            self.open_tile_positions[(x, y + 1)][(0, -1)] = tile.get_edge((0, 1))
        if (x, y - 1) not in self.tile_locations.values():
            self.open_tile_positions[(x, y - 1)][(0, 1)] = tile.get_edge((0, -1))
        del self.open_tile_positions[(x, y)]

        # Remove tile from unplaced tiles
        self.unplaced_tiles.remove(tile)

    def get_placable_tile(self) -> tuple:
        """
        This function does two things:
        1: Iterate through all tiles until a tile is found that matches an edge
        in the open_tile_positions list.
        2: Rotate the given tile until it is in the correct location.
        Then it returns the position that tile belongs in, and the tile itself.
        """
        matching_position = None
        matching_tile_id = None
        matching_edge = None
        # Find matching tile, and position to place the matching tile
        for tile in self.unplaced_tiles:
            for position, dict_of_open_edges in self.open_tile_positions.items():
                open_edges = set(dict_of_open_edges.values())
                for edge in tile.get_all_edges():
                    if (edge in open_edges):
                        matching_tile_id = tile.get_id()
                        matching_position = position
                        matching_edge = edge
                        break
                    if (edge[::-1] in open_edges):
                        matching_tile_id = tile.get_id()
                        matching_position = position
                        matching_edge = edge[::-1]
                        break
                if matching_tile_id is not None:
                    break
            if matching_tile_id is not None:
                break

        # Rotate matching tile into correct position.
        edges_to_connect = self.open_tile_positions[matching_position]
        
        # Get edge position
        edge_position = (0, 0)
        for ep, edge in edges_to_connect.items():
            if edge == matching_edge or edge[::-1] == matching_edge:
                edge_position = ep

        # Get matching tile
        matching_tile = self.all_tiles[matching_tile_id]

        done = False
        for _ in range(8):
            matching_tile.rotate_image()
            if matching_tile.get_edge(edge_position) == matching_edge:
                done = True
                break

        if not done:
            matching_tile.flip_image()
            if matching_tile.get_edge(edge_position) == matching_edge:
                done = True

        if not done:
            for _ in range(8):
                matching_tile.rotate_image()
                if matching_tile.get_edge(edge_position) == matching_edge:
                    done = True
                    break

        # Tile now in correct orientation so we can return
        return (matching_position, matching_tile.tile_id)


    def get_corner_positions(self) -> list:
        """
        Returns a list of the four (x, y) tuples that correspond to the
        locations of the 4 corners of the image.
        """
        loc_x = [x[0] for x in self.tile_locations.values()]
        loc_y = [x[1] for x in self.tile_locations.values()]
        max_x = max(loc_x)
        min_x = min(loc_x)
        max_y = max(loc_y)
        min_y = min(loc_y)
        return [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]
    
    def part_a(self) -> int:
        """ Return the product of all the corner image ID's """
        product = 1
        for pos in self.get_corner_positions():
            for tid, loc in self.tile_locations.items():
                if pos == loc:
                    product *= tid
        return product

    def get_map(self):
        """
        Returns a list of strings constituting the map of all pieces in their
        final positions.
        """
        loc_x = [x[0] for x in self.tile_locations.values()]
        loc_y = [x[1] for x in self.tile_locations.values()]
        max_x = max(loc_x)
        min_x = min(loc_x)
        max_y = max(loc_y)
        min_y = min(loc_y)
        




def read_input(file_name: str) -> dict:
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
    picture_board = PictureBoard(tiles)
    picture_board.place_all_tiles()
    print("Part A: " + str(picture_board.part_a()))
    