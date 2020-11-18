"""Solver for integral system that operates in time and in 2d space"""


from integral_calculation import integrate_monte_carlo as integrate_
import math
import numpy as np
import re


class SolveTheIntegral:
    """Solve system of integral equations."""

    def __init__(self, system):
        """Initialize matrix-function A, scalar vec b, set up volumes for integration."""

        self.A11, self.A12, self.A21, self.A22 = system.A11, system.A12, system.A21, system.A22
        self.Y = np.array(system.Y_0 + system.Y_gamma).reshape((-1, 1))
        self.a, self.b, self.c, self.d = system.a, system.b, system.c, system.d
        self.t0, self.T = system.t0, system.T
        self.t0_inf = -5
        self.bound = 5
        self.G = system.G
        self.u_inf = system.u
        self.actual_sol = system.y
        self.volume_outer = {'a': self.a - self.bound, 'b': self.b + self.bound,
                             'c': self.c - self.bound, 'd': self.d + self.bound,
                             't0': self.t0, 'T': self.T}
        self.volume_inner = system.volume
        self.volume_pre_history = {'a': self.a, 'b': self.b,
                                   'c': self.c, 'd': self.d,
                                   't0': self.t0_inf, 'T': self.t0 }

    def integrate_0(self, matrix):
        """Integrate matrix on [t0_inf, 0] in rectangle in which system is observed."""
        print('calc pre-history integral')
        return integrate_matrix(matrix, self.volume_pre_history)

    def integrate_gamma(self, matrix):
        """Integrate matrix on [0,T], outside rectangle in which system is observed."""
        print('calc gamma integral')
        return integrate_matrix(matrix, self.volume_outer) - integrate_matrix(matrix, self.volume_inner)

    def calculate_u(self, P_inv):
        """Calculate solution to the integral system."""
        vec = np.dot(P_inv, self.Y)
        A = np.vstack((
            np.hstack((self.A11, self.A12)),
            np.hstack((self.A21, self.A22))
        ))
        return multiply(A.T, vec,
                        lin_combination)

    def calculate_error(self, P, P_inv):
        """Calculate error (||integral[A(t)u(t)]-Y||^2)."""
        return np.dot(self.Y.transpose(),
                      self.Y - np.dot(P, np.dot(P_inv, self.Y)))

    def calculate_P(self):
        """Calculate P as integral A*A_T.
        The main difficulty is that there are different volumes for A11 and A12 and etc."""
        P_11 = self.integrate_0(multiply(
            self.A11, self.A11.transpose(), inner_product)) + self.integrate_gamma(multiply(
            self.A12, self.A12.transpose(), inner_product))
        P_12 = self.integrate_0(multiply(
            self.A11, self.A21.transpose(), inner_product)) + self.integrate_gamma(multiply(
            self.A12, self.A22.transpose(), inner_product))
        P_21 = self.integrate_0(multiply(
            self.A21, self.A11.transpose(), inner_product)) + self.integrate_gamma(multiply(
            self.A22, self.A12.transpose(), inner_product))
        P_22 = self.integrate_0(multiply(
            self.A21, self.A21.transpose(), inner_product)) + self.integrate_gamma(multiply(
            self.A22, self.A22.transpose(), inner_product))
        P = np.vstack((
            np.hstack((P_11, P_12)),
            np.hstack((P_21, P_22)))
        )
        print(P)
        return P

    def build_sol(self, u_0, u_gamma):
        """Build solution as integral(G*u_inf)+integral(G*u_0)+integral(G*u_gamma)."""
        return lambda v1, v2, tau: self.integrate_0(
            np.array([[lambda x1, x2, t: self.G(v1 - x1, v2 - x2, tau - t) * u_0(x1, x2, t)]])
        ) + integrate_(
            lambda x1, x2, t: self.G(v1 - x1, v2 - x2, tau - t) * self.u_inf(x1, x2, t),
            self.volume_inner) + self.integrate_gamma(
            np.array([[lambda x1, x2, t: self.G(v1 - x1, v2 - x2, tau - t) * u_gamma(x1, x2, t)]]))

    def solve(self):
        """Find  u_0, u_gamma and build y(x1, x2, t) based on found u_."""
        P = self.calculate_P()
        P_inv = np.linalg.pinv(P)
        u_0, u_gamma = self.calculate_u(P_inv).flatten()
        error = self.calculate_error(P, P_inv)
        print('Error of inverting integral system', error)
        return [self.build_sol(u_0, u_gamma), self.actual_sol]


def integrate_matrix(matrix, volume):
    """Integrate matrix which contains lambdas on [t0,T]."""
    result = np.full(matrix.shape, fill_value=0.)
    for row in range(matrix.shape[0]):
        for col in range(row, matrix.shape[1]):
            result[row, col] = integrate_(matrix[row, col], volume)
            if col < matrix.shape[0] and row < matrix.shape[1]:
                result[col, row] = result[row, col]
    return result


def multiply(A, B, inner_prod_func):
    """Multiply A and B - matrices containing lambdas/scalars."""
    n_rows, n_cols = A.shape[0], B.shape[1]
    result = np.full((n_rows, n_cols), fill_value=None, dtype=A.dtype)
    for row in range(n_rows):
        for col in range(n_cols):
            result[row, col] = inner_prod_func(A[row], B[:, col])
    return result


def add_lambdas_impl(f, g):
    """Create lambda function as sum of given."""
    return lambda x1, x2, t: f(x1, x2, t) + g(x1, x2, t)


def add_lambdas(lambda_f, lambda_g):
    """Create np.array with lambdas that are sums of given."""
    result = np.full(lambda_f.shape, None, object)
    for i in range(lambda_f.shape[0]):
        result[i, 0] = add_lambdas_impl(lambda_f[i, 0], lambda_g[i, 0])
    return result


def lin_combination(lambdas, scalars):
    """Create lambda function as linear combination of lambdas."""
    return lambda x1, x2, t: sum([f(x1, x2, t) * coef for (f, coef) in zip(lambdas, scalars)])


def inner_product(lambda_f, lambda_g):
    """Create lambda function as inner product of lambdas from given arrays."""
    return lambda x1, x2, t: sum([f(x1, x2, t) * g(x1, x2, t) for (f, g) in zip(lambda_f, lambda_g)])


def H(x):
    """Heaviside function."""
    return x > 0


def validate_expr(expr, c=1):
    """Modify string expr so as to make it a valid python expression of variables x1, x2, t.
    Add module prefix('math.') for functions in expr from math module.
    Replace 'c' with some value, replace '^' with '**', replace 'r' with 'sqrt(x1**2+x2**2)'
    """
    expr = expr.replace('^', '**').replace('r^2', '(x1**2+x2**2)')
    math_list = [obj_name for obj_name in dir(math) if not obj_name.startswith('__')]
    new_expr = ''
    while expr:
        match = re.search(r'[^()\*\-\+/ ]+', expr)
        if match:
            part = match.group()
            start, end = match.start(), match.end()
            if part in math_list:
                part = 'math.' + part
            elif part == 'c':
                part = str(c)
            elif part == 'r':
                part = 'math.sqrt(x1**2+x2**2)'
            new_expr += expr[:start] + part
            expr = expr[end:]
        else:
            new_expr += expr
            expr = ''
    return new_expr


def construct_lambda(expr):
    """Construct lambda function from string expression with variables x1, x2, t."""
    header = 'lambda x1, x2, t: '
    expr = validate_expr(str(expr))
    return eval(header + expr)
