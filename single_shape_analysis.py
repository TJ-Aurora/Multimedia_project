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
	surface_area = mesh.get_surface_area()

	return num_vertices, num_triangles, surface_area





"""
file = 'ShapeDatabase_INFOMR-master/Car/D00168.obj'
mesh = read_mesh(file)
num_vertices, num_triangles, surface_area = single_shape_analysis(mesh)
#print(mesh)
print("The amount of vertices in this shape is", num_vertices)
print("The amount of triangles in this shape is", num_triangles)
print("The class of this shape is", file.split("/")[1])
print("The surface area is ", surface_area)
visualize_mesh(mesh, vis_option = "wireframe_on_shaded")
"""


