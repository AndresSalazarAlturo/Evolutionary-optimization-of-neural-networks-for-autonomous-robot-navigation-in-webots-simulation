## Utilities
import matplotlib.pyplot as plt
import numpy as np

class Square:
    """
        Create the instance of one square of the board.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0.125
        self.height = 0.125
        self.been_there = False             ## Initialize been_there attribute to False

    def __str__(self):
        return f"Square at ({self.x}, {self.y})"

class Board:
    """
        Creates the board.
    """
    def __init__(self):
        self.width = 2
        self.height = 2
        self.square_size = 0.125

    def create_board(self):
        # """
        #     Creates the grid. Grid is a list of lists made of intances of Square class.
        # """
        # grid = []
        # for y in range(-2, int(self.height / self.square_size)):
        #     row = []
        #     for x in range(-2, int(self.width / self.square_size)):
        #         row.append(Square(x * self.square_size, y * self.square_size))
        #     grid.append(row)
        # return grid

        board = []
        for y in range(self.height * 8, -((self.height * 8) + 1), -1):
            for x in range(-self.width * 8, (self.width * 8) + 1):
                board.append(Square(x * self.square_size, y * self.square_size))
        return board

    def display_grid(self):

        for row in self.grid:
            for square in row:
                print(square, end=" ")
            print()

    def display_board(self, data):
        """
            Display the board with grid and the robot trayectory.
            :param data: The robot trayectory. List of lists
        """

        # Extract x and y coordinates from the list of lists
        x = [point[0] for point in data]
        y = [point[1] for point in data]

        # Create plot
        plt.figure(figsize=(10, 10))  # Set figure size
        plt.plot(x, y, color = 'red')  # Plot a line connecting the data points

        # Add horizontal and vertical lines at x=0 and y=0 to represent the axes
        plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
        plt.axvline(0, color='black', linestyle='--', linewidth=0.5)

        # Set labels and title
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Robot trayectory')

        # Set custom ticks for x-axis and y-axis to change grid size
        plt.xticks(np.arange(-2, 2, 0.125))  # Set x-axis ticks at intervals of 0.125
        plt.yticks(np.arange(-2, 2, 0.125))  # Set y-axis ticks at intervals of 0.125

        # Set axis limits to ensure all quadrants are visible
        plt.xlim(-self.width/2, self.width/2)
        plt.ylim(-self.height/2, self.height/2)

        # Show grid
        plt.grid(True)

        ## Save plot
        plt.savefig("../../../My_Robot_Trayectory_Plots/First_Test.png")

        # Show plot
        plt.show()


    def is_within_square(self, coordinates, grid):
        """
            Change the attribute been_there to True if the coordinate is inside the coordinates of that square.
            Checks if the coordinate "x" is inside the horizontal boundaries of the square. It ensures that "x"
            is greater than or equal to the leftmost x-coordinate of the square(square.x) and less than the rightmost
            x-coordinate of the square, which is the sum of the square's x-coordinate and its width.
            It uses the same conditi`on for "y" and he vertical boundaries.
            :param coordinates: The robot trayectory. List of lists
            :param grid: Board grid. List of lists
            :return: False
        """
        # x, y = coordinates[0], coordinates[1]
        # for row in grid:
        #     for square in row:
        #         if square.x <= x < (square.x + square.width) and square.y <= y < (square.y + square.height):
        #             square.been_there = True  # Set been_there to True if coordinate is within this square
        #             return True
        # return False

        x, y = coordinates[0], coordinates[1]
        for square in grid:
            if square.x <= x < (square.x + square.width) and square.y <= y < (square.y + square.height):
                square.been_there = True  # Set been_there to True if coordinate is within this square
                return True
        return False

    def count_squares_with_been_there(self, grid):
        """
            Count the number of squares in grid that change the attribute been_there to True.
            :param grid: Board grid. List of lists
            :return count: Number of squares where the robot have been.
        """
        # count = 0
        # for row in grid:
        #     for square in row:
        #         if square.been_there:
        #             count += 1
        # return count

        count = 0
        for square in grid:
            if square.been_there:
                count += 1
        return count

    def reset_been_there_to_False(self, grid):
        """
            Reset all the squares that changed the attribute been_there to True back to False.
            :param grid: Board grid. List of lists
            :return grid: All the square intances attribute been_there are back to False.
        """

        # for row in grid:
        #     for square in row:
        #         if square.been_there:
        #             square.been_there = False

        # return grid

        for square in grid:
            if square.been_there:
                square.been_there = False

        return grid

# ## Utilities
# import matplotlib.pyplot as plt
# import numpy as np

# class Square:
#     """
#         Create the instance of one square of the board.
#     """
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.width = 0.125
#         self.height = 0.125
#         self.been_there = False             ## Initialize been_there attribute to False

# class Board:
#     """
#         Creates the board.
#     """
#     def __init__(self):
#         self.width = 2
#         self.height = 2
#         self.square_size = 0.125

#     def create_board(self):
#         """
#             Creates the grid. Grid is a list of lists made of intances of Square class.
#         """
#         grid = []
#         for y in range(-2, int(self.height / self.square_size)):
#             row = []
#             for x in range(-2, int(self.width / self.square_size)):
#                 row.append(Square(x * self.square_size, y * self.square_size))
#             grid.append(row)
#         return grid

#     def display_board(self, data):
#         """
#             Display the board with grid and the robot trayectory.
#             :param data: The robot trayectory. List of lists
#         """

#         # Extract x and y coordinates from the list of lists
#         x = [point[0] for point in data]
#         y = [point[1] for point in data]

#         # Create plot
#         plt.figure(figsize=(10, 10))  # Set figure size
#         plt.plot(x, y, color = 'red')  # Plot a line connecting the data points

#         # Add horizontal and vertical lines at x=0 and y=0 to represent the axes
#         plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
#         plt.axvline(0, color='black', linestyle='--', linewidth=0.5)

#         # Set labels and title
#         plt.xlabel('X-axis')
#         plt.ylabel('Y-axis')
#         plt.title('Robot trayectory')

#         # Set custom ticks for x-axis and y-axis to change grid size
#         plt.xticks(np.arange(-2, 2, 0.125))  # Set x-axis ticks at intervals of 0.125
#         plt.yticks(np.arange(-2, 2, 0.125))  # Set y-axis ticks at intervals of 0.125

#         # Set axis limits to ensure all quadrants are visible
#         plt.xlim(-self.width/2, self.width/2)
#         plt.ylim(-self.height/2, self.height/2)

#         # Show grid
#         plt.grid(True)

#         ## Save plot
#         plt.savefig("../../../My_Robot_Trayectory_Plots/First_Test.png")

#         # Show plot
#         plt.show()


#     def is_within_square(self, coordinates, grid):
#         """
#             Change the attribute been_there to True if the coordinate is inside the coordinates of that square.
#             Checks if the coordinate "x" is inside the horizontal boundaries of the square. It ensures that "x"
#             is greater than or equal to the leftmost x-coordinate of the square(square.x) and less than the rightmost
#             x-coordinate of the square, which is the sum of the square's x-coordinate and its width.
#             It uses the same conditi`on for "y" and he vertical boundaries.
#             :param coordinates: The robot trayectory. List of lists
#             :param grid: Board grid. List of lists
#             :return: False
#         """
#         x, y = coordinates[0], coordinates[1]
#         for row in grid:
#             for square in row:
#                 if square.x <= x < (square.x + square.width) and square.y <= y < (square.y + square.height):
#                     square.been_there = True  # Set been_there to True if coordinate is within this square
#                     return True
#         return False

#     def count_squares_with_been_there(self, grid):
#         """
#             Count the number of squares in grid that change the attribute been_there to True.
#             :param grid: Board grid. List of lists
#             :return count: Number of squares where the robot have been.
#         """
#         count = 0
#         for row in grid:
#             for square in row:
#                 if square.been_there:
#                     count += 1
#         return count

#     def reset_been_there_to_False(self, grid):
#         """
#             Reset all the squares that changed the attribute been_there to True back to False.
#             :param grid: Board grid. List of lists
#             :return grid: All the square intances attribute been_there are back to False.
#         """

#         for row in grid:
#             for square in row:
#                 if square.been_there:
#                     square.been_there = False

#         return grid

#################################################

# ## Create the board and grid
# board = Board()
# my_grid = board.create_board()

# ## Robot trayectory data
# ## Data as a list of lists
# data = [[-0.0, 0.0], [-0.0, -0.00048], [-0.0, -0.00108], [-0.0, 0.00156], [-0.0, 0.00402], [-0.0, 0.00633], [-0.0, 0.00855], 
#         [-0.0, 0.01071], [-0.0, 0.01283], [-0.0, 0.01496], [-0.0, 0.01712], [-0.0, 0.01935], [-0.0, 0.02167], [-0.0, 0.02294], 
#         [-0.0, 0.02433], [-0.0, 0.02583], [-0.0, 0.02743], [-0.0, 0.02915], [-0.0, 0.03097], [-0.0, 0.03293], [-0.0, 0.03451], 
#         [-0.0, 0.03609], [-0.0, 0.03767], [-0.0, 0.03926], [-0.0, 0.04085], [-0.0, 0.04244], [-0.0, 0.04403], [-0.0, 0.04562], 
#         [-0.0, 0.04722], [-0.0, 0.04882], [-0.0, 0.05041], [-0.0, 0.05201], [-0.0, 0.05361], [-0.0, 0.05521], [-0.0, 0.05681], 
#         [-0.0, 0.0584], [-0.0, 0.06], [-0.0, 0.0616], [-0.0, 0.0632], [-0.0, 0.0648], [-0.0, 0.0664], [-0.0, 0.068], [-0.0, 0.0696]]
# ## Display robot trayectory and board
# board.display_board(data)

# ## Change been_there Square instances attribute to True if the robot has been there
# for coordinates in data:
#     # print(f"\nCoordinates {coordinates}:")
#     # print("Is within a square on the board:", board.is_within_square(coordinates))
#     board.is_within_square(coordinates, my_grid)

# ## Count squares with been_there attribute set to True
# print("\nNumber of squares where 'been_there' is True:", board.count_squares_with_been_there(my_grid))