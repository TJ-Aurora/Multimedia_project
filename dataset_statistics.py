import open3d as o3d
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd

from read_data import read_mesh
from single_shape_analysis import single_shape_analysis

path = "ShapeDatabase_INFOMR-master"


"""
Read all meshes in a database
Store their information (file name, class, vertex amount, faces amount) in a csv file
"""
def read_all_meshes(path):

	class_amount = 0
	row_list = []
	row_list.append(["file_path", "file_class", "file_name", "num_of_vertices", "num_of_triangles"])

	for root, dirs, files in os.walk(path):
		class_amount += len(dirs)
		for name in files:
			if name.endswith('.obj'):
				file_path = os.path.join(root, name)
				mesh = read_mesh(file_path)
				num_vertices, num_triangles = single_shape_analysis(mesh)
				row_list.append([file_path, root.split("\\")[1], name, num_vertices, num_triangles])

	print("The amount of class is", class_amount)

	#the file name is dataset_statistics.csv for original dataset, dataset_statistics_remeshed.csv for remeshed dataset
	with open('dataset_statistics_remeshed.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(row_list)


"""
show some basic distributions of database
given the csv file
"""
def distribute_dataset(csv_file, first_percentile, second_percentile):
	whole_data = np.loadtxt(csv_file, delimiter=',', dtype=str)
	data = whole_data[1:, :]


	#compute the average, min and max vertices and faces
	ave_vertices = np.mean(data[:, 3].astype(np.float64))
	ave_faces = np.mean(data[:, 4].astype(np.float64))
	print("The average vertices in whole database is", ave_vertices)
	print("The average faces in whole database is", ave_faces)

	median_vertices = np.median(data[:, 3].astype(np.float64))
	median_faces = np.median(data[:, 4].astype(np.float64))
	print("The median vertices in whole database is", median_vertices)
	print("The median faces in whole database is", median_faces)

	std_vertices = np.std(data[:, 3].astype(np.float64))
	std_faces = np.std(data[:, 4].astype(np.float64))
	print("The vertices std in whole database is", std_vertices)
	print("The faces std in whole database is", std_faces)

	max_vertices_index = np.argmax(data[:, 3].astype(np.float64))
	print("max vertices amount is: ", np.max(data[:, 3].astype(np.float64)), 
		"with class", data[:, 1][max_vertices_index], "and name", data[:, 2][max_vertices_index])
	print("max faces amount is: ", np.max(data[:, 4].astype(np.float64)))

	min_vertices_index = np.argmin(data[:, 3].astype(np.float64))
	print("min vertices amount is: ", np.min(data[:, 3].astype(np.float64)), 
		"with class", data[:, 1][min_vertices_index], "and name", data[:, 2][min_vertices_index])
	print("min faces amount is: ", np.min(data[:, 4].astype(np.float64)))

	#percentiles for amount of vertices
	percentile1 = np.percentile(data[:, 3].astype(np.float64), first_percentile)
	percentile2 = np.percentile(data[:, 3].astype(np.float64), second_percentile)
	print(f"The {first_percentile} percentile is: ", percentile1)
	print(f"The {second_percentile} percentile is: ", percentile2)



	#show distribution over vertices, faces, classes
	#change the range for the specific distribution you need
	_, _, bars = plt.hist(data[:, 3].astype(np.float64), bins = np.arange(0, 2000, step=200))
	plt.title('distribution of number of vertices')
	plt.bar_label(bars)

	values = np.arange(0, 2000, 200)
	plt.xticks(values)

	plt.show()

	_, _, bars = plt.hist(data[:, 4].astype(np.float64), bins = np.arange(0, 2000, step=200))
	plt.title('distribution of number of faces')
	plt.bar_label(bars)
	
	values = np.arange(0, 2000, 200)
	plt.xticks(values)
	

	plt.show()

	_, _, bars = plt.hist(data[:, 1])
	plt.title('distribution of classes')
	plt.show()

	return percentile1, percentile2



"""
check the outliers in the dataset (from csv file)
store the information of outliers in csv files
"""

def check_outliers(csv_file, target_min_vertices, target_max_vertices):
	whole_data = np.loadtxt(csv_file, delimiter=',', dtype=str)
	data = whole_data[1:, :] #numpy array without header

	#find outliers with too less or too many vertices
	vertex_outliers_under = data[np.where(data[:, 3].astype(np.float64) < target_min_vertices)]
	print("There are totally ", vertex_outliers_under.shape[0], "meshes with amuont of vertices below requirement.")
	#vertex_outliers_under.tofile('vertex_outliers_under.csv', sep = ' ')
	df = pd.DataFrame(vertex_outliers_under)
	df.to_csv("vertex_outliers_under.csv")

	vertex_outliers_above = data[np.where(data[:, 3].astype(np.float64) > target_max_vertices)]
	print("There are totally ", vertex_outliers_above.shape[0], "meshes with amuont of vertices above requirement.")
	df = pd.DataFrame(vertex_outliers_above)
	df.to_csv("vertex_outliers_above.csv")

	
	#find outliers with too less or too many faces
	#not necessary for now
	"""
	faces_outliers_under = data[np.where(data[:, 4].astype(np.float64) <= 100)]
	print("There are totally ", faces_outliers_under.shape[0], "meshes with less or equal to 100 faces.")
	df = pd.DataFrame(faces_outliers_under)
	df.to_csv("faces_outliers_under.csv")

	faces_outliers_above = data[np.where(data[:, 4].astype(np.float64) >= 50000)]
	print("There are totally ", faces_outliers_above.shape[0], "meshes with more or equal to 50000 faces.")
	df = pd.DataFrame(faces_outliers_above)
	df.to_csv("faces_outliers_above.csv")
	"""



#read_all_meshes(path)

target_min, target_max = distribute_dataset('dataset_statistics_remeshed.csv', 30, 70)
#check_outliers('dataset_statistics.csv', target_min, target_max)

