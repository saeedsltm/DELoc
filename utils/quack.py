# Import modules.
import numpy as np
import pykonal
import matplotlib.pyplot as plt

# Instantiate EikonalSolver object using Cartesian coordinates.
solver = pykonal.EikonalSolver(coord_sys="cartesian")
# Set the coordinates of the lower bounds of the computational grid.
# For Cartesian coordinates this is x_min, y_min, z_min.
# In this example, the origin is the lower bound of the computation grid.
solver.velocity.min_coords = 0, 0, 0
# Set the interval between nodes of the computational grid.
# For Cartesian coordinates this is dx, dy, dz.
# In this example the nodes are separated by 1 km in in each direction.
solver.velocity.node_intervals = 5, 5, 3
# Set the number of nodes in the computational grid.
# For Cartesian coordinates this is nx, ny, nz.
# This is a 2D example, so we only want one node in the z direction.
solver.velocity.npts = 8, 8, 3
# Set the velocity model.
# In this case the velocity is equale to 1 km/s everywhere.
vg = np.ones(solver.velocity.npts)
vg[:,:,0] = 4.0
vg[:,:,1] = 5.0
vg[:,:,2] = 6.0
solver.velocity.values = vg

# Initialize the source. This is the trickiest part of the example.
# The source coincides with the node at index (0, 0, 0)
src_idx = 4, 4, 2
# Set the traveltime at the source node to 0.
solver.traveltime.values[src_idx] = 0
# Set the unknown flag for the source node to False.
# This is an FMM state variable indicating which values are completely
# unknown. Setting it to False indicates that the node has a tentative value
# assigned to it. In this case, the tentative value happens to be the true,
# final value.
solver.unknown[src_idx] = False
# Push the index of the source node onto the narrow-band heap.
solver.trial.push(*src_idx)

# Solve the system.
solver.solve()

ax1 = plt.subplot(211)
im = ax1.imshow(vg[4,:,:].T, cmap="jet", origin="upper")
plt.colorbar(im)

ax0 = plt.subplot(212, sharex=ax1)
im = ax0.imshow(solver.traveltime.values[:,:,2], cmap="jet", origin="lower")
plt.colorbar(im)

plt.show()
