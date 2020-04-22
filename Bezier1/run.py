from Point2D import Point2D
from GeneralBezier import BezierCurve

if __name__ == "__main__":
    p = [Point2D(0,0), Point2D(10, 5)]

    B = BezierCurve(p)
    B.control_points_from_file("control_points.txt")
    B.plot()