import numpy as np
import matplotlib.pyplot as plt

# Initialize the random number generator
rng = np.random.default_rng()

# N-dimensional Monte Carlo function
def montecarlo_nd(ndim, Nsamp, rad):
    points = np.zeros((Nsamp, ndim))
    for i in range(Nsamp):
        for j in range(ndim):
            points[i][j] = rng.random()
    radius = np.linalg.norm(points, axis=1)
    is_inside = radius <= rad
    return (np.sum(is_inside) / Nsamp) * (2**ndim)

# Parameters
d = 25
n = 100000
dims = list(range(d + 1)) 

# Monte Carlo estimation for each dimension
vol = [montecarlo_nd(dim, n, 1) for dim in dims]

# Plotting
plt.plot(dims, vol, color='k')
plt.xlabel("Dimension")
plt.ylabel("Estimated Volume")
plt.title("Volume of N-dimensional unit sphere")
plt.show()
