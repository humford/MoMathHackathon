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

max_rate = 6.28

def sign(x):
	if x >= 0:
		return 1
	else:
		return -1

def PIDcontroller(x, y, theta, v, interror, params, line):
	return np.dot(get_error(x, y, theta, v, interror, line), params)
	
def sq_dist(a, b):
	return sum((a-b)**2)
	
def projection(v, w, p):
	l2 = sq_dist(v, w)
	if l2 == 0:
		return v
	else:
		t = max(0, min(1, np.dot(p - v, w - v)/l2))
		return v + t*(w - v)

def minimum_distance(v, w, p):
	return sq_dist(p, projection(v, w, p))

def get_error(x, y, theta, v, interror, line):
	
	my_pos = np.array([x, y])
	best_dist = sq_dist(my_pos, line[0])
	best_i = 0
	
	for i in range(0, len(line)-1):
		d = minimum_distance(line[i], line[i+1], my_pos)
		if d < best_dist:
			best_i = i
			best_dist = d
			
	p = projection(line[best_i], line[best_i+1], my_pos)
	dist = sqrt(minimum_distance(line[best_i], line[best_i+1], my_pos))

	if dist == 0:
		return [0, interror, v]
	else:
		return [sign((x - p[0])*sin(theta) - (y - p[1])*cos(theta))*dist, interror, (x - p[0])/dist * v*cos(theta) + (y - p[1])/dist * v*sin(theta)]


def car_rate_of_change_function(controller, params, line):
	return lambda y, t : (y[3]*cos(y[2]), y[3]*sin(y[2]), y[3]*max_rate*tanh(controller(y[0], y[1], y[2], y[3], y[4], params, line)), 0, get_error(y[0], y[1], y[2], y[3], y[4], line)[0])


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
