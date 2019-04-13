# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:32:46 2019

@author: roman
"""

import numpy as np
import math
from math import sin, cos, radians

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
        c+=6 #thickness of the sticks in the corners is 6cm
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
        corn = self.get_corner(corner)
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

        #Calculate rotation angle based on vehicle coordinates
        #TODO
        """not sure if alpha or theta is correct angle, I used solution from:
    https://math.stackexchange.com/questions/158679/how-to-calculate-coordinates-of-third-point-in-a-triangle-2d-knowing-2-points
    second answer."""
        theta = (self.vehicle_loc[0] - corn[0])/AB
        theta = math.degrees(math.asin(theta))
        
        alpha = (self.vehicle_loc[1] - corn[1])/AB
        aplha = math.degrees(math.acos(alpha))
        
        point = rotate_point((Cy, Cx), theta, (0,0)) 
        self.objects += [point]
        #TODO: figure out solution for all corners (or any reference point), now it works only for (0,0)
        print("Coordinates of object", obj_name,"are",round(point[1],0),round(point[0],0))
        return point

    #obj takes coordinates of a known object as a touple
    #angle is the angle between the known object and a new object
    #distance is the distance of the new object from out vehicle
    #correct location of the vehicle has to be stored in self.vehicle
    #TODO
    def add_by_objects(self, obj, angle, distance):
        return
        
    def find_route(self):
        #use TSP solution from the other code here? 
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
        return c

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
arena.vehicle_loc = (22,33)
#                       c           a     angle B
arena.add_by_corner(1, 39.661,'A',24.331 ,  24.228)

