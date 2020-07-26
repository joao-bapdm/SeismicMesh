import meshio
from mpi4py import MPI

import SeismicMesh

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Serial or parallel 3d mesh generation building a mesh roughly 1.6 million cells.
# Warning: In serial, this example takes roughly 20 minutes...


def example_3D():

    # Name of SEG-Y file containg velocity model.
    fname = "velocity_models/EGAGE_Salt.bin"
    # Bounding box describing domain extents (corner coordinates)
    bbox = (-4200, 0, 0, 13520, 0, 13520)

    # Construct mesh sizing object from velocity model
    ef = SeismicMesh.MeshSizeFunction(
        bbox=bbox,
        model=fname,
        nx=676,  # size of velocity model in x-direction
        ny=676,  # size of velocity model in y-direction
        nz=210,  # size of velocity model in z-direction
        dt=0.001,
        freq=2,
        wl=5,
        grade=0.25,
        hmin=100,
        hmax=5e3,
        domain_ext=250,
        padstyle="linear_ramp",
    )

    # Build mesh size function (in parallel)
    ef = ef.build()

    # Write to disk for later use
    ef.WriteVelocityModel("EGAGE_Salt")

    # Construct a mesh generator object
    mshgen = SeismicMesh.MeshGenerator(ef)

    # Build the mesh
    points, cells = mshgen.build(max_iter=75, axis=1)

    # Do mesh improvement in serial to bound lower dihedral angle to >= 5 degrees
    points, cells = mshgen.build(
        points=points, mesh_improvement=True, max_iter=50, min_dh_bound=5,
    )

    if rank == 0:
        # Write to disk (see meshio package for more details)
        meshio.write_points_cells(
            "EGAGE_Salt.vtk", points / 1000.0, [("tetra", cells)],
        )
        # Write to gmsh22 format (quite slow)
        meshio.write_points_cells(
            "EGAGE_Salt.msh",
            points / 1000,
            [("tetra", cells)],
            file_format="gmsh22",
            binary=False,
        )


if __name__ == "__main__":

    example_3D()
