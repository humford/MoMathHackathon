#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  integrator.py
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
from scipy.misc import imread
from controllers import *
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
from time import time



def project(arr, i):
	return list(map(lambda x: x[i], arr))

def Return_Graph(controller, params, line, t_max, N):
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
	ax.plot(project(line, 0), project(line, 1), label = "center line", linewidth = 5, linestyle = "--", color = 'y')
	ax.plot(project(sol, 0), project(sol, 1), label = "path", color = 'red')
	ax.axis('off')
	return ax

def Show_Debug_Stats(controller, params, line, t_max, N):
	y0 = [0, 0, 0, 1, 0]
	t = np.linspace(0, t_max, N)
	
	start = time()
	func = car_rate_of_change_function(controller, params, line)
	sol = odeint(func, y0, t)
	print("Time: " + str(time() - start))
	lables = ["x", "y", r"$\theta$", "v", r"$\int error$"]

	for i in range(5):
		if i != 3:
			plt.plot(t, project(sol, i), label = lables[i])

	plt.plot(t, list(map(lambda x: get_error(x[0], x[1], x[2], x[3], x[4], line)[0], sol)), label = "error")
	p = plt.legend()
	plt.show()

def center_line_func(x):
	return (x, 1/(1 + exp(-(10*x-5))))

def main(args):
	N = 25
	Time_Num = 10000
	length = 1
	line = list(map(center_line_func, np.linspace(0, length, N)))
	Return_Graph(PIDcontroller, [100, 2, 5], line, length*2, Time_Num)
	plt.show()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
