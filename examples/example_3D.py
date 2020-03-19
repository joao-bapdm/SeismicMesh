import meshio

import SeismicMesh


def example_3D():
    # Name of SEG-Y file containg velocity model.
    fname = "velocity_models/EGAGE_Salt.bin"
    bbox = (-4.2e3, 0, 0, 13520e3, 0, 13520e3)
    # Construct mesh sizing object from velocity model
    ef = SeismicMesh.MeshSizeFunction(
        bbox=bbox,
        model=fname,
        nx=676,
        ny=676,
        nz=210,
        dt=0.001,
        freq=5,
        wl=5,
        hmin=50.0,
    )

    # Build mesh size function
    ef = ef.build()

    # Construct mesh generator
    mshgen = SeismicMesh.MeshGenerator(ef)

    # Build the mesh
    points, facets = mshgen.build(max_iter=50, nscreen=1)

    # Write to disk (see meshio for more details)
    meshio.write_points_cells(
        "foo3D.vtk", points, [("triangle", facets)],
    )


if __name__ == "__main__":

    example_3D()