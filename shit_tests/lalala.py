import numpy as np
import matplotlib.pyplot as plt

# N-dimensional Monte Carlo function
def montecarlo_nd(ndim, Nsamp, rad):
    points = np.random.rand(Nsamp, ndim)
    radius = np.linalg.norm(points, axis=1)
    is_inside = radius <= rad
    return (np.sum(is_inside) / Nsamp) * (2**float(ndim))

n_vals = np.arange(1,1_000_00,1)
pi_vals = np.zeros_like(n_vals,dtype=float)
for i in range(len(n_vals)):
    pi_vals[i] = montecarlo_nd(2,n_vals[i],1)
print('done')
plt.plot(n_vals, pi_vals, 'k') 
plt.axhline(np.pi, color = 'r')
plt.show()

# # Parameters
# d = 25
# n = 1000
# dims = list(range(d + 1)) 

# # Monte Carlo estimation for each dimension
# vol = [montecarlo_nd(dim, n, 1) for dim in dims]

# # Plotting
# plt.plot(dims, vol, color='k', marker = '.')
# plt.xlabel("Dimension")
# plt.ylabel("Estimated Volume")
# plt.title("Volume of N-dimensional unit sphere")
# plt.show()

