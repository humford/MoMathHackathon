#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  controllers.py
#
#  Copyright 2017 Benjamin Church <ben@U430>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from math import *
import numpy as np

max_rate = 3

def sign(x):
	if x >= 0:
		return 1
	else:
		return -1

def PIDcontroller(x, y, theta, v, interror, params, line):
	return np.dot(get_error(x, y, theta, v, interror, line), params)

def get_dist(x, y, p):
	return sqrt((x - p[0])**2 + (y - p[1])**2)

def get_error(x, y, theta, v, interror, line):
	
	best_dist = get_dist(x, y, line[0])
	best_i = 0
	
	for i in range(0, len(line)):
		d = get_dist(x, y, line[i])
		if d < best_dist:
			best_i = i
			best_dist = d
			

	p = line[best_i]
	dist = get_dist(x, y, p)

	if dist == 0:
		return [0, interror, v]
	else:
		return [sign((x - p[0])*sin(theta) - (y - p[1])*cos(theta))*dist, interror, (x - p[0])/dist * v*cos(theta) + (y - p[1])/dist * v*sin(theta)]


def car_rate_of_change_function(controller, params, line):
	return lambda y, t : (y[3]*cos(y[2]), y[3]*sin(y[2]), max_rate*tanh(controller(y[0], y[1], y[2], y[3], y[4], params, line)), 0, get_error(y[0], y[1], y[2], y[3], y[4], line)[0])


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
