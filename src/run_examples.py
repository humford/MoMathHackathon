#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  run_examples.py
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
from scipy.integrate import odeint
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
from time import time

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

def project(arr, i):
	return list(map(lambda x: x[i], arr))

def Graph(controller, params, line, t_max, N, initial_pos):
	y0 = [0, 0, 0, 1, 0]
	t = np.linspace(0, t_max, N)

	start = time()
	func = car_rate_of_change_function(controller, params, line)
	sol = odeint(func, y0, t)
	print("Time: " + str(time() - start))
	lables = ["x", "y", r"$\theta$", "v", r"$\int error$"]

	fig = plt.figure(facecolor='#576b0f')
	ax = fig.add_subplot(111)
	ax.plot(project(line, 0), project(line, 1), label = "center line", linewidth = 50, color = 'k',  path_effects=[pe.Stroke(linewidth = 53, foreground='w'), pe.Normal()])
	ax.plot(project(line, 0), project(line, 1), label = "center line", linewidth = 3, linestyle = "--", color = 'y')
	ax.plot(project(sol, 0), project(sol, 1), label = "path", color = 'red', linewidth = 2, linestyle = "-")
	ax.set_xlim([-1, t_max + 1])
	ax.set_ylim([-0.5, 1.5])
	ax.axis('off')
	return fig

def Show_Debug_Stats(controller, params, line, t_max, N):
	y0 = [0, 0, 0, 1, 0]
	t = np.linspace(0, t_max, N)

	start = time()
	func = car_rate_of_change_function(controller, params, line)
	sol = odeint(func, y0, t)
	print("Time: " + str(time() - start))
	lables = ["x", "y", r"$\theta$", "v", r"$\int error$"]

def center_line_func(x):
	return np.array([x, 1/(1 + exp(-(2*(x-5))))])

def run_example_1(k_p):
	params = [k_p, 0, 0]
	N = 5
	Time_Num = 1000
	length = 10
	line = list(map(center_line_func, np.linspace(0, length, N)))
	return Return_Graph(PIDcontroller, params, line, length, Time_Num)
