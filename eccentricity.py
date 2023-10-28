import open3d as o3d
import pymeshlab as pml
import numpy as np
import os
import csv


"""
compute the eccentricity of a single mesh
ratio of largest to smallest eigenvalues of covariance matrix
"""
def eccentricity(mesh):
	#calculate eigenvalues, eigenvectors
    vertices = np.asarray(mesh.vertices)
    cov = np.cov(vertices.transpose())
    eigenvalues, eigenvectors = np.linalg.eig(cov)

    #sort eigenvalues
    sorted_index = np.argsort(-eigenvalues)
    eigenvalues = eigenvalues[sorted_index]

    eccentricity = eigenvalues[0] / eigenvalues[2]
    return eccentricity

"""
mesh_path = 'database_normalized/Guitar/D00374.obj'
mesh = o3d.io.read_triangle_mesh(mesh_path)
mesh.compute_vertex_normals()

eccentricity = eccentricity(mesh)
print(eccentricity)
o3d.visualization.draw_geometries([mesh], width=1280, height=720, mesh_show_wireframe=True)
"""

"""
cauculate D4 for all meshes as feature vectors
store in a .csv file
"""
def compute_feature_vector(path):
	csv_file = []
	csv_file.append(["file_path", "file_class", "file_name", "eccentricity"])
	for root, dirs, files in os.walk(path):
		for name in files:
			if name.endswith('.obj'):
				file_path = os.path.join(root, name)
				mesh = o3d.io.read_triangle_mesh(file_path)
				mesh.compute_vertex_normals()
				eccentricity_result = eccentricity(mesh)

				csv_file.append([file_path, root.split("\\")[1], name, eccentricity_result])

				print("The calculation of ", root.split("\\")[1] + ' ' + name, " done!")

	with open('eccentricity.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(csv_file)


path = 'database_normalized'
compute_feature_vector(path)