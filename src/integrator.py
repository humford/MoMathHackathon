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

from run_examples import *

def Show_Debug_Stats(controller, params, line, t_max, N):
	y0 = [0, 0, 0, 1, 0]
	t = np.linspace(0, t_max, N)

	start = time()
	func = car_rate_of_change_function(controller, params, line)
	sol = my_odeint(func, y0, t)
	print("Time: " + str(time() - start))
	lables = ["x", "y", r"$\theta$", "v", r"$\int error$"]

	for i in range(5):
		if i != 3:
			plt.plot(t, project(sol, i), label = lables[i])

	plt.plot(t, list(map(lambda x: get_error(x[0], x[1], x[2], x[3], x[4], line)[0], sol)), label = "error")
	plt.plot(t, list(map(lambda x: get_error(x[0], x[1], x[2], x[3], x[4], line)[2], sol)), label = r"$\frac{d}{dt} error$")
	p = plt.legend()
	plt.show()


def main(args):
	params = [10, 1, 0]
	N = 10
	Time_Num = 10000
	length = 10
	t_max = 20
	center_line_func = lambda x : np.array([x, 6/(1 + exp(-(10*(x-5))))])

	line = list(map(center_line_func, np.linspace(0, length, N)))
	#Show_Debug_Stats(PIDcontroller, params, line, t_max, Time_Num)
	
	#input()
	
	run_example_3(1)
	#plt.savefig("road.png")
	plt.show()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
