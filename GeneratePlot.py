from BezierCurve import BezierCurve
from Point2D import Point2D
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

p = [Point2D(0,0), Point2D(10, 5)]
B = BezierCurve(p)
B.load_control_points_from_file("control_points.txt")

def plot(B):
    plt.style.use("classic")
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.3)
    plt.title("Bezier Curve")
    plt.xlabel("X [position]")
    plt.ylabel("Y [Position]")
    ax.set_aspect("equal")
    
    bezier_main_path, = plt.plot([], [], color ='black', linestyle="dashed")
    control_point_path = plt.plot([], [], color='blue')
    points, = plt.plot([], [], color='gray', marker='x', linestyle="dashed")
    left_trajectory, = plt.plot([], [], color="red")
    right_trajectory, = plt.plot([], [], color="red")

    def update(t):
        B.load_control_points_from_file("control_points.txt")
        waypoints = B.get_points()
        x_points = [point[0] for point in waypoints]
        y_points = [point[1] for point in waypoints]

        points.set_data(x_points, y_points)
        
        ax.set_xlim(min(x_points)-1, max(x_points)+1)
        ax.set_ylim(min(y_points)-1, max(y_points)+1)
        ax.set_aspect("equal")

        bezier_x = B.x_coords()[:int(t*199)]
        bezier_y = B.y_coords()[:int(t*199)]
        bezier_main_path.set_data(bezier_x, bezier_y)

        trajectory_points = B.get_normal_points()[:int(t*199)]
        trajectory_x_points = [point[0] for point in trajectory_points]
        trajectory_y_points = [point[1] for point in trajectory_points]
        
        left_trajectory_x_points = [bezier_x[i] + trajectory_x_points[i] for i in range(len(trajectory_x_points))]
        left_trajectory_y_points = [bezier_y[i] + trajectory_y_points[i] for i in range(len(trajectory_y_points))]
        left_trajectory.set_data(left_trajectory_x_points, left_trajectory_y_points)

        right_trajectory_x_points = [bezier_x[i] - trajectory_x_points[i] for i in range(len(trajectory_x_points))]
        right_trajectory_y_points = [bezier_y[i] - trajectory_y_points[i] for i in range(len(trajectory_y_points))]
        right_trajectory.set_data(right_trajectory_x_points, right_trajectory_y_points)
        

    t_slider = plt.axes([0.25, 0.15, 0.50, 0.02])
    time_slider = Slider(t_slider, "t", 0, 1, 0)
    time_slider.on_changed(update)

    plt.show()

if __name__ == "__main__":
    plot(B)