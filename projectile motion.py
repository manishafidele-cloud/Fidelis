from manim import *
import numpy as np

class ProjectileMotion(Scene):
    def construct(self):
        # Physics setup
        g = 9.8
        v0 = 10          # initial speed
        angle = 45        # launch angle in degrees
        theta = angle * DEGREES

        vx = v0 * np.cos(theta)
        vy = v0 * np.sin(theta)
        t_flight = 2 * vy / g  # total time of flight

        # Axes
        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[0, 6, 1],
            x_length=9,
            y_length=5,
            axis_config={"include_tip": True},
        ).add_coordinates()
        axes.to_edge(DOWN)

        labels = axes.get_axis_labels(x_label="x", y_label="y")

        self.play(Create(axes), Write(labels))

        # Position function scaled into axes coordinates
        def pos(t):
            x = vx * t
            y = vy * t - 0.5 * g * t**2
            return axes.c2p(x, y)

        # Trajectory path (full parabola, drawn as a guide)
        trajectory = axes.plot_line_graph(
            x_values=[vx * t for t in np.linspace(0, t_flight, 200)],
            y_values=[vy * t - 0.5 * g * t**2 for t in np.linspace(0, t_flight, 200)],
            line_color=GRAY,
            add_vertex_dots=False,
        )

        # Moving projectile
        ball = Dot(color=RED, radius=0.12).move_to(pos(0))

        # Trace that follows the ball
        trace = TracedPath(ball.get_center, stroke_color=YELLOW, stroke_width=3)

        # Info text
        info = Text(f"v0 = {v0} m/s, angle = {angle}°", font_size=28).to_edge(UP)
        self.play(Write(info))

        self.add(trace, ball)

        # Animate the projectile along the path using a ValueTracker
        t_tracker = ValueTracker(0)
        ball.add_updater(lambda m: m.move_to(pos(t_tracker.get_value())))

        self.play(t_tracker.animate.set_value(t_flight), run_time=4, rate_func=linear)

        ball.clear_updaters()
        self.play(Create(trajectory))

        self.wait(1)