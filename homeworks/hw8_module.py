import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# NOTE: DO NOT MODIFY THE CODE BELOW THIS LINE

# set adiabatic index
gamma = 5./3.

class SedovExact:
    """Self-similar strong-shock solution, used only for comparison.

    With R(t) = xi0 (E0 t^2 / rho0)^(1/5) and xi = r/R, the profiles are
        rho = rho0 frho(xi),  u = Rdot fu(xi),  p = rho0 Rdot^2 fp(xi).
    The similarity ODEs are integrated inward from the strong-shock jump conditions at
    xi = 1, and energy conservation then fixes xi0.
    """

    def __init__(self, gamma, xi_min=1e-3):

        def rhs(s, y):
            xi = np.exp(s)
            fu, frho, fp = y[0], np.exp(y[1]), np.exp(y[2])
            a = fu - xi
            ratio = fp/(frho*a)
            dfu = (1.5*fu - ratio*(3.0 - 2.0*gamma*fu/xi))/(a - gamma*ratio)
            dlnfrho = -(dfu + 2.0*fu/xi)/a
            dlnfp = (3.0 - gamma*(dfu + 2.0*fu/xi))/a
            return [xi*dfu, xi*dlnfrho, xi*dlnfp]  # derivatives in s = ln(xi)

        y0 = [
            2.0/(gamma + 1.0),
            np.log((gamma + 1.0)/(gamma - 1.0)),
            np.log(2.0/(gamma + 1.0)),
        ]
        s_eval = np.linspace(0.0, np.log(xi_min), 4000)
        sol = solve_ivp(rhs, (0.0, s_eval[-1]), y0, method="Radau", t_eval=s_eval,
                        rtol=1e-9, atol=1e-11)
        if not sol.success:
            raise RuntimeError(f"Similarity integration failed: {sol.message}")

        # reverse the arrays so that xi increases, as np.interp requires
        self.xi = np.exp(sol.t)[::-1]
        self.fu = sol.y[0][::-1]
        self.frho = np.exp(sol.y[1])[::-1]
        self.fp = np.exp(sol.y[2])[::-1]

        integrand = (0.5*self.frho*self.fu**2 + self.fp/(gamma - 1.0))*self.xi**2
        integral = np.sum(0.5*(integrand[1:] + integrand[:-1])*np.diff(self.xi))
        self.xi0 = (16.0*np.pi/25.0*integral)**(-0.2)

    def shock_radius(self, t, E0=1.0, rho0=1.0):
        return self.xi0*(E0*t**2/rho0)**0.2

    def profiles(self, x, t, E0=1.0, rho0=1.0):
        """Return the exact rho, u and p at radii x, with no ambient pressure."""
        R = self.shock_radius(t, E0, rho0)
        Rdot = 0.4*R/t
        xi = np.asarray(x)/R
        inside = xi <= 1.0

        rho = np.full_like(xi, rho0, dtype=float)
        u = np.zeros_like(xi, dtype=float)
        p = np.zeros_like(xi, dtype=float)
        rho[inside] = rho0*np.interp(xi[inside], self.xi, self.frho)
        u[inside] = Rdot*np.interp(xi[inside], self.xi, self.fu)
        p[inside] = rho0*Rdot**2*np.interp(xi[inside], self.xi, self.fp)
        return rho, u, p

def rsolver(wl, wr, gamma=5/3):
    """
    Returns the flux vector given the left state wl and the right state wr.  The state vectors
    are organized as
    
    wl[0]: left mass density; wr[0]: right mass density;
    wl[1]: left velocity;     wr[1]: right velocity;
    wl[2]: left pressure;     wr[2]: right pressure;
        
    The returned flux vector is for the conserved variables (rho, rho*u, E).
    """
    
    # Decompose the states.
    rhol, ul, pl = wl
    rhor, ur, pr = wr
    
    # Compute Roe-averaged state
    sqrtdl = np.sqrt(rhol)   
    sqrtdr = np.sqrt(rhor)
    isdlpdr = 1 / (sqrtdl + sqrtdr)
    
    roed = sqrtdl * sqrtdr
    roevx = (sqrtdl * ul + sqrtdr * ur) * isdlpdr
    el = pl / (gamma - 1) + 0.5 * rhol * ul**2
    er = pr / (gamma - 1) + 0.5 * rhor * ur**2
    # enthalpy
    roeh = ((el + pl) / sqrtdl + (er + pr) / sqrtdr) * isdlpdr
    
    # Compute sound speed in L,R, and Roe-averaged state
    cl = np.sqrt(gamma * pl / rhol)
    cr = np.sqrt(gamma * pr / rhor)
    q = max([roeh - 0.5 * roevx**2, 0.0])
    a = np.sqrt((gamma - 1) * q)

    # Compute the max/min wave speeds based on L/R and Roe-averaged values
    al = min([roevx - a, ul - cl])
    ar = max([roevx + a, ur + cr])
    bp = max([ar, 0.0])
    bm = min([al, 0.0])
        
    # Compute L/R fluxes along the lines bm/bp: F_L - (S_L)U_L; F_R - (S_R)U_R
    fl = np.zeros(3,)
    fr = np.zeros(3,)
    
    fl[0] = rhol * (ul - bm)
    fr[0] = rhor * (ur - bp)
    fl[1] = rhol * ul * (ul - bm) + pl
    fr[1] = rhor * ur * (ur - bp) + pr
    fl[2] = el * (ul - bm) + pl * ul
    fr[2] = er * (ur - bp) + pr * ur
    
    if bp != bm:
        tmp = 0.5 * (bp + bm) / (bp - bm)
    else:
        tmp = 0
    return 0.5 * (fl + fr) + (fl - fr) * tmp

def prim2cons(W, gamma):
    """ convert W = (rho, u, p) to U = (rho, rho*u, E), indexed [variable, zone] """
    U = np.zeros_like(W)
    U[0] = W[0]
    U[1] = W[0] * W[1]
    U[2] = W[2] / (gamma - 1) + 0.5 * W[0] * W[1]**2
    return U
 
def cons2prim(U, gamma):
    """ convert U = (rho, rho*u, E) to W = (rho, u, p), indexed [variable, zone] """
    W = np.zeros_like(U)
    W[0] = U[0]
    W[1] = U[1] / U[0]
    W[2] = (gamma - 1) * (U[2] - 0.5 * U[1]**2 / U[0])
    return W

# NOTE: DO NOT MODIFY THE CODE ABOVE THIS LINE

# Modify the code included below

class SphericalFluid1DGrid:

    """a finite-volume grid for fluid variables in spherical symmetry"""

    def __init__(self, nx, ng=1, xmin=0.0, xmax=1.3):
        """create a grid with nx zones, ng ghost zones (on each end)
        that runs from [xmin, xmax]"""

        self.xmin = xmin
        self.xmax = xmax
        self.ng = ng
        self.nx = nx

        # python is zero-based.  Make easy integers to know where the
        # real data lives
        self.ilo = ng
        self.ihi = ng+nx-1


        # physical coords: the zones fill [xmin, xmax], with x_{i-1/2} = x_i - dx/2
        # and x_{i+1/2} = x_i + dx/2, so an interface (not a zone center) sits at r = 0
        self.dx = (xmax - xmin)/nx
        self.x = xmin + (np.arange(nx+2*ng)-ng+0.5)*self.dx
        self.xm = self.x - 0.5*self.dx
        self.xp = self.x + 0.5*self.dx

        # A[i] is the area of the interface at x_{i+1/2}, V[i] is the volume of zone i
        self.A = 4*np.pi*self.xp**2
        self.V = 4*np.pi/3*(self.xp**3 - self.xm**3)

        # storage for the w vector (primitive variables), w[0] = rho, w[1] = u, w[2] = p
        self.w = np.zeros((3, nx+2*ng), dtype=np.float64)
        self.winit = np.zeros((3, nx+2*ng), dtype=np.float64)
        # rho, u and p are views into w, so assign to them in place, e.g. g.rho[:] = 1.0
        self.rho, self.u, self.p = self.w
        self.rhoinit, self.uinit, self.pinit = self.winit
        
    def scratch_array(self):
        """ return a scratch array dimensioned for our grid """
        return np.zeros((self.nx+2*self.ng), dtype=np.float64)

    def fill_BCs(self, a):
        """ fill the ghost zones of a[variable, zone]: reflecting at the center,
        open at the outer boundary """
        # FILL IN CODE BELOW FOR EXERCISE 1(a)
        


def euler_fv_spherical(nx, C, tmax, init_cond, xmin=0.0, xmax=1.3):
    """ Integrate Euler's equations in spherical symmetry with the finite volume method

    init_cond(g) must set g.rho, g.u and g.p in place. Returns the grid g, with the
    final solution in g.rho, g.u, g.p and g.w.
    """

    g = SphericalFluid1DGrid(nx, xmin=xmin, xmax=xmax)

    init_cond(g)
    g.winit[:] = g.w[:]

    U = prim2cons(g.w, gamma)
    Unew = np.zeros_like(U)
    F = np.zeros_like(U)
    t = 0.0

    while t < tmax:
        g.fill_BCs(U)
        W = cons2prim(U, gamma)

        # stop with an error rather than letting NaNs end the loop silently
        rho, u, p = W[:, g.ilo:g.ihi+1]
        if not (np.all(rho > 0) and np.all(p > 0)):
            raise RuntimeError(f"Non-positive density or pressure at t = {t:.4g}")

        # recompute dt each step, limited by the fastest wave
        cmax = np.max(np.abs(u) + np.sqrt(gamma*p/rho))
        dt = min(C*g.dx/cmax, tmax - t)

        # F[:, i] is the flux at x_{i+1/2}
        for i in range(g.ilo-g.ng, g.ihi+g.ng):
            # FILL IN CODE BELOW FOR EXERCISE 1(b)
            F[:, i] = 

        for i in range(g.ilo, g.ihi+1):
            # flux difference, weighted by the interface areas
            # FILL IN CODE BELOW FOR EXERCISE 1(b)
            Unew[:, i] = 

        U[:] = Unew[:]
        t += dt

    g.fill_BCs(U)
    g.w[:] = cons2prim(U, gamma)
    return g


class Disk1DGrid:

    """a finite-volume grid for disk variables in cylindrical symmetry"""
    # FILL IN CODE BELOW FOR EXERCISE 2(a)