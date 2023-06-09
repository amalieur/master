from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import AffinityPropagation
from scipy.cluster.hierarchy import dendrogram
import os
import pandas as pd
import numpy as np


def _mirrorDiagonal(M: np.ndarray ) -> np.ndarray:
    """Flips and mirrors a two-dimenional np.array """
    return M.values + np.rot90(np.fliplr(M.values))


path_to_distances = os.path.abspath("C:\\Users\\bafla\\Desktop\\Projects\\master\\code\\benchmarks\\similarities\\rome-dtw.csv")

distances = _mirrorDiagonal(pd.read_csv(path_to_distances, index_col=0))
print(distances)
model = AgglomerativeClustering(n_clusters=48, affinity="euclidean", linkage="ward")


a = model.fit_predict(distances)

#print(model)
#print(a)



AP = AffinityPropagation(preference=-7000, affinity="euclidean")
b = AP.fit_predict(distances)

#print(b)

print(len(set(b)))


