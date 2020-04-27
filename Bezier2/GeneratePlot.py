from BezierCurve import BezierCurve
from Point2D import Point2D
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, CheckButtons
from matplotlib.patches import Circle

p = [Point2D(0,0), Point2D(5,15)]
B = BezierCurve(p)
B.load_control_points_from_file("control_points.txt")
trackwidth = 1

def plot(B):
    plt.style.use("classic")
    fig, ax = plt.subplots()
    ax.grid()
    plt.subplots_adjust(bottom=0.3)
    plt.title("Bezier Curve")
    plt.xlabel("X [position]")
    plt.ylabel("Y [Position]")
    ax.set_aspect("equal")
    
    bezier_main_path, = plt.plot([], [], color ='black', linestyle="dashed")
    points, = plt.plot([], [], color='gray', marker='x', linestyle="dashed")
    left_trajectory, = plt.plot([], [], color="red")
    right_trajectory, = plt.plot([], [], color="red")
    curvature_circle = Circle((0,0), 0)
    curvature_circle.fill = False
    curvature_circle.set_visible(False)
    ax.add_artist(curvature_circle)

    B.load_control_points_from_file("control_points.txt")
    waypoints = B.get_points()
    x_points = [point[0] for point in waypoints]
    y_points = [point[1] for point in waypoints]

    points.set_data(x_points, y_points)

    ax.set_xlim(min(x_points)-1, max(x_points)+1)
    ax.set_ylim(min(y_points)-1, max(y_points)+1)
    ax.set_aspect("equal")

    def hide_curvature(label):
        curvature_circle.set_visible(not curvature_circle.get_visible())
        plt.draw()

    def update(t):
        B.load_control_points_from_file("control_points.txt")
        waypoints = B.get_points()
        x_points = [point[0] for point in waypoints]
        y_points = [point[1] for point in waypoints]

        points.set_data(x_points, y_points)
        
        ax.set_xlim(min(x_points)-1, max(x_points)+1)
        ax.set_ylim(min(y_points)-1, max(y_points)+1)
        ax.set_aspect("equal")
       
        if (t != 0):
            set_size = B.get_t().size
            bezier_main_path.set_data(B.x[:int(t*set_size-1)], B.y[:int(t*set_size-1)])

            trajectory_points = B.get_normal_points()[:int(t*set_size-1)]
            trajectory_x_points = [point[0] for point in trajectory_points]
            trajectory_y_points = [point[1] for point in trajectory_points]
            
            left_trajectory_x_points = [B.x[i] + (trackwidth/2)*trajectory_x_points[i] for i in range(len(trajectory_x_points))]
            left_trajectory_y_points = [B.y[i] + (trackwidth/2)*trajectory_y_points[i] for i in range(len(trajectory_y_points))]
            left_trajectory.set_data(left_trajectory_x_points, left_trajectory_y_points)

            right_trajectory_x_points = [B.x[i] - (trackwidth/2)*trajectory_x_points[i] for i in range(len(trajectory_x_points))]
            right_trajectory_y_points = [B.y[i] - (trackwidth/2)*trajectory_y_points[i] for i in range(len(trajectory_y_points))]
            right_trajectory.set_data(right_trajectory_x_points, right_trajectory_y_points)

            if B.get_curvature_at_t(t):
                radius = 1/(B.get_curvature_at_t(t))
            else:
                radius = 0
            
            if trajectory_x_points:
                curvature_center_x = B.x[int(t*set_size-1)] + trajectory_x_points[-1]*radius
                curvature_center_y = B.y[int(t*set_size-1)] + trajectory_y_points[-1]*radius
                curvature_circle.center = curvature_center_x, curvature_center_y
                curvature_circle.radius = radius
            else:
                curvature_circle.center = 0, 0
                curvature_circle.radius = 0
            
            B.get_headings()

            fig.canvas.update()
        else:
            bezier_main_path.set_data([], [])
            left_trajectory.set_data([], [])
            right_trajectory.set_data([], [])
            curvature_circle.center = 0, 0
            curvature_circle.radius = 0
            ax.add_artist(curvature_circle)

    t_slider = plt.axes([0.25, 0.15, 0.50, 0.02])
    time_slider = Slider(t_slider, "t", 0, 1, 0)
    time_slider.on_changed(update)

    button_ax = plt.axes([0.45, 0.04, 0.1, 0.1])
    labels = ["Curvature"]
    button = CheckButtons(button_ax, labels)
    button.on_clicked(hide_curvature)

    plt.show()

if __name__ == "__main__":
    plot(B)
    B.generate_file_of_dense_points()
    B.get_velocities_along_path(2.5, 7.5, 15)
    B.generate_file_of_states(1)