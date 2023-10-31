import csv
import numpy as np
import pandas as pd


"""
concatenate all .csv files together
normalize scalar features by standardization
normalize distribution features by dividing by the area
"""

#load and preprocessing surface area and compactness
whole_data = np.loadtxt('SurfaceArea and Compactness.csv', delimiter=',', dtype=str)
file_path = whole_data[1:, 0]
file_class = whole_data[1:, 1]
file_name = whole_data[1:, 2]

Area = whole_data[1:, 3].astype(np.float64)
average_Area = np.average(Area)
std_Area = np.std(Area)
normalized_Area = np.subtract(Area, average_Area) / std_Area

compactness = whole_data[1:, 4].astype(np.float64)
average_compactness = np.average(compactness)
std_compactness = np.std(compactness)
normalized_compactness = np.subtract(compactness, average_compactness) / std_compactness


#load and preprocessing convexity and regularity
whole_data = np.loadtxt('convexity and regularity.csv', delimiter=',', dtype=str)

convexity = whole_data[1:, 3].astype(np.float64)
average_convexity = np.average(convexity)
std_convexity = np.std(convexity)
normalized_convexity = np.subtract(convexity, average_convexity) / std_convexity

regularity = whole_data[1:, 4].astype(np.float64)
average_regularity = np.average(regularity)
std_regularity = np.std(regularity)
normalized_regularity = np.subtract(regularity, average_regularity) / std_regularity


#load and preprocessing diameter
whole_data = np.loadtxt('diameter.csv', delimiter=',', dtype=str)

diameter = whole_data[1:, 3].astype(np.float64)
average_diameter = np.average(diameter)
std_diameter = np.std(diameter)
normalized_diameter = np.subtract(diameter, average_diameter) / std_diameter


#load and preprocessing eccentricity
whole_data = np.loadtxt('eccentricity.csv', delimiter=',', dtype=str)

eccentricity = whole_data[1:, 3].astype(np.float64)
average_eccentricity = np.average(eccentricity)
std_eccentricity = np.std(eccentricity)
normalized_eccentricity = np.subtract(eccentricity, average_eccentricity) / std_eccentricity


#load all distribution features, preprocessing has been done before
df = pd.read_csv('A3.csv', delimiter=',')
whole_data = df.values
A3 = whole_data[:, 3]

df = pd.read_csv('D1.csv', delimiter=',')
whole_data = df.values
D1 = whole_data[:, 3]

df = pd.read_csv('D2.csv', delimiter=',')
whole_data = df.values
D2 = whole_data[:, 3]

df = pd.read_csv('D3.csv', delimiter=',')
whole_data = df.values
D3 = whole_data[:, 3]

df = pd.read_csv('D4.csv', delimiter=',')
whole_data = df.values
D4 = whole_data[:, 3]


#concatenate all features together
row_list = []
row_list.append(["file_path", "file_class", "file_name", "feature_vector"])
for i in range(file_path.shape[0]):
	feature_vector = [normalized_Area[i], normalized_compactness[i], normalized_convexity[i], normalized_regularity[i], normalized_diameter[i], normalized_eccentricity[i]]

	A3[i] = A3[i].strip('[]')
	A3[i] = np.fromstring(A3[i], sep = ' ')
	feature_vector += list(A3[i])

	D1[i] = D1[i].strip('[]')
	D1[i] = np.fromstring(D1[i], sep = ' ')
	feature_vector += list(D1[i])

	D2[i] = D2[i].strip('[]')
	D2[i] = np.fromstring(D2[i], sep = ' ')
	feature_vector += list(D2[i])

	D3[i] = D3[i].strip('[]')
	D3[i] = np.fromstring(D3[i], sep = ' ')
	feature_vector += list(D3[i])

	D4[i] = D4[i].strip('[]')
	D4[i] = np.fromstring(D4[i], sep = ' ')
	feature_vector += list(D4[i])

	row_list.append([file_path[i], file_class[i], file_name[i], feature_vector])

with open('preprocessed_features.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(row_list)

