# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:32:46 2019

@author: roman
"""

import numpy as np
import math

class Arena:
    def __init__(self, size=250, scale=1, start=(249, 125)):
        self.size = size
        self.scale = scale
        self.objects = [start]
        self.vehicle_loc = start

    #corners are numbered 1..2  
    #                     3..4  
    #c is distance from corner in cm
    #wall direction can be 'R' or 'L' which means Right and Left from the vehicle
    #b is distance from the nearest wall in cm
    #returns coordinates in y,x format
    def vehicle_location(self, corner, c, wall_direction, b):
        c *= self.scale
        b *= self.scale
        a = self.scale * int(round(math.sqrt((c**2) - (b**2)), 0))
        if corner == 1:
            if wall_direction == 'R':
                return (b,a)
            else:
                return (a,b)
        if corner == 2:
            if wall_direction == 'R':
                return (a, self.size - b)
            else:
                return (b,self.size - a)
        if corner == 3:
            if wall_direction == 'R':
                return (self.size-a, b)
            else:
                return (self.size - b, a)
        if corner == 4:
            if wall_direction == 'R':
                return (self.size - b, self.size-a-1)
            else:
                return (self.size-a-1, self.size-b-1)

    #c_dist is distance of our vehicle from the corner
    #obj_name is the name (letter) of the object
    #obj_dist is distance of the new object from our vehicle
    #angle is the angle between new object and the corner
    #TODO
    def add_by_corner(self, corner, c_dist, obj_name, obj_dist, angle):
        if corner == 1:
            c = (0,0)
        elif corner == 2:
            c = (0, self.size-1)
        elif corner == 3:
            c = (self.size-1, 0)
        else:
            c = (self.size-1, self.size-1)
        #here we calculate the distance of the new obj from the corner
        obj_corn_dist = distance_coordinates(c, self.vehicle_loc)

    #obj takes coordinates of a known object as a touple
    #angle is the angle between the known object and a new object
    #distance is the distance of the new object from out vehicle
    #correct location of the vehicle has to be stored in self.vehicle
    #TODO
    def add_by_objects(self, obj, angle, distance):
        return
        
    def find_route(self):
        #use TSP from the other code here? 
        return

#calculate distance between two objects, given their distances (a, b) from the
#vehicle and angle between them
def distance(self, a, b, angle):
        c = math.sqrt((a**2)+(b**2)-(2*a*b*(math.cos(math.radians(angle)))))
        print(c)

#calculates Euclidean distance between two coordinates
def distance_coordinates(a, b):
        return math.hypot(a.first - a.second, b.first - b.second)

arena = Arena()
print(arena.vehicle_location(1,25,'L',10))
