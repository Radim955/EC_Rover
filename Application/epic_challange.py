# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:32:46 2019

@author: roman
"""

import numpy as np
import math
from math import sin, cos, radians
import matplotlib.pyplot as plt

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 16:46:21 2019

@author: roman
"""

"""Simple travelling salesman problem on a circuit board."""

import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model(objects):
    """Stores the data for the problem."""
    data = {}
    # Locations in block units
    #HERE WE PUT THE COORDINATES OF DISCOVERED OBJECTS:
    data['locations'] = objects  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances


def print_solution(manager, routing, assignment, labels):
    """Prints assignment on console."""
    print('Distance: {}cm'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(labels[index])
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(labels[0])
    print(plan_output)
    plan_output += 'Objective: {}m\n'.format(route_distance)


def main(objects, labels):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(objects)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['locations']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(manager, routing, assignment, labels)

class Arena:
    def __init__(self, size=250, scale=1, start=(125, 250)):
        self.size = size
        self.scale = scale
        self.objects = [start]
        self.object_names = ['Start']
        self.vehicle_loc = start

    #corners are numbered 1..2  
    #                     3..4  
    #c is distance from corner in cm
    #wall direction can be 'R' or 'L' which means Right and Left from the vehicle
    #b is distance from the nearest wall in cm
    #returns coordinates in y,x format
    def vehicle_location(self, corner, c, wall_direction, b):
        c+=6 #thickness of the sticks in the corners is 6cm
        c *= self.scale
        b *= self.scale
        a = self.scale * int(round(math.sqrt((c**2) - (b**2)), 0))
        loc = (0,0)
        if corner == 1:
            if wall_direction == 'R':
                loc = (b,a)
            else:
                loc = (a,b)
        if corner == 2:
            if wall_direction == 'R':
                loc = (a, self.size - b)
            else:
                loc = (b,self.size - a)
        if corner == 3:
            if wall_direction == 'R':
                loc = (self.size-a, b)
            else:
                loc = (self.size - b, a)
        if corner == 4:
            if wall_direction == 'R':
                loc = (self.size - b, self.size-a-1)
            else:
                loc = (self.size-a-1, self.size-b-1)
        self.vehicle_loc = loc
        return loc #maybe this is also (y,x) and needs swap?

    #c_dist is distance of our vehicle from the corner
    #obj_name is the name (letter) of the object
    #obj_dist is distance of the new object from our vehicle
    #angle is the angle between new object and the corner
    def add_by_corner(self, corner, c_dist, obj_name, obj_dist, angle):
        corn = self.get_corner(corner)
        ref_point = corn
        #here we calculate the distance of the new obj from the corner
        obj_c_dist = distance(c_dist, obj_dist, angle)
        """https://math.stackexchange.com/questions/543961/determine-third-point-of-triangle-when-two-points-and-all-sides-are-known """
        """https://www.triangle-calculator.com/?what=vc"""
        
        #just making variable names easier to read and put into formulas
        c = AB = c_dist
        a = BC = obj_dist
        b = AC = obj_c_dist

        #These two lines calculate correct coordinates only if vehicle is at (0, c_dist)
        Cy = ((AB**2) + (AC**2) -(BC**2))/(2*AB)
        Cx = math.sqrt((AC**2)-(Cy**2))

        
        """
    https://math.stackexchange.com/questions/158679/how-to-calculate-coordinates-of-third-point-in-a-triangle-2d-knowing-2-points
    second answer."""
        #Calculate rotation angle based on vehicle coordinates
        m = (self.vehicle_loc[0] - ref_point[0])/AB      #sin(x)
        n = (self.vehicle_loc[1] - ref_point[1])/AB      #cos(x)
        theta = math.degrees(math.atan2(m, n))           # x

        point = rotate_point((Cx, Cy), theta, (0,0))
        point = (point[1], point[0]) #I have no idea why we need to swap this but it works like that
        self.objects += [point]
        self.object_names += [obj_name]
        #TODO: figure out solution for all corners (or any reference point), now it works only for (0,0)
        print("Coordinates of object", obj_name,"are",round(point[1],0),round(point[0],0))
        return point

    #obj takes coordinates of a known object as a tuple
    #angle is the angle between the known object and a new object
    #distance is the distance of the new object from out vehicle
    #correct location of the vehicle has to be stored in self.vehicle
    #TODO
    def add_by_objects(self, obj, angle, distance):
        return
        
    def find_route(self):
        main(self.objects, self.object_names)
        return
    
    def get_corner(self, corner):
        if corner == 1:
            c = (0,0)
        elif corner == 2:
            c = (0, self.size-1)
        elif corner == 3:
            c = (self.size-1, 0)
        else:
            c = (self.size-1, self.size-1)
        return (c[1],c[0]) #it returned coordinates in (y, x) so I flip it here

    def get_names(self):
        for i,a in enumerate(self.object_names):
            print("%d --> %s" % (i, a))

    def add_obj(self, name, x, y):
        self.objects += [(x,y)]
        self.object_names += [name]

    def list_obj(self):
        for o, n in zip(self.objects, self.object_names):
            print("%s --> %s" % (n, o))

    def show(self):
        plt.figure()
        plt.axis([0,250,0,250])
        plt.grid(False)
        plt.scatter(*zip(*self.objects))
        ax=plt.gca()                            # get the axis
        ax.set_ylim(ax.get_ylim()[::-1])        # invert the axis
        ax.xaxis.tick_top()                     # and move the X-Axis      
        ax.yaxis.tick_left()
        plt.show()

#calculate distance between two objects, given their distances (a, b) from the
#vehicle and angle between them
def distance(a, b, angle):
        return math.sqrt((a**2)+(b**2)-(2*a*b*(math.cos(math.radians(angle)))))

#calculates Euclidean distance between two coordinates
def distance_coordinates(a, b):
        anp = np.array(a)
        bnp = np.array(b)
        return np.linalg.norm(anp-bnp)

def rotate_point(point, angle, center_point=(0, 0)):
    """Rotates a point around center_point(origin by default)
    Angle is in degrees.
    Rotation is counter-clockwise
    """
    angle_rad = math.radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    new_point = (point[0] - center_point[0], point[1] - center_point[1])
    new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                 new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
    # Reverse the shifting we have done
    new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point

#PLAYGROUND
""" get test inputs from https://www.triangle-calculator.com/?what=vc"""
arena = Arena()
arena.add_obj('A', 30, 250-55)
arena.add_obj('B', 140, 250-126)
arena.add_obj('C', 65, 74)
arena.add_obj('D', 100+65, 120)
arena.add_obj('E', 250-42, 250-45)
arena.add_obj('F', 250-58, 10)
arena.add_obj('G', 250-100, 250-78)
arena.add_obj('H', 48, 55)
arena.add_obj('I', 16, 20)
arena.add_obj('J', 250-88, 28)
arena.find_route()
arena.show()
#928 expected
