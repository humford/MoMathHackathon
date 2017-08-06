import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request
from src.run_examples import *
import matplotlib.pyplot as plt, mpld3
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/_example-null')
def exampleNULL():
	return mpld3.fig_to_html(run_example_NULL())

@app.route('/_example-0')
def example0():
	a = request.args.get('a', 0.6, type=float)
	return mpld3.fig_to_html(run_example_0(a))

@app.route('/_example-1')
def example1():
	a = request.args.get('a', 5, type=float)
	return mpld3.fig_to_html(run_example_1(a))

@app.route('/_example-2')
def example2():
	a = request.args.get('a', 0.2, type=float)
	return mpld3.fig_to_html(run_example_2(a))

@app.route('/_example-3')
def example3():
	a = request.args.get('a', 10, type=float)
	return mpld3.fig_to_html(run_example_3(a))

@app.route('/_example-4')
def example4():
	a = request.args.get('a', 5, type=float)
	b = request.args.get('b', 0.2, type=float)
	c = request.args.get('c', 10, type=float)
	return mpld3.fig_to_html(run_example_4(a,b,c))

@app.route('/_example-5')
def example5():
	a = request.args.get('a', 5, type=float)
	b = request.args.get('b', 0.2, type=float)
	c = request.args.get('c', 10, type=float)
	x = request.args.get('x', None, type=float)
	y = request.args.get('y', None, type=float)
	if x == None or y == None:
		pass
	return mpld3.fig_to_html(run_example_play(a,b,c,x,y))

@app.before_first_request
def setup():
	#startup_calculations()
	pass

if __name__ == "__main__":
	app.run()
