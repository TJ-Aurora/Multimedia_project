"""
calculate some statistics of a single mesh
"""

import open3d as o3d
import numpy as np

from read_data import read_mesh, visualize_mesh

"""
input: mesh subject already read from file
"""
def single_shape_analysis(mesh):

	num_vertices = np.asarray(mesh.vertices).shape[0]
	num_triangles = np.asarray(mesh.triangles).shape[0]

	return num_vertices, num_triangles





"""
file = 'ShapeDatabase_INFOMR-master/Car/D00168.obj'
mesh = read_mesh(file)
num_vertices, num_triangles = single_shape_analysis(mesh)
#print(mesh)
print("The amount of vertices in this shape is", num_vertices)
print("The amount of triangles in this shape is", num_triangles)
print("The class of this shape is", file.split("/")[1])
visualize_mesh(mesh, vis_option = "wireframe_on_shaded")
"""

