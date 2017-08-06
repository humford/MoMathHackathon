# MoMath Hackathon 2017: Control Theory, the Math of Self-Driving Cars

- _Math Exploration: Other Stack_ 
- Henry Williams and Benjamin Church

## The Math

Our project explores control theory and feedback from a visual and intuitive perspective. Specifically we interactively guide the viewer through constructing a proportion-integral-derivative (PID) controller, one of the simplest and most powerful general control systems. The purpose is to alter the behavior of a dynamical system under some constraints on our control over the dynamics. Phrased another way, a controller is a map from an input signal driving our dynmaical system to an output signal which we hope satisfies some property, generally minimising some measure of error. 

Although highly important to and inspired by engineering, control theory and the larger theory of dynamical systems is highly important in pure and applied mathematics for it forms of the foundation of studies of chaotic and ergodic systems. PID controllers in particular serve as an intuitive representation of the applications of calculus, and thusly blend learning about the underlying mathematical concepts with learning their uses. 

The implimentation we built shows the behavior of a second-order differential system under various simple control schemes. The project uses numerical integration to calculate the paths with our error measure being the minimum distance to the target path. These functions representing these paths are shown symbolically and the paths are represented visually on a dynamic web-app.

## The Submission

Our submission comes in the form of a library of python functions for graphical representations of PID systems and a web-application with a full tour. The point of our submission is to 

A short but thorough explanation of your submission. What is the mathematical "point" of your submission? How does it illustrate the mathematical concepts you describe in an engaging way? Who do you envision the target audience to be?

## Additional Notes

### Usage

We have provided two methods of interfacing with our web app:
1. A hosted web-service on the free Heroku hosting platform: [webapp](https://momathhackathon.herokuapp.com/)
  
2. A Flask server to be run 

### Potential Exhibit

In creating our digital platform and visualizations, we hope to lay the groundwork for a potential full exhibit exploring these same concepts. In a full exhibit, the museum could feature real RC cars 

### The Team
