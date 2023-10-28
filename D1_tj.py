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


"""
calculate D1 for all samples at once
"""
def D1(mesh, sample_amount):
	barycenter = np.asarray(mesh.get_center())
	vertices = np.asarray(mesh.vertices)
	vertices_amount = vertices.shape[0]
	selected_vertices_index = random.choices(range(0, vertices_amount), k = sample_amount)

	selected_vertices_index = np.asarray(selected_vertices_index)

	selected_vertices = vertices[selected_vertices_index]
	distances = np.sqrt(np.sum(np.square(np.subtract(barycenter, selected_vertices)), axis = 1))

	return distances



"""
function to display the distribution over a class of shapes
"""
def D1_distributions(path):
	for root, dirs, files in os.walk(path):
		for name in files:
			mesh = o3d.io.read_triangle_mesh(os.path.join(root, name))
			mesh.compute_vertex_normals()
			distances = D1(mesh, SAMPLE_AMOUNT)
			
			hist, edges= np.histogram(distances, bins = 20)
			hist = hist / np.sum(hist)
			edges = edges[0:-1]
			
			plt.plot(edges, hist, color = [np.random.uniform(), np.random.uniform(), np.random.uniform()])
			print("The plot of ", name, " done!")
	plt.show()

"""
cauculate D1 for all meshes as feature vectors
store in a .csv file
"""
def compute_feature_vector(path, bins_amount, sample_amount):
	csv_file = []
	csv_file.append(["file_path", "file_class", "file_name", "D1"])
	for root, dirs, files in os.walk(path):
		for name in files:
			if name.endswith('.obj'):
				file_path = os.path.join(root, name)
				mesh = o3d.io.read_triangle_mesh(file_path)
				mesh.compute_vertex_normals()
				distances = D1(mesh, sample_amount)
				
				hist, _= np.histogram(distances, bins = 20)
				hist = hist / np.sum(hist)

				csv_file.append([file_path, root.split("\\")[1], name, hist])

				print("The vector of ", root.split("\\")[1] + ' ' + name, " done!")

	with open('D1.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(csv_file)


"""
start_time = time.time()
mesh_path = 'database_normalized/Guitar/D00023.obj'
mesh = o3d.io.read_triangle_mesh(mesh_path)
mesh.compute_vertex_normals()
D1(mesh, SAMPLE_AMOUNT)
print("--- %s seconds ---" % (time.time() - start_time))
"""


path = 'database_normalized'
compute_feature_vector(path, bins_amount = 20, sample_amount = 1000000)

