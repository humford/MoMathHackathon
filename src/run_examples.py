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
import matplotlib
#matplotlib.use('Agg')
from math import *
from scipy.integrate import odeint
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
from time import time
from operator import add

max_rate = 2.5
rd_width = 0.75
max_steps = 1000
Time_Num = 1000
N = 10
length = 10

def sign(x):
	if x >= 0:
		return 1
	else:
		return -1

def CRAPcontroller(x, y, theta, v, interror, params, line):
	err = get_error(x, y, theta, v, interror, line)[0]
	if err > rd_width:
		return params[0]
	elif err < -rd_width:
		return -params[0]
	else:
		return 0

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
	
def cross(a, b):
	return a[0]*b[1] - a[1]*b[0]

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
	
	v_unit_vec = np.array([cos(theta), sin(theta)])

	if dist == 0:
		return [0, interror, v]
	else:
		c = cross((my_pos - p), v_unit_vec)
		if np.dot((my_pos - p), v_unit_vec) < 0:
			err = dist*sign(c)*pow(abs(c), 0.25)
		else:
			err = dist*sign(c)
		
	return [err, interror, sign(err)*v*np.dot((my_pos - p), v_unit_vec)]


def car_rate_of_change_function(controller, params, line):
	return lambda y, t : (y[3]*cos(y[2]), y[3]*sin(y[2]), y[3]*max_rate*tanh(controller(y[0], y[1], y[2], y[3], y[4], params, line)), 0, get_error(y[0], y[1], y[2], y[3], y[4], line)[0])

def project(arr, i):
	return list(map(lambda x: x[i], arr))

def my_odeint(func, y0, t):
	sol = [y0]*len(t)
	dt = t[1] - t[0]
	for i in range(len(t) - 1):
		sol[i + 1] = sol[i] + np.array(func(sol[i], t[i]))*dt
	return sol

def Graph(controller, params, line, t_max, N, initial_pos):
	y0 = np.array([initial_pos[0], initial_pos[1], 0, 1, 0])
	t = np.linspace(0, t_max, N)

	start = time()
	func = car_rate_of_change_function(controller, params, line)
	sol = my_odeint(func, y0, t)
	print("Time: " + str(time() - start))
	lables = ["x", "y", r"$\theta$", "v", r"$\int error$"]
	fig = plt.figure(facecolor='#576b0f', figsize = (7,5))
	ax = fig.add_subplot(111)
	ax.plot(project(line, 0), project(line, 1), label = "center line", linewidth = 50, color = 'k',  path_effects=[pe.Stroke(linewidth = 53, foreground='w'), pe.Normal()])
	ax.plot(project(line, 0), project(line, 1), label = "center line", linewidth = 3, linestyle = "--", color = 'y')
	ax.plot(project(sol, 0), project(sol, 1), label = "path", color = 'red', linewidth = 2, linestyle = "-")
	ax.set_xlim([-1.5, 11.30])
	ax.set_ylim([-1.5, 7.5])
	ax.axis('off')
	return fig

examples_dics = dict()

def run_example_NULL():
	line = list(map(lambda x : (x, 0), np.linspace(0, length, N)))
	fig = plt.figure(facecolor='#576b0f', figsize = (7,5))
	ax = fig.add_subplot(111)
	ax.plot(project(line, 0), project(line, 1), label = "center line", linewidth = 50, color = 'k',  path_effects=[pe.Stroke(linewidth = 53, foreground='w'), pe.Normal()])
	ax.plot(project(line, 0), project(line, 1), label = "center line", linewidth = 3, linestyle = "--", color = 'y')
	ax.set_xlim([-1.5, 11.30])
	ax.set_ylim([-1.5, 7.5])
	ax.axis('off')
	return fig


def run_example_0(k_c):
	if not "kc:" + str(k_c) in examples_dics:
		params = [k_c/15, 0, 0]
		t_max = 20
		center_line_func = lambda x : np.array([x, 6/(1 + exp(-(8*(x-5))))])
		line = list(map(center_line_func, np.linspace(0, length, N)))
		examples_dics["kc:" + str(k_c)] =  Graph(CRAPcontroller, params, line, t_max, Time_Num, np.array([0,0]))
		print("DID CALC")
	return examples_dics["kc:" + str(k_c)]

def run_example_1(k_p):
	if not "kp:" + str(k_p) in examples_dics:
		params = [k_p, 0, 0]
		t_max = 17
		center_line_func = lambda x : np.array([x, 6/(1 + exp(-(10*(x-5))))])
		line = list(map(center_line_func, np.linspace(0, length, N)))
		examples_dics["kp:" + str(k_p)] = Graph(PIDcontroller, params, line, t_max, Time_Num, np.array([0,0]))
		print("DID CALC")
	return examples_dics["kp:" + str(k_p)]

def run_example_2(k_i):
	if not "ki:" + str(k_i) in examples_dics:
		params = [10, k_i/20, 0]
		t_max = 17
		center_line_func = lambda x : np.array([x, 6/(1 + exp(-(10*(x-5))))])
		line = list(map(center_line_func, np.linspace(0, length, N)))
		examples_dics["ki:" + str(k_i)] = Graph(PIDcontroller, params, line, t_max, Time_Num, np.array([0,0]))
		print("DID CALC")
	return examples_dics["ki:" + str(k_i)]
	
def run_example_3(k_d):
	if not "kd:" + str(k_d) in examples_dics:
		params = [10, 0, 2*k_d]
		t_max = 16
		center_line_func = lambda x : np.array([x, 6/(1 + exp(-(10*(x-5))))])
		line = list(map(center_line_func, np.linspace(0, length, N)))
		examples_dics["kd:" + str(k_d)] = Graph(PIDcontroller, params, line, t_max, Time_Num, np.array([0,0]))
		print("DID CALC")
	return examples_dics["kd:" + str(k_d)]

def run_example_4(k_p, k_i, k_d):
	params = [k_p, k_i/20, 2*k_d]
	t_max = 16
	center_line_func = lambda x : np.array([x, 6/(1 + exp(-(10*(x-5))))])
	line = list(map(center_line_func, np.linspace(0, length, N)))
	return Graph(PIDcontroller, params, line, t_max, Time_Num, np.array([0,0]))
	
def run_example_play(k_p, k_i, k_d, mouse_x, mouse_y):
	params = [k_p, k_i/20, 2*k_d]
	N = 10
	Time_Num = 10000
	length = 10
	t_max = 16
	center_line_func = lambda x : np.array([x, 6/(1 + exp(-(10*(x-5))))])
	line = list(map(center_line_func, np.linspace(0, length, N)))
	return Graph(PIDcontroller, params, line, t_max, Time_Num, np.array([mouse_x, mouse_y]))
