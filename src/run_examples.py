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
from scipy.interpolate import interp1d

max_rate = 2.5
rd_width = 0.75
max_steps = 1000
Time_Num = 1000
N = 30
length = 10
vert = 6

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

def Graph(controller, params, line, t_max, initial_pos, line_func):
	y0 = np.array([initial_pos[0], initial_pos[1], 0, 1, 0])
	t = np.linspace(0, t_max, Time_Num)

	start = time()
	func = car_rate_of_change_function(controller, params, line)
	sol = my_odeint(func, y0, t)
	print("Integration Time: " + str(time() - start))

	xnew = np.linspace(0, length, 100)
	smooth = list(map(line_func, xnew))

	lables = ["x", "y", r"$\theta$", "v", r"$\int error$"]
	fig = plt.figure(facecolor='#576b0f', figsize = (7,5))
	ax = fig.add_subplot(111)

	cut = len(sol)

	for i in range(len(sol)):
		if sol[i][0] > length:
			cut = i
			break

	print("Time to Finish: " + str(t[i]))

	ax.plot(project(smooth, 0), project(smooth, 1), label = "shoulder", linewidth = 52, color = 'w')
	ax.plot(project(smooth, 0), project(smooth, 1), label = "road", linewidth = 50, color = 'k')
	ax.plot(project(smooth, 0), project(smooth, 1), label = "center line", linewidth = 3, linestyle = "--", color = 'y')
	ax.plot(project(sol[:cut], 0), project(sol[:cut], 1), label = "path", color = 'red', linewidth = 2, linestyle = "-")
	ax.set_xlim([-1.5, length + 1.30])
	ax.set_ylim([-1.5, vert + 1.5])
	ax.axis('off')
	return fig

center_line_func = lambda x : np.array([x, 6/(1 + exp(-(10*(x-5))))])

def curve(t):
		return np.array([t + sin(3.9*(t-5))*exp(-0.5*(t-5)**2), 6*exp(-(t-5)**2)])

s = 1.69

def cube_root(x):
	return sign(x)*pow(abs(x), 1/3)

def exp_thing(a, t):
	return exp(-1/(5**(s*a)) * (t-5)**int(2*a))

def nasty_curve(a, t):
	return np.array([(5 + (a-1)*cube_root(sin(2*pi/10*t)))*exp_thing(a, t) + t * (1-exp_thing(a, t)), (6*t/10)*exp_thing(a, t) + 6/(1 + exp(5-t)) * (1-exp_thing(a,t))])


examples_dics = dict()

def run_example_NULL():
	line = list(map(lambda x : (x, 0), np.linspace(0, length, N)))
	xnew = np.linspace(line[0][0],line[N-1][0], 100)
	smooth = list(map(interp1d(project(line, 0), project(line, 1)), xnew))

	fig = plt.figure(facecolor='#576b0f', figsize = (7,5))
	ax = fig.add_subplot(111)

	ax.plot(xnew, smooth, label = "shoulder", linewidth = 52, color = 'w')
	ax.plot(xnew, smooth, label = "road", linewidth = 50, color = 'k')
	ax.plot(xnew, smooth, label = "center line", linewidth = 3, linestyle = "--", color = 'y')
	ax.set_xlim([-1.5, 11.30])
	ax.set_ylim([-1.5, 7.5])
	ax.axis('off')
	return fig


def get_key(ident, k, a):
	return str(ident) + "k:" + str(k) + "rd:" + str(a)

def run_example_0(k_c, a):
	if not get_key(0, k_c, a) in examples_dics:
		params = [k_c, 0, 0]
		t_max = 20*(1+a/6)
		if a < 1 or a > 6:
			func = center_line_func
		else:
			func = lambda x : nasty_curve(a, x)
		line = list(map(func, np.linspace(0, length, N)))
		examples_dics[get_key(0, k_c, a)] =  Graph(CRAPcontroller, params, line, t_max, np.array([0,0]), func)
		print("DID CALC")
	return examples_dics[get_key(0, k_c, a)]

def run_example_1(k_p, a):
	if not get_key(1, k_p, a) in examples_dics:
		params = [k_p, 0, 0]
		t_max = 17*(1+a/6)
		if a < 1 or a > 6:
			func = center_line_func
		else:
			func = lambda x : nasty_curve(a, x)
		line = list(map(func, np.linspace(0, length, N)))
		examples_dics[get_key(1, k_p, a)] = Graph(PIDcontroller, params, line, t_max, np.array([0,0]), func)
		print("DID CALC")
	return examples_dics[get_key(1, k_p, a)]



def run_example_2(k_i, a):
	if not get_key(2, k_i, a) in examples_dics:
		params = [10, k_i, 0]
		t_max = 17*(1+a/6)
		if a < 1 or a > 6:
			func = center_line_func
		else:
			func = lambda x : nasty_curve(a, x)
		line = list(map(func, np.linspace(0, length, N)))
		examples_dics[get_key(2, k_i, a)] = Graph(PIDcontroller, params, line, t_max, np.array([0,0]), func)
		print("DID CALC")
	return examples_dics[get_key(2, k_i, a)]

road_type_dict3 = dict()

def run_example_3(k_d, a):
	if not get_key(3, k_d, a) in examples_dics:
		for k_d in np.linspace(0, 20, 10):
			example3_body(k_d, a)
		print("DID CALC")
	return examples_dics[get_key(3, k_d, a)]

def example3_body(k_d, a):
	params = [10, 0, k_d]
	t_max = 16*(1 + a/6)
	if a < 1 or a > 6:
		func = center_line_func
	else:
		func = lambda x : nasty_curve(a, x)
	line = list(map(func, np.linspace(0, length, N)))
	examples_dics[get_key(3, k_d, a)] = Graph(PIDcontroller, params, line, t_max, np.array([0,0]), func)

def run_example_4(k_p, k_i, k_d, a):
	params = [k_p, k_i, k_d]
	t_max = 16*(1+a/6)
	if a < 1 or a > 6:
		func = center_line_func
	else:
		func = lambda x : nasty_curve(a, x)
	line = list(map(func, np.linspace(0, length, N)))
	return Graph(PIDcontroller, params, line, t_max, np.array([0,0]), func)


def run_example_play(k_p, k_i, k_d, mouse_x, mouse_y):
	params = [k_p, k_i, k_d]
	t_max = 22
	new_N = 50
	line = list(map(curve, np.linspace(0, length, new_N)))
	return Graph(PIDcontroller, params, line, t_max, np.array([mouse_x, mouse_y]), curve)

def startup_calculations():
	for k_c in np.linspace(0, 2, 10):
		run_example_0(k_c)
	for k_p in np.linspace(0, 10, 10):
		run_example_1(k_p)
	for k_i in np.linspace(0, 1, 10):
		run_example_2(k_i)
	for k_d in np.linspace(0, 20, 10):
		run_example_3(k_d)
	print("SETUP COMPLETE")
