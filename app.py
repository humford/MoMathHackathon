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
	a = request.args.get('a', 10, type=int)
	return mpld3.fig_to_html(run_example_0(a))

@app.route('/_example-1')
def example1():
	a = request.args.get('a', 10, type=int)
	return mpld3.fig_to_html(run_example_1(a))

@app.route('/_example-2')
def example2():
	a = request.args.get('a', 10, type=int)
	return mpld3.fig_to_html(run_example_2(a))

if __name__ == "__main__":
	app.run()
