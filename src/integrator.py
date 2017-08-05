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
from controllers import *
import numpy as np
from matplotlib import pyplot as plt

def project(arr, i):
	return list(map(lambda x: x[i], arr))

def Return_Integration(controller, params, line, t_max, N):
	y0 = [0, 0, 0, 1, 0]
	t = np.linspace(0, t_max, N)
	sol = odeint(car_rate_of_change_function(controller, params, line), y0, t)
	lables = ["x", "y", r"$\theta$", "v", r"$\int error$"]

	for i in range(5):
		if i != 3:
			plt.plot(t, project(sol, i), label = lables[i])

	plt.plot(t, list(map(lambda x: get_error(x[0], x[1], x[2], x[3], x[4], line)[0], sol)), label = "error")
	plt.legend()

	plt.figure()
	plt.plot(project(line, 0), project(line, 1), label = "center line")
	plt.plot(project(sol, 0), project(sol, 1), label = "path")
	plt.legend()
	plt.plot()
	plt.show()

	return t, sol

def center_line_func(x):
	return (x, 1/(1 + exp(-(10*x-5))))

def main(args):
	N = 100
	Time_Num = 1000
	length = 1
	line = list(map(center_line_func, np.linspace(0, length, N)))
	Return_Integration(PIDcontroller, [100, 10, 5], line, length*2, Time_Num)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
