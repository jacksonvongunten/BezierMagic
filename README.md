# BezierMagic
Implementation of a general Bezier Curve utilizing the explicit formula for path planning purposes.
See https://en.wikipedia.org/wiki/B%C3%A9zier_curve for more information.

## Use
Open run.py and run to see an example of the use, note that matplotlib is the only dependency.
There are a few python files, Point2D which adds a class to define coordinates and give their Cartestian and Polar representation, MathHelperFunctions which is a class of static functions relating to mathematical operations needed, and GeneralBezier, which defines a class for our Bezier Curve.

By altering the array "p" in run.py you can change the endpoints, and by altering "control_points" you can change where the control points are located and how many there are, effectively allowing you to change the path.
