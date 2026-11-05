import numpy as np
import matplotlib.pyplot as plt

class uGrid:
    """a finite-difference grid for u"""

    def __init__(self, nx, ng=1, xmin=0.0, xmax=1.0):
        """create a grid with nx points, ng ghost points (on each end)
        that runs from [xmin, xmax]"""

        self.xmin = xmin
        self.xmax = xmax
        self.ng = ng
        self.nx = nx

        # python is zero-based.  Make easy integers to know where the
        # real data lives
        self.ilo = ng
        self.ihi = ng+nx-1

        # physical coords
        self.dx = (xmax - xmin)/(nx-1)
        self.x = xmin + (np.arange(nx+2*ng)-ng)*self.dx

        # storage for the solution
        self.u = self.scratch_array()
        self.uinit = self.scratch_array()
        
    def scratch_array(self):
        """ return a scratch array dimensioned for our grid """
        return np.zeros((self.nx+2*self.ng), dtype=np.float64)

    def fill_BCs(self):
        """ fill the a single ghostcell with periodic boundary conditions """
        self.u[self.ilo-1] = self.u[self.ihi-1]
        self.u[self.ihi+1] = self.u[self.ilo+1]
        
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(self.x[self.ilo:self.ihi+1], self.uinit[self.ilo:self.ihi+1],
                label="initial conditions")
        ax.plot(self.x[self.ilo:self.ihi+1], self.u[self.ilo:self.ihi+1])
        ax.legend()
        return fig

def burgers_upwind(ul, ur):
    """ solve rieman problem for burgers using upwind """

    # use the average ul and ur to determine direction
    ua = 0.5*(ul+ur)
    if ua > 0:
        return ul**2/2
    else:
        return ur**2/2

def burgers_fv(nx, C, tmax, init_cond, xmin=-10.0, xmax=10.0):
    g = uGrid(nx, xmin=xmin, xmax=xmax)

    # set the initial conditions before using u
    init_cond(g)
    g.uinit[:] = g.u[:]

    unew = g.scratch_array()
    F = g.scratch_array()
    t = 0.0

    while t < tmax:
        g.fill_BCs()

        # recompute dt each step, limited by the fastest wave
        umax = np.max(np.abs(g.u[g.ilo:g.ihi+1]))
        dt = min(C*g.dx/umax, tmax - t)

        # start at ilo-1 so that F[ilo-1] is set
        for i in range(g.ilo-1, g.ihi+1):
            F[i] = burgers_upwind(g.u[i], g.u[i+1])

        for i in range(g.ilo, g.ihi+1):
            unew[i] = g.u[i] - dt/g.dx*(F[i] - F[i-1])

        g.u[:] = unew[:]
        t += dt

    g.fill_BCs()
    return g


def burgers_upwind_nc(nx, C, tmax, init_cond, xmin=-10.0, xmax=10.0):
    g = uGrid(nx, xmin=xmin, xmax=xmax)

    # set the initial conditions before using u
    init_cond(g)
    g.uinit[:] = g.u[:]

    unew = g.scratch_array()
    t = 0.0

    while t < tmax:
        g.fill_BCs()

        # recompute dt each step, limited by the fastest wave
        umax = np.max(np.abs(g.u[g.ilo:g.ihi+1]))
        dt = min(C*g.dx/umax, tmax - t)

        # start at ilo-1 so that F[ilo-1] is set
        for i in range(g.ilo-1, g.ihi+1):
            if g.u[i] > 0:
                dudx = (g.u[i]-g.u[i-1])/g.dx
            elif u[i] < 0:
                dudx = (g.u[i+1]-g.u[i])/g.dx   
            else:
                dudx = 0.
            unew[i] = g.u[i]*(1 - dt*dudx)

        g.u[:] = unew[:]
        t += dt

    g.fill_BCs()
    return g

class Fluid1DGrid:
    """a finite-difference grid for fluid variables"""

    def __init__(self, nx, ng=1, xmin=0.0, xmax=1.0):
        """create a grid with nx points, ng ghost points (on each end)
        that runs from [xmin, xmax]"""

        self.xmin = xmin
        self.xmax = xmax
        self.ng = ng
        self.nx = nx

        # python is zero-based.  Make easy integers to know where the
        # real data lives
        self.ilo = ng
        self.ihi = ng+nx-1

        # physical coords
        self.dx = (xmax - xmin)/(nx-1)
        self.x = xmin + (np.arange(nx+2*ng)-ng)*self.dx

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
        """ fill the ghost cells of a[variable, zone] with open boundary conditions """
        a[:, :self.ilo] = a[:, self.ilo, np.newaxis]
        a[:, self.ihi+1:] = a[:, self.ihi, np.newaxis]
        

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


def euler_fv(nx, C, tmax, init_cond, xmin=-10.0, xmax=10.0):
    """ Integrate Euler's equations with the finite volume method

    init_cond(g) must set g.rho, g.u and g.p in place. Returns the grid g, with the
    final solution in g.rho, g.u, g.p and g.w.
    """

    # set adiabatic index
    gamma = 5./3.

    g = Fluid1DGrid(nx, xmin=xmin, xmax=xmax)

    init_cond(g)
    g.winit[:] = g.w[:]

    U = prim2cons(g.w, gamma)
    Unew = np.zeros_like(U)
    F = np.zeros_like(U)
    t = 0.0

    while t < tmax:
        g.fill_BCs(U)
        W = cons2prim(U, gamma)

        # recompute dt each step, limited by the fastest wave
        rho, u, p = W[:, g.ilo:g.ihi+1]
        csmax = np.max(np.abs(u) + np.sqrt(gamma*p/rho))
        dt = min(C*g.dx/csmax, tmax - t)

        for i in range(g.ilo-g.ng, g.ihi+g.ng):
            F[:, i] = rsolver(W[:, i], W[:, i+1], gamma)

        for i in range(g.ilo, g.ihi+1):
            Unew[:, i] = U[:, i] - dt/g.dx*(F[:, i] - F[:, i-1])

        U[:] = Unew[:]
        t += dt

    g.fill_BCs(U)
    g.w[:] = cons2prim(U, gamma)
    return g