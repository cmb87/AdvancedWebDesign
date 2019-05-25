import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import json
import pandas as pd


class Cube(object):
    def __init__(self):
        pass

    def createSTL(self):
        # Define the 8 vertices of the cube
        vertices = np.array([
            [-1, -1, -1],
            [+1, -1, -1],
            [+1, +1, -1],
            [-1, +1, -1],
            [-1, -1, +1],
            [+1, -1, +1],
            [+1, +1, +1],
            [-1, +1, +1]])
        # Define the 12 triangles composing the cube
        faces = np.array([
            [0, 3, 1],
            [1, 3, 2],
            [0, 4, 7],
            [0, 7, 3],
            [4, 5, 6],
            [4, 6, 7],
            [5, 1, 2],
            [5, 2, 6],
            [2, 3, 6],
            [3, 7, 6],
            [0, 1, 5],
            [0, 5, 4]])

        # Create the mesh
        cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                cube.vectors[i][j] = vertices[f[j], :]

        # Write the mesh to file "cube.stl"
        cube.save('cube.stl')

    def readSTL(self):
        mystl = mesh.Mesh.from_file('/home/cp/projects/01_sqliteJS/src/models/geometry/Airbus_A319.stl')
        #mystl = mesh.Mesh.from_file('/home/cp/projects/01_sqliteJS/src/models/geometry/cube.stl')

        xmax = max([mystl.x.max(), mystl.y.max(), mystl.z.max()])
        xmin = min([mystl.x.min(), mystl.y.min(), mystl.z.min()])

        mystl.x = 3 * ((mystl.x - mystl.x.min()) / (xmax - xmin) - 0.5)
        mystl.y = 3 * ((mystl.y - mystl.y.min()) / (xmax - xmin) - 0.5)
        mystl.z = 3 * ((mystl.z - mystl.z.min()) / (xmax - xmin) - 0.5)

        xaxis = np.asarray([0, 0, 0, 0, 0, 0.1, 2, 0, 0])
        colorx = np.asarray([1, 0, 0, 1, 0, 0, 1, 0, 0])
        yaxis = np.asarray([0, 0, 0, 0.1, 0, 0, 0, 2, 0])
        colory = np.asarray([1, 0, 0, 1, 0, 0, 1, 0, 0])
        zaxis = np.asarray([0, 0, 0, 0.1, 0, 0, 0, 0, 2])
        colorz = np.asarray([1, 0, 0, 1, 0, 0, 1, 0, 0])

        nvertices = mystl.vectors.shape[0] * mystl.vectors.shape[1] + 3 + 3 + 3
        vertices = mystl.vectors.flatten()
        vertices = np.hstack((vertices, xaxis, yaxis, zaxis))

        def cstm_autumn_r(x):
            return plt.cm.autumn_r((np.clip(x, 2, 10) - 2) / 8.)[:, :3].flatten()

        colors = cstm_autumn_r(np.linspace(2, 10, nvertices))  # np.ones(vertices.shape[0])
        colors = np.hstack((colors, colorx, colory, colorz))

        return pd.Series(vertices).to_json(orient='values'), nvertices, pd.Series(colors).to_json(orient='values')


if __name__ == '__main__':
    cube = Cube()
    # cube.createSTL()
    a, b, c = cube.readSTL()
