import open3d as o3d
import pymeshlab as pml
import numpy as np
import math
import time
import random
import matplotlib.pyplot as plt
import os
import csv

SAMPLE_AMOUNT = 1000000

def random_choice(array, vertices_amount):
	#array = np.random.choice(a = vertices_index, size = 3, replace = False)
	choiced_vertices = random.sample(range(0, vertices_amount), 3)
	return np.asarray(choiced_vertices)

"""
calculate D3 for all samples at once
"""
def D3(mesh, sample_amount):
	vertices = np.asarray(mesh.vertices)
	vertices_amount = vertices.shape[0]
	vertices_index = np.arange(vertices_amount)

	sampled_vertices = np.zeros([sample_amount, 3])
	sampled_vertices = np.apply_along_axis(random_choice, 1, sampled_vertices, vertices_amount)
	
	#3 vertices
	V1 = vertices[sampled_vertices[:, 0]]
	V2 = vertices[sampled_vertices[:, 1]]
	V3 = vertices[sampled_vertices[:, 2]]

	#2 vectors
	vector_1 = V2 - V1
	vector_2 = V3 - V1

	areas = np.sqrt(0.5 * np.linalg.norm(np.cross(vector_1, vector_2, axis = 1), axis = 1))
	
	return areas

"""
function to display the distribution over a class of shapes
"""
def D3_distributions(path):
	for root, dirs, files in os.walk(path):
		for name in files:
			try: 
				mesh = o3d.io.read_triangle_mesh(os.path.join(root, name))
				mesh.compute_vertex_normals()
				areas = D3(mesh, SAMPLE_AMOUNT)
				
				hist, edges= np.histogram(areas, bins = 20)
				hist = hist / np.sum(hist)
				edges = edges[0:-1]
				
				plt.plot(edges, hist, color = [np.random.uniform(), np.random.uniform(), np.random.uniform()])
				print("The plot of ", name, " done!")
			except ValueError:
				continue
	plt.show()

"""
cauculate D3 for all meshes as feature vectors
store in a .csv file
"""
def compute_feature_vector(path, bins_amount, sample_amount):
	csv_file = []
	csv_file.append(["file_path", "file_class", "file_name", "D3"])
	for root, dirs, files in os.walk(path):
		for name in files:
			if name.endswith('.obj'):
				file_path = os.path.join(root, name)
				mesh = o3d.io.read_triangle_mesh(file_path)
				mesh.compute_vertex_normals()
				areas = D3(mesh, sample_amount)
				
				hist, _= np.histogram(areas, bins = 20)
				hist = hist / np.sum(hist)

				csv_file.append([file_path, root.split("\\")[1], name, hist])

				print("The vector of ", root.split("\\")[1] + ' ' + name, " done!")

	with open('D3.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(csv_file)

"""
start_time = time.time()
mesh_path = 'database_normalized/Car/D00265.obj'
mesh = o3d.io.read_triangle_mesh(mesh_path)
mesh.compute_vertex_normals()
areas = D3(mesh, SAMPLE_AMOUNT)
print("--- %s seconds ---" % (time.time() - start_time))
"""

path = 'database_normalized'
compute_feature_vector(path, bins_amount = 20, sample_amount = 1000000)
#D3_distributions(path)