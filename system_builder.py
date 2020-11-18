"""Build integral system using given G, y, L_0, L_gamma, [a,b], [c,d], [0,T], initial and boundary points."""


from integral_calculation import integrate_monte_carlo
import numpy as np
from solver import construct_lambda


def L1(x1, x2, t, y):
    """Operator that approximates d_t^2 - c*(d_x1^2 + d_x2^2)"""
    c = 1
    delta = 0.05
    d_t2 = y(x1, x2, t + delta) - 2 * y(x1, x2, t) + y(x1, x2, t - delta)
    d_x1_2 = y(x1 + delta, x2, t) - 2 * y(x1, x2, t) + y(x1 - delta, x2, t)
    d_x2_2 = y(x1, x2 + delta, t) - 2 * y(x1, x2, t) + y(x1, x2 - delta, t)
    return (d_t2 - c * (d_x1_2 + d_x2_2)) / delta / delta


class SystemBuilder:
    def __init__(self, data, end_time: float, G: str, func: str):
        """Store problem setting from user's input. Build A(t) and Y for integral system.
        Comments:
            L(d_s) is not much needed as long as we store G.
            We will have only 1 operator for initial + 1 operator for boundary observations. And they are identity
            operators. Maybe, something like L_0(d_t) := d_t is also manageable but lets start with the simplest)
            L_0(d_t) := identity
            l_gamma(d_x) := identity
            G : Grins' operator that corresponds to L(d_s).
            func: system's state. if func == 'choose from file' than we will use data.Func
        """
        self.a, self.b, self.c, self.d = data.a, data.b, data.c, data.d  # boundary of rectangle where system is observed
        self.t0, self.T = 0, end_time  # system is observed at time [0, T]
        self.volume = {'a': self.a, 'b': self.b,
                       'c': self.c, 'd': self.d,
                       't0': self.t0, 'T': self.T}
        self.y = construct_lambda(data.Func if func == 'choose from file' else func)
        self.G = construct_lambda(G)
        self.u = lambda x1, x2, t: L1(x1, x2, t, self.y)  # applying L(d_s) to y
        self.init_points = data.i_points  # points are from [a,b]x[c,d]x{0}
        self.boundary_points = data.b_points  # points are from boundary_of_rectangle x [0, self.T]
        # L_0(d_tau) applied to G(v1-x1, v2 - x2, tau - t)
        self.L_0_G = lambda v1, v2, tau, x1, x2, t: self.G(v1 - x1, v2 - x2, tau - t)
        # L_gamma(d_v1, d_v2) applied to G(v1-x1, v2 - x2, tau - t)
        self.L_gamma_G = lambda v1, v2, tau, x1, x2, t: self.G(v1 - x1, v2 - x2, tau - t)
        self.L_0_y = self.y  # L_0(d_t) applied to y
        self.L_gamma_y = self.y  # L_gamma(d_x1, d_x2) applied to y

        self.Y_0_actual = [self.L_0_y(*point) for point in self.init_points]
        self.Y_gamma_actual = [self.L_gamma_y(*point) for point in self.boundary_points]
        # subtract from Y_actual y_inf  calculated as integral(G(point-s)*u(s)ds)
        self.Y_0 = self.get_Y_modified(self.L_0_G, self.Y_0_actual, self.init_points)
        self.Y_gamma = self.get_Y_modified(self.L_gamma_G, self.Y_gamma_actual, self.boundary_points)
        # set up A_i_j
        self.A11 = np.array([[lambda x1, x2, t: self.L_0_G(v1, v2, tau, x1, x2, t)]
                             for (v1, v2, tau) in self.init_points])
        self.A12 = np.array([[lambda x1, x2, t: self.L_0_G(v1, v2, tau, x1, x2, t)]
                             for (v1, v2, tau) in self.init_points])
        self.A21 = np.array([[lambda x1, x2, t: self.L_0_G(v1, v2, tau, x1, x2, t)]
                             for (v1, v2, tau) in self.boundary_points])
        self.A22 = np.array([[lambda x1, x2, t: self.L_0_G(v1, v2, tau, x1, x2, t)]
                             for (v1, v2, tau) in self.boundary_points])

    def get_Y_modified(self, operator, y_list, points):
        """Subtract from values in y_list  y_inf calculated as integral(G(point-s)*u(s)ds)."""
        return [y_actual - self.integrate_u(operator, point) for y_actual, point in zip(y_list, points)]

    def integrate_u(self, operator, point: tuple) -> float:
        """Integrate on [a,b]x[c,d]x[0,T] operator(point-s)*u(s)"""
        v1, v2, tau = point[:]
        return integrate_monte_carlo(lambda x1, x2, t: operator(v1, v2, tau, x1, x2, t) * self.u(x1, x2, t),
                                     self.volume)
