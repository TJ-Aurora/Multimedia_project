import open3d as o3d
import pymeshlab as pml
import numpy as np
import math
import time
import random
import matplotlib.pyplot as plt
import os
import csv

SAMPLE_AMOUNT = 100000

def A3(mesh, sample_amount):
	#randomly select vertices
	vertices = np.asarray(mesh.vertices)
	vertices_amount = vertices.shape[0]

	#compute angles
	angles = []
	i = 0

	while i < sample_amount:
		try:
			v1_index = random.randint(0, vertices_amount-1)
			v2_index = random.randint(0, vertices_amount-1)
			if np.array_equal(vertices[v1_index], vertices[v2_index]):
				continue
			v3_index = random.randint(0, vertices_amount-1)
			if np.array_equal(vertices[v2_index], vertices[v3_index]) or np.array_equal(vertices[v1_index], vertices[v3_index]):
				continue
			angle = compute_angle(vertices[v1_index], vertices[v2_index], vertices[v3_index])
			angles.append(angle)
			i += 1
		except ValueError:
			print("There is a value error")
			continue

	return np.asarray(angles)

	

"""
compute the angle among 3 given vertices
v1 as head, v2, v3 as tails
"""
def compute_angle(v1, v2, v3):
	vector_1 = v2 - v1
	vector_2 = v3 - v1

	norm_1 = np.linalg.norm(vector_1)
	norm_2 = np.linalg.norm(vector_2)

	cosine = np.dot(vector_1, vector_2) / (norm_1 * norm_2)
	angle = math.acos(cosine) #result in rads, not degrees

	return angle

"""
function to display the distribution over a class of shapes
for comparision among different classes
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
				print("There is a value error")
				continue
	plt.show()

"""
cauculate A3 for all meshes as feature vectors
store in a .csv file
"""
def compute_feature_vector(path, bins_amount, sample_amount):
	csv_file = []
	csv_file.append(["file_path", "file_class", "file_name", "A3"])
	for root, dirs, files in os.walk(path):
		for name in files:
			if name.endswith('.obj'):
				file_path = os.path.join(root, name)
				mesh = o3d.io.read_triangle_mesh(file_path)
				mesh.compute_vertex_normals()
				angles = A3(mesh, sample_amount)
				
				hist, _= np.histogram(angles, bins = 20)
				hist = hist / np.sum(hist)

				csv_file.append([file_path, root.split("\\")[1], name, hist])

				print("The plot of ", root.split("\\")[1] + ' ' + name, " done!")

	with open('A3.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(csv_file)


"""
start_time = time.time()
mesh_path = 'database_normalized/Chess/m1593.obj'
mesh = o3d.io.read_triangle_mesh(mesh_path)
mesh.compute_vertex_normals()
A3(mesh, SAMPLE_AMOUNT)
print("--- %s seconds ---" % (time.time() - start_time))
"""


mesh_path = 'database_normalized'
compute_feature_vector(mesh_path, bins_amount = 20, sample_amount = 100000)

