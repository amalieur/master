""" Sheet that will be used for clustering of trajectories, using hierarchical clustering """


from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
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



class HCA():
    """ A HCA class created for clustering and visualisation """        
    def __init__(self, city: str, distance_matrix_path: str, n_clusters: int = 30 ):
        self.city = city
        self.n_clusters = n_clusters
        
        self.distance_matrix_path = distance_matrix_path
        self.distances = _mirrorDiagonal(pd.read_csv(os.path.abspath(self.distance_matrix_path),index_col=0))
        self.model, self.clusters = self.generate_agglomerative_clusters()


    def generate_agglomerative_clusters(self) -> list:
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        
        model = AgglomerativeClustering(n_clusters=self.n_clusters, affinity="euclidean", linkage="ward")        
        clusters = model.fit_predict(self.distances)
        
        return model, clusters


    def plot_clusters(self, title: str):
        """ Method that visualises the clusters 
        
        Params
        ---
        clusters : List[clusterindex]
            The clusters derived from agglomerative clustering
        city : str (porto | rome)
            The city that should be clustered
        """
        n_clusters = len(set(self.clusters))

        DATA_FOLDER = f"../data/chosen_data/{self.city.lower()}/"
        META_FILE = f"../data/chosen_data/{self.city.lower()}/META-1000.txt"

        files = mfh.read_meta_file(META_FILE)
        trajectories = fh.load_trajectory_files(files, DATA_FOLDER)
        
        keys = sorted(trajectories.keys())

        cmap = plt.get_cmap('brg')
        fig, axs = plt.subplots(6,5, sharex=True, sharey=True, figsize=(15, 15), dpi=300)
        fig.set
        plt.subplots_adjust(hspace=0, wspace=0)
        for i, ax in enumerate(axs.flat):
            j = 0
            while j < 1000:
                if self.clusters[j] == i:
                    t_index = keys[j]
                    values = trajectories[t_index]
                    lats, lons = list(zip(*values))
                    color = cmap(float(i)/n_clusters)
                    
                    traj_len = len(lats)
                    cm = plt.get_cmap("winter")
                    ax.set_prop_cycle(color=[cm(1.*i/(traj_len-1)) for i in range(traj_len-1)])
                    #ax.text(0.01,0.99, i)
                    #ax.spines["top"].set_visible(False)
                    #ax.spines["right"].set_visible(False)
                    #ax.spines["bottom"].set_visible(False)
                    #ax.spines["left"].set_visible(False)
                    for k in range(traj_len-1):
                        ax.plot(lons[k:k+2], lats[k:k+2])


                    #ax.plot(lons,lats, color=color)
                j+=1
        for ax in fig.get_axes():
            ax.label_outer()

        plt.show()



    def silhouette_score(self) -> float:

        silhouette = metrics.silhouette_score(self.distances, self.clusters)

        return silhouette
    

    def davies_bouldin(self) -> float:
        davies_bouldin = metrics.davies_bouldin_score(X=self.distances, labels=self.clusters)
        return davies_bouldin


    def calinski_harabaz(self) -> float:
        calinski_harabaz = metrics.calinski_harabasz_score(self.distances, self.clusters)
        return calinski_harabaz