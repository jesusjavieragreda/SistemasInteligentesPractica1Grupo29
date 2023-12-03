import os
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import json
import numpy as np


##############################################################
# USE INSTRUCTIONS:
#   At the bottom of this file, modify the global variables
#   to specify the JSON file and the generated routes.
#
#   The file will automatically plot an image with the path,
#   and store it in the current folder
##############################################################

def save_images_map(name, routes):
    """Show the city map."""
    with open(name, "r") as file:
        dictionary = json.load(file)

    root = os.path.splitext(name)[0]

    city = dictionary["city"]
    rows = city["rows"]
    columns = city["columns"]
    blocked = city["blocked"]
    departure = dictionary["departure"]
    dangers = dictionary["dangers"]
    trapped = dictionary["trapped"]

    # Sanity check to verify the number of routes
    condition = len(routes) == len(trapped)
    message = "Number of routes and trapped people mismatch."
    assert condition, message
    
    # Convert all routes into upper-case to avoid problems
    routes = [[action.upper() for action in route] for route in routes]

    start = 0
    step = 1
    xtickslabels = np.arange(start, columns, step)
    ytickslabels = np.arange(start, rows, step)

    # Positionate the ticks in the mid of the cell
    xticks = xtickslabels + 0.5
    yticks = ytickslabels + 0.5

    shape = (rows, columns)
    dtype = int
    city = np.zeros(shape, dtype)

    x, y = zip(*blocked)
    city[x, y] = 1

    x, y = zip(*dangers)
    city[x, y] = 2

    x, y = departure
    city[x, y] = 3

    for index, (x, y) in enumerate(trapped):
        # Avoid modifications in the original matrix
        matrix = np.copy(city)
        matrix[x, y] = 4

        figsize = (rows, columns)
        figure, axis = plt.subplots(figsize = figsize)

        edgecolors = "k"
        colors = ["white", "black", "red", "green", "yellow"]
        cmap = ListedColormap(colors)
        plt.pcolor(matrix, cmap = cmap, edgecolors = edgecolors)

        # Invert to start from the "UP"per "LEFT" corner
        axis.invert_yaxis()

        axis.set_xticks(xticks)
        axis.set_xticklabels(xtickslabels)

        axis.set_yticks(yticks)
        axis.set_yticklabels(ytickslabels)

        # Display the x-axis ticks at the top
        axis.tick_params(axis = "x",
                         which = "both",
                         bottom = False,
                         labelbottom = False,
                         top = True,
                         labeltop = True)

        # Define the values to increment for drawing the arrows
        up = (0.5, 0.75, 0.5, 0.25)
        down = (0.5, 0.25, 0.5, 0.75)
        left = (0.75, 0.5, 0.25, 0.5)
        right = (0.25, 0.5, 0.75, 0.5)
        increments = {"UP": up, "DOWN": down, "LEFT": left, "RIGHT": right}

        # Define the values to increment for moving the position
        up = (0, -1)
        down = (0, 1)
        left = (-1, 0)
        right = (1, 0)
        movements = {"UP": up, "DOWN": down, "LEFT": left, "RIGHT": right}

        # Use abscissa style for the plot
        y, x = departure
        arrowprops = {"arrowstyle": "->"}

        for action in routes[index]:
            action = str.upper(action)
            a, b, c, d = increments[action]

            xytext = (x + a, y + b)
            xy = (x + c, y + d)
            plt.annotate("", xy = xy, xytext = xytext, arrowprops = arrowprops)

            dx, dy = movements[action]
            x, y = x + dx, y + dy


        output = root + "_" + str(index) + ".png"
        plt.savefig(output, bbox_inches = "tight")
        
        
#################################
# MODIFY THE FOLLOWING VARIABLES
#################################

if __name__ == "__main__":
    # Name of the JSON file representing the problem
    # The file should be in the folder indicated in the folder as a first argument
    json_name = os.path.join("./folder", "instance-30-18-12-3-12-2023.json")
    
    # List of actions written in "UP" - "RIGHT" - "DOWN" - "LEFT" format.
    # NON-CASE SENSITIVE
    # This will be the returning list of sequences (one per search/trapped person)
    routes = [
    ["UP", "UP", "UP", "UP", "UP", "UP", "UP", "UP", "UP", "UP", "UP", "UP", "UP", "LEFT", "LEFT"],
    ["DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "LEFT", "LEFT", "LEFT", "LEFT"],
    ["DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "DOWN", "LEFT", "LEFT"]]
    
    # Calls the method
    save_images_map(json_name, routes)

