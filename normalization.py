import open3d as o3d
import pymeshlab as pml
import numpy as np
from copy import deepcopy

from read_data import read_mesh


"""
make a mesh centered at the origin of the coordinate frame
"""
def translation(mesh):
    #get axes and center
    world_axes = o3d.geometry.TriangleMesh.create_coordinate_frame()
    world_center = world_axes.get_center()

    #translate to the origin
    mesh_translated = deepcopy(mesh).translate(np.negative(world_center))
    #o3d.visualization.draw_geometries([world_axes, mesh, mesh_translated])

    return mesh_translated


def PCA(mesh):
    vertices = np.asarray(mesh.vertices)
    cov = np.cov(vertices.transpose())
    eigenvalues, eigenvectors = np.linalg.eig(cov)

    #sort eigenvalues, the sequence of eigenvectors should follow their corresponse eigenvalues
    sorted_index = np.argsort(-eigenvalues)
    eigenvalues = eigenvalues[sorted_index]
    eigenvectors = eigenvectors[sorted_index]

    return eigenvalues, eigenvectors

"""
align a shape’s eigenvectors with the xyz coordinate frame
"""

def alignment(mesh, eigenvectors):
    vertices = np.asarray(mesh.vertices)

    #do projection in each axis
    x_updated = np.dot(vertices, eigenvectors[0])
    x_updated = np.resize(x_updated, (vertices.shape[0], 1))

    y_updated = np.dot(vertices, eigenvectors[1])
    y_updated = np.resize(y_updated, (vertices.shape[0], 1))

    z_updated = np.dot(vertices, np.cross(eigenvectors[0], eigenvectors[1]))
    z_updated = np.resize(z_updated, (vertices.shape[0], 1))

    vertices_updated = np.concatenate((x_updated, y_updated, z_updated), axis = 1)

    #update the vertices coordinates
    aligned_mesh = deepcopy(mesh)
    aligned_mesh.vertices = o3d.utility.Vector3dVector(vertices_updated)

    return aligned_mesh

"""
fix the issue that PCA alignment cannot distinguished between flipped (mirrored) shapes
"""
def orientation(mesh):
    vertices = np.asarray(mesh.vertices)
    triangles = np.asarray(mesh.triangles)

    #calculate coordinates of center of each triangle
    triangle_centers = np.zeros((triangles.shape[0], triangles.shape[1]))
    for i in range(triangles.shape[0]):

        #get coordinate of 3 vertices of this triangle
        v1 = np.resize(vertices[triangles[i][0]], (3, 1))
        v2 = np.resize(vertices[triangles[i][1]], (3, 1))
        v3 = np.resize(vertices[triangles[i][2]], (3, 1))
        vertices_array = np.concatenate((v1, v2, v3), axis = 1)
        triangle_center = np.mean(vertices_array, axis = 0)
        triangle_centers[i] = triangle_center

    #compute f0, f1, f2
    x_coordinate = triangle_centers[:, 0]
    f0 = np.sum(np.multiply(np.sign(x_coordinate), np.power(x_coordinate, 2)))
    
    y_coordinate = triangle_centers[:, 1]
    f1 = np.sum(np.multiply(np.sign(y_coordinate), np.power(y_coordinate, 2)))

    z_coordinate = triangle_centers[:, 2]
    f2 = np.sum(np.multiply(np.sign(z_coordinate), np.power(z_coordinate, 2)))

    F = np.array([[np.sign(f0), 0, 0], [0, np.sign(f1), 0], [0, 0, np.sign(f2)]])
    
    updated_vertices = np.dot(vertices, F)

    #update the vertices coordinates
    orientated_mesh = deepcopy(mesh)
    orientated_mesh.vertices = o3d.utility.Vector3dVector(updated_vertices)

    return orientated_mesh

"""
rescale the size of shape
"""
def rescale(mesh):
    vertices = np.asarray(mesh.vertices)
    obb = mesh.get_oriented_bounding_box()

    #x, y, z size of the oriented bounding box that encloses the shape
    obb_size = obb.extent

    d_max = np.max(obb_size)
    scaling_factor = 1/d_max

    updated_vertices = np.multiply(vertices, scaling_factor)
    #update the vertices coordinates
    rescaled_mesh = deepcopy(mesh)
    rescaled_mesh.vertices = o3d.utility.Vector3dVector(updated_vertices)

    """
    #test code for rescale, you can see bound box from here
    obb_points = obb.get_box_points()
    obb_line_indices = [[0, 1], [1, 6], [6, 3], [3, 0], [0, 2], [2, 5], [5, 4], [4, 7], [7, 2], [6, 4], [1, 7], [3, 5]]
    obb_lineset = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(obb_points),
        lines=o3d.utility.Vector2iVector(obb_line_indices),
    )
    blue = [0, 0, 255]
    obb_lineset.colors = o3d.utility.Vector3dVector(np.array([blue] * 12))

    # Visualize the geometry
    to_draw = [rescaled_mesh]
    to_draw.append(obb_lineset)
    o3d.visualization.draw_geometries(
        to_draw,
        width=1280,
        height=720,
        mesh_show_wireframe=True
    )
    """

    return rescaled_mesh


#TEST CODE: use your own file path here
mesh = read_mesh("D00696.obj")
triangles = np.asarray(mesh.triangles)
mesh_translated = translation(mesh)
eigenvalues, eigenvectors = PCA(mesh_translated)
aligned_mesh = alignment(mesh_translated, eigenvectors)
orientated_mesh = orientation(aligned_mesh)
rescaled_mesh = rescale(orientated_mesh)


world_axes = o3d.geometry.TriangleMesh.create_coordinate_frame()
o3d.visualization.draw_geometries([world_axes, rescaled_mesh], mesh_show_wireframe=True)

