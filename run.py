from Point2D import Point2D
from GeneralBezier import GeneralBezier

if __name__ == "__main__":
    p = [Point2D(0,0), Point2D(5,5)]
    control_points = [Point2D(1,8), Point2D(3, 10), Point2D(5,8)]

    B = GeneralBezier(p)
    B.add_control_points(control_points)
    B.plot()