import open3d as o3d
import pymeshlab as pml
import numpy as np


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

    eccentricity = eigenvalues[0] / eigenvalues[1]
    return eccentricity

"""
mesh_path = 'database_normalized/Hat/m1635.obj'
mesh = o3d.io.read_triangle_mesh(mesh_path)
mesh.compute_vertex_normals()

eccentricity(mesh)
o3d.visualization.draw_geometries([mesh], width=1280, height=720, mesh_show_wireframe=True)
"""
