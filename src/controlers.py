#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  controlers.py
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
from scipy.special import expit 

max_rate = 1

def Pcontroler(x, y, theta, v, interror, params):
	return get_error(x,y)*params[0];

def PIcontroler(x, y, theta, v, interror, params):
	return get_error(x,y)*params[0] + det_derror(x, y, theta, v)*params[1];

def get_error(x, y):
	return dist((x, y))
	
def get_derror(x, y):
	return diff_dist((x, y))

def car_rate_of_change_function(controller, params):
	return lambda x, y, theta, v, interror : v*cos(theta), v*sin(theta), max_rate*expit(controller(x, y, interror, params)), 0, get_error(x, y) 
	


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
