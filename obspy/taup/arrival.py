#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

from math import pi


class Arrival(object):
    """
    Convenience class for storing the parameters associated with a phase
    arrival.
    """
    def __init__(self, phase, distance, time, purist_dist, ray_param,
                 ray_param_index, name, purist_name, source_depth,
                 takeoff_angle, incident_angle):
        # phase that generated this arrival
        self.phase = phase
        # actual distance in degrees
        self.distance = distance
        # travel time in seconds
        self.time = time
        # purist angular distance (great circle) in radians
        self.purist_dist = purist_dist
        # ray parameter in seconds per radians
        self.ray_param = ray_param
        self.ray_param_index = ray_param_index
        # phase name
        self.name = name
        # phase name changed for true depths
        self.purist_name = purist_name
        # source depth in kilometers
        self.source_depth = source_depth
        self.incident_angle = incident_angle
        self.takeoff_angle = takeoff_angle
        # pierce and path points
        self.pierce = None
        self.path = None

    def __str__(self):
        return "%s phase arrival at %.3f seconds" % (self.phase.name,
                                                     self.time)

    @property
    def ray_param_sec_degree(self):
        """
        Returns the ray parameter in seconds per degree.
        """
        return self.ray_param * pi / 180.0

    @property
    def purist_distance(self):
        return self.purist_dist * 180.0 / pi