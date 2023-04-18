""" Sheet that will be used for clustering of trajectories, using affinty propagation clustering """


from sklearn.cluster import AffinityPropagation
from sklearn import metrics

import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import metafile_handler as mfh
from utils import file_handler as fh

def _mirrorDiagonal(M: np.ndarray ) -> np.ndarray:
    """Flips and mirrors a two-dimenional np.array """
    return M.values + np.rot90(np.fliplr(M.values))

def generate_affinity_clusters(preference: int, distance_matrix_path: str, convergence_iter: int = 15, max_iter: int = 200, damping: float = 0.5) -> list:
    distance_path = os.path.abspath(distance_matrix_path)
    distances = _mirrorDiagonal(pd.read_csv(distance_path, index_col=0))
    
    #model = AffinityPropagation(preference=preference, affinity="euclidean", convergence_iter=convergence_iter, max_iter=max_iter, damping=damping)
    model = AffinityPropagation(preference=preference, affinity="euclidean")
    clusters = model.fit_predict(distances)
    
    return clusters, distances


def test_silhouette_score(preference: int, distance_matrix_path: str, convergence_iter: int = 15, max_iter: int = 200, damping: float = 0.5) -> list:
    distance_path = os.path.abspath(distance_matrix_path)
    distances = _mirrorDiagonal(pd.read_csv(distance_path, index_col=0))

    model = AffinityPropagation(preference=preference, affinity="euclidean", convergence_iter=convergence_iter, max_iter=max_iter, damping=damping)
    clusters = model.fit_predict(distances)

    silhouette = metrics.silhouette_score(distances, clusters)

    return silhouette




def plot_clusters(clusters: np.array, city: str):
    """ Method that visualises the clusters 
    
    Params
    ---
    clusters : List[clusterindex]
        The clusters derived from agglomerative clustering
    city : str (porto | rome)
        The city that should be clustered
    """
    n_clusters = len(set(clusters))

    DATA_FOLDER = f"../data/chosen_data/{city}/"
    META_FILE = f"../data/chosen_data/{city}/META-1000.txt"

    files = mfh.read_meta_file(META_FILE)
    trajectories = fh.load_trajectory_files(files, DATA_FOLDER)
    
    keys = sorted(trajectories.keys())

    fig, axs = plt.subplots(5,8, sharex=True, sharey=True, figsize=(15, 15), dpi=300)
    cmap = plt.get_cmap('brg')
    for i, ax in enumerate(axs.flat):
        j = 0
        #if clusters.tolist().count(i) < 5:
        #    continue
        while j < 1000:
            if clusters[j] == i:
                t_index = keys[j]
                values = trajectories[t_index]
                lats, lons = list(zip(*values))
                color = cmap(float(i)/n_clusters)

                traj_len = len(lats)
                cm = plt.get_cmap("winter")
                ax.set_prop_cycle(color=[cm(1.*i/(traj_len-1)) for i in range(traj_len-1)])
                
                for k in range(traj_len-1):
                    ax.plot(lats[k:k+2], lons[k:k+2])
                
                #ax.plot(lons,lats, color=color)
            j+=1
    for ax in fig.get_axes():
        ax.label_outer()

    plt.show()