import open3d as o3d
import pymeshlab as pml
import numpy as np
import time
import os


from read_data import read_mesh, visualize_mesh

path = "ShapeDatabase_INFOMR-master"


"""
experiment on the settings of remesh
current optimal solution: teaget length 0.04, iter 5
should not run this when remesh whole dataset
"""
def remesh_setting_experiment():
	lowpoly_path = "D01121.obj"
	highpoly_path = "D00166.obj"
	target_edge_length = 0.04
	iter_low = 2
	iter_high = 5

	do_remeshing = True   # Turn off if you don't want to do the remeshing on the fly.
					   # Useful for viewing meshes you've already remeshed.
	start_time = time.time()

	# Remeshing
	if do_remeshing:

		# --- REFINEMENT --- #
		# Load a low-poly input mesh using PyMeshLab
		mesh_lowpoly = pml.MeshSet()
		mesh_lowpoly.load_new_mesh(lowpoly_path)

		# Create refined (i.e. high-poly) versions of it
		print(f"Refining lowpoly mesh ({iter_low} iterations)... ", end="")
		mesh_lowpoly.meshing_isotropic_explicit_remeshing(
			targetlen=pml.AbsoluteValue(target_edge_length), iterations=iter_low)
		mesh_lowpoly.save_current_mesh(f"refined_iter{iter_low}.obj")
		print("Finished.")

		mesh_lowpoly = pml.MeshSet()
		mesh_lowpoly.load_new_mesh(lowpoly_path)

		print(f"Refining lowpoly mesh ({iter_high} iterations)... ", end="")
		mesh_lowpoly.meshing_isotropic_explicit_remeshing(
			targetlen=pml.AbsoluteValue(target_edge_length), iterations=iter_high)
		mesh_lowpoly.save_current_mesh(f"refined_iter{iter_high}.obj")
		print("Finished.")


		# --- DECIMATION --- #
		# Load a high-poly input mesh
		mesh_highpoly = pml.MeshSet()
		mesh_highpoly.load_new_mesh(highpoly_path)

		# Create decimated (i.e. low-poly) versions of it
		print(f"Decimating highpoly mesh... ", end="")
		mesh_highpoly.meshing_decimation_quadric_edge_collapse(
			targetperc = 0.3)
		mesh_highpoly.save_current_mesh(f"decimated.obj")
		print("Finished.")


	original_low_mesh = read_mesh(lowpoly_path)
	low_mesh_iter_low = read_mesh(f'refined_iter{iter_low}.obj')
	low_mesh_iter_high = read_mesh(f'refined_iter{iter_high}.obj')

	original_high_mesh = read_mesh(highpoly_path)
	decimated_high_mesh = read_mesh(f'decimated.obj')



	print("Number of vertices in original lowpoly mesh:",
	  np.asarray(original_low_mesh.vertices).shape[0])
	print(f"Number of vertices in refined version of lowpoly mesh ({iter_low} iterations):",
	  np.asarray(low_mesh_iter_low.vertices).shape[0])
	print(f"Number of vertices in refined version of lowpoly mesh ({iter_high} iterations):",
	  np.asarray(low_mesh_iter_high.vertices).shape[0])

	print("Number of vertices in original highpoly mesh:",
	  np.asarray(original_high_mesh.vertices).shape[0])
	print(f"Number of vertices in decimated version of highpoly mesh:",
	  np.asarray(decimated_high_mesh.vertices).shape[0])

	print("--- %s seconds ---" % (time.time() - start_time))


	# Position the meshes in a 2x3 grid
	translation_vector = np.array([1.2, 0, 0])
	low_mesh_iter_low.translate(translation_vector)
	translation_vector = np.array([2.4, 0, 0])
	low_mesh_iter_high.translate(translation_vector)

	translation_vector = np.array([0, -1, 0])
	original_high_mesh.translate(translation_vector)
	translation_vector = np.array([2, -1, 0])
	decimated_high_mesh.translate(translation_vector)


	# Visualize the meshes
	o3d.visualization.draw_geometries(
	[
		original_low_mesh, low_mesh_iter_low, low_mesh_iter_high, original_high_mesh, decimated_high_mesh],
	width=1280,
	height=720,
	mesh_show_wireframe=True
	)

	"""
	check the resulted edge length
	reference: https://pymeshlab.readthedocs.io/en/latest/tutorials/apply_filter_output.html?highlight=edge%20length#apply-filter-output
	"""

	ms = pml.MeshSet()
	ms.load_new_mesh(lowpoly_path)
	out_dict = ms.get_geometric_measures()
	avg_edge_length = out_dict['avg_edge_length']
	print("Edge Lengths of original low mesh:", avg_edge_length)

	ms.load_new_mesh(f'refined_iter{iter_low}.obj')
	out_dict = ms.get_geometric_measures()
	avg_edge_length = out_dict['avg_edge_length']
	print(f"Edge Lengths of refined_iter{iter_low}.obj", avg_edge_length)

	ms.load_new_mesh(f'refined_iter{iter_high}.obj')
	out_dict = ms.get_geometric_measures()
	avg_edge_length = out_dict['avg_edge_length']
	print(f"Edge Lengths of refined_iter{iter_high}.obj", avg_edge_length)


	ms.load_new_mesh(highpoly_path)
	out_dict = ms.get_geometric_measures()
	avg_edge_length = out_dict['avg_edge_length']
	print("Edge Lengths of original high mesh:", avg_edge_length)

	ms.load_new_mesh(f'decimated.obj')
	out_dict = ms.get_geometric_measures()
	avg_edge_length = out_dict['avg_edge_length']
	print(f"Edge Lengths of decimated.obj", avg_edge_length)


def remesh_single_shape(remesh_type, file_path, target_edge_length, iterations, target_percentage):
	mesh_set = pml.MeshSet()
	mesh_set.load_new_mesh(file_path)

	if remesh_type == "REFINEMENT":

		print(f"Remesh mesh {file_path} ({iterations} iterations)... ", end="")
		mesh_set.meshing_isotropic_explicit_remeshing(targetlen=pml.AbsoluteValue(target_edge_length), iterations=iterations)
		mesh_set.save_current_mesh(f"{file_path}")
		print("Finished.")

	if remesh_type == "DECIMATION":
		print(f"Decimating highpoly mesh {file_path}... ", end="")
		mesh_set.meshing_decimation_quadric_edge_collapse(
			targetperc = target_percentage)
		mesh_set.save_current_mesh(f"{file_path}")
		print("Finished.")


def dataset_remesh(path, outliers_above_csv, outliers_below_csv, floor, ceiling):
	#get the list of outliers names
	whole_data = np.loadtxt(outliers_above_csv, delimiter=',', dtype=str)
	outliers_above = whole_data[1:, 1:]
	outliers_above_names = outliers_above[:, 2].tolist()

	whole_data = np.loadtxt(outliers_below_csv, delimiter=',', dtype=str)
	outliers_below = whole_data[1:, 1:]
	outliers_below_names = outliers_below[:, 2].tolist()


	for root, dirs, files in os.walk(path):
		for name in files:
			#original parameters of remesh
			target_edge_length = 0.06
			iterations = 5
			target_percentage = 0.5

			if name.endswith('.obj') and name in outliers_below_names:
				remesh_type = 'REFINEMENT'

			elif name.endswith('.obj') and name in outliers_above_names:
				remesh_type = 'DECIMATION'

			if not name.endswith('.obj'):
				continue

			#first time remesh
			file_path = os.path.join(root, name)
			remesh_single_shape(remesh_type, file_path, target_edge_length, iterations, target_percentage)

			remesh_time = 1
			keep_remesh = True
			while keep_remesh:
				#check the result of the previous remesh
				mesh = o3d.io.read_triangle_mesh(file_path)
				mesh.compute_vertex_normals()
				num_vertices = np.asarray(mesh.vertices).shape[0]

				if remesh_time > 5:
					print("Still not optimal after 5 times of remesh, abandon")
					keep_remesh = False
					break

				#do remesh again if not satisfied our requirement
				if num_vertices < floor:
					remesh_type = 'REFINEMENT'
					target_edge_length -= 0.01
					print("Too few vertices, remesh again with REFINEMENT")
					remesh_single_shape(remesh_type, file_path, target_edge_length, iterations, target_percentage)
					remesh_time += 1

				elif num_vertices > ceiling:
					remesh_type = 'DECIMATION'
					target_percentage -= 0.05
					print("Too many vertices, remesh again with DECIMATION")
					remesh_single_shape(remesh_type, file_path, target_edge_length, iterations, target_percentage)
					remesh_time += 1

				else:
					keep_remesh = False



dataset_remesh(path, 'vertex_outliers_above.csv', 'vertex_outliers_under.csv', floor = 627, ceiling = 4855)
#remesh_setting_experiment()