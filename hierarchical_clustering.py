import argparse
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

parser = argparse.ArgumentParser(description='Obtain hierarchical clustering from distance matrix')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'Distance matrix .mat file')
args = parser.parse_args()

input_filename = args.input_filename[0]

distance_matrix = np.loadtxt(input_filename, dtype='f', delimiter=',')
distance_matrix = distance_matrix[:-1, :-1]
Z = linkage(distance_matrix, method='average', metric='euclidean')
fig = plt.figure(figsize=(25, 10))
plt.title('UPGMA LINEs clustering - ' + input_filename[6:input_filename.index('.')])
plt.xlabel('LINE ID')
plt.ylabel('Distance between sequences')
dn = dendrogram(Z)
plt.savefig(input_filename[6:input_filename.index('.')] + '-upgma.png')