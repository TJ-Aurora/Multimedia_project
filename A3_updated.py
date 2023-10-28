import open3d as o3d
import pymeshlab as pml
import numpy as np
import math
import time
import random
import matplotlib.pyplot as plt
import os

SAMPLE_AMOUNT = 1000000

def random_choice(array, vertices_amount):
	#array = np.random.choice(a = vertices_index, size = 3, replace = False)
	choiced_vertices = random.sample(range(0, vertices_amount), 3)
	return np.asarray(choiced_vertices)

"""
calculate A3 for all samples at once
"""
def A3(mesh, sample_amount):
	vertices = np.asarray(mesh.vertices)
	vertices_amount = vertices.shape[0]
	vertices_index = np.arange(vertices_amount)

	sampled_vertices = np.zeros([sample_amount, 3])
	sampled_vertices = np.apply_along_axis(random_choice, 1, sampled_vertices, vertices_amount)
	angles = compute_angles(vertices, sampled_vertices)
	return angles


"""
Input: an n*3 array with n angles need to be computed
Return: an n*1 array with all computed angles
"""
def compute_angles(vertices, selected_vertices):
	#compute coordinates and vectors of angles
	#Note: all vectors instead of scalars
	V1 = vertices[selected_vertices[:, 0]]
	V2 = vertices[selected_vertices[:, 1]]
	V3 = vertices[selected_vertices[:, 2]]

	vector_1 = np.subtract(V2, V1)
	vector_2 = np.subtract(V3, V1)
	
	norm_1 = np.linalg.norm(vector_1, axis = 1)
	norm_2 = np.linalg.norm(vector_2, axis = 1)
	"""
	norm_1_has_zero = np.any(norm_1 == 0)
	print(norm_1_has_zero)
	"""
	norm_1_zero_index = np.where(norm_1 == 0)
	"""
	norm_2_has_zero = np.any(norm_2 == 0)
	print(norm_2_has_zero)
	"""
	norm_2_zero_index = np.where(norm_2 == 0)
	#print(norm_2_zero_index)

	angles = np.sum(np.multiply(vector_1, vector_2), axis = 1) / np.multiply(norm_1, norm_2)
	return angles


"""
function to display the distribution over a class of shapes
"""
def A3_distributions(path):
	for root, dirs, files in os.walk(path):
		for name in files:
			try: 
				mesh = o3d.io.read_triangle_mesh(os.path.join(root, name))
				mesh.compute_vertex_normals()
				angles = A3(mesh, SAMPLE_AMOUNT)
				
				hist, edges= np.histogram(angles, bins = 20)
				hist = hist / np.sum(hist)
				edges = edges[0:-1]
				
				plt.plot(edges, hist, color = [np.random.uniform(), np.random.uniform(), np.random.uniform()])
				print("The plot of ", name, " done!")
			except ValueError:
				continue
	plt.show()

	


start_time = time.time()
mesh_path = 'database_normalized/Gun/D00103.obj'
mesh = o3d.io.read_triangle_mesh(mesh_path)
mesh.compute_vertex_normals()
angles = A3(mesh, SAMPLE_AMOUNT)
print("--- %s seconds ---" % (time.time() - start_time))



"""
mesh_path = 'database_normalized/Chess'
A3_distributions(mesh_path)
"""


