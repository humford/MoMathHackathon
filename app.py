from flask import Flask, render_template, request
from matplotlib
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/_example-1')
def example1():
	a = request.args.get('a', 0, type=int)
	return "<p>" + str(a) + "</p>"

if __name__ == "__main__":
	app.run()
