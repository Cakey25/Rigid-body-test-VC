This is a simple rigid body physics engine that I programmed myself and by using resources found on this page: 
https://www.myphysicslab.com/engine2D/collision-en.html

<img width="1191" height="777" alt="image" src="https://github.com/user-attachments/assets/bc012fb2-1785-4636-88a3-721038a9ff46" />

The example that is currently in the project is a simple scene with a rotating, unmoving shape and a shape that the user
can control.
You can see collisions by running into the shape and having it hit you away.
There are many things to be improved about this project, specifically the collision detection and finding the collision point and
normal accurately in some edge cases which I am going to improve in the future.
Another current limitation is all practical collision detection algorithms only work on convex shapes and right now my program
cannot break up a concave shape into multiple convex ones which will lead to errors when creating a shape that is concave.

To run the project run main.py. The only dependacies are pygame and numpy.
To move the "player" around, you can use w,a,s,d.
