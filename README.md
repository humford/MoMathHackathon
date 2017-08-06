# MoMath Hackathon 2017: Control Theory, the Math of Self-Driving Cars

- _Math Exploration: Other Stack_ 
- Henry Williams and Benjamin Church

## The Math

Our project explores control theory and feedback from a visual and intuitive perspective. Specifically, we interactively guide the viewer through constructing a proportion-integral-derivative (PID) controller, one of the simplest and most powerful general control systems. The purpose is to alter the behavior of a dynamical system under some constraints on our control over the dynamics. Phrased another way, a controller is a map from an input signal driving our dynmaical system to an output signal which we hope satisfies some property, generally minimising some measure of error. 

Although highly important to and inspired by engineering, control theory and the larger theory of dynamical systems is highly important in pure and applied mathematics for it forms of the foundation of studies of chaotic and ergodic systems. PID controllers in particular serve as an intuitive representation of the applications of calculus, and thusly blend learning about the underlying mathematical concepts with learning their uses. 

The implementation we built shows the behavior of a second-order differential system under various simple control schemes. The project uses numerical integration to calculate the paths with our error measure being the minimum distance to the target path. These functions representing these paths are shown symbolically and the paths are represented visually on a dynamic web-app.

## The Submission

Our submission comes in the form of a library of Python functions for graphical representations of PID systems and a web-application with a full interactive tour of PID controllers. The mathematical point of our submission is to provide users and museum guests an introduction to the power of control theory through the lens of PID and self-driving cars. 

We illustrate our core mathematical concepts with highly visual and engaging interactive demonstrations of how the different terms in a PID controller add to the whole and accomplish the purpose of autonomous pathfinding. In addition, we endeavour to keep math jargon to an absolute minimum, and to guide our viewers to the important mathematical intuitions of PID controllers though guided questions rather than spelling the answers out. 

Research has shown intuitive introductions to the topics of calculus is often more engaging to young children than algebra and arithmetic. We envision a broad audience, especially with a potential theme of competing self-driving RC cars with PIDs designed by our users. Even so, we'd hope to include more advanced resources with the exhibit for those interested to pursue.

## Additional Notes

### Usage

We have provided two methods of interfacing with our web app:
1. A hosted web-service on the free Heroku hosting platform: [webapp](https://momathhackathon.herokuapp.com/)
   * Since this is a free hosting service, this version is extremely slow and cannot handle many users at a time, it is purely for demonstration purposes
2. A Python Flask server to be run on either a users computer or a computer hosting an exhibit

To host the server locally:
``` 
git clone [this repo]
cd [project folder]
pip install -r requirements.txt
python app.py
```
The local server IP will be provided by Flask.

### Potential Exhibit

In creating our digital platform and visualizations, we hope to lay the groundwork for a potential full exhibit exploring these same concepts. In a full exhibit, the museum could feature real RC cars and allow visitors of all ages to tweak the parameters of their control systems, demostrating how the fundamental concepts of integration and derivation apply to the real world.

### The Team

Benjamin Church is a rising Columbia junior and Henry is a rising high school senior. We attended high school together and competed on the same VEX robotics team, where we learned the fascinating mathematics, engineering, and computer science behind building competition robots. In addition, we competed together on a finalist team in MIT's Battlecode AI Competition.
