import numpy as np
import pandas as pd
from gimmebio.ram_seq import rs_matrix, seq_power_series
from scipy.spatial import KDTree


SEED_SIZE = 10 * 1000
BALANCE_GAP = 10 * 1000
BATCH_SIZE = 1000


def hamming_distance(k1, k2):
    d = 0
    for v1, v2 in zip(k1, k2):
        d += 1 if v1 != v2 else 0
    return d


class KDRFTCover:

    def __init__(self, radius, seed_size=-1):
        self.rf_coeffs = None
        self.seed_size = seed_size
        self.points = []
        self.centroids = []
        self.batch = []
        self.radius = radius
        self.clusters = {}
        self.tree = None
        self.raw = []

    def ramify(self, kmer):
        if self.rf_coeffs is None:
            self.rf_coeffs = rs_matrix(len(kmer))
        rft = seq_power_series(kmer, RS=self.rf_coeffs)[:min(12, len(kmer))]
        return np.array(rft)

    def add(self, kmer):
        self.raw.append(kmer)
        rft = self.ramify(kmer)
        self.points.append(rft)

    def search(self, kmer, max_dist):
        rft = self.ramify(kmer)
        centroids = self.tree.query_ball_point(rft, max_dist, eps=0.01)
        return centroids

    def greedy_clusters(self):
        all_tree = KDTree(np.array(self.points))
        clusters, clustered_points = {}, set()
        batch_map, batch_points = {}, []
        for i, rft in enumerate(self.points):
            if i in clustered_points:
                continue
            batch_map[len(batch_points)] = i
            batch_points.append(rft)
            if len(batch_points) == 1000:
                self._greedy_cluster_batch(
                    all_tree, batch_map, batch_points, clusters, clustered_points
                )
                batch_map, batch_points = {}, []
        if batch_points:
            self._greedy_cluster_batch(
                all_tree, batch_map, batch_points, clusters, clustered_points
            )
        self.clusters = clusters
        self.centroids = [self.points[i] for i in clusters.keys()]
        self.tree = KDTree(np.array(self.centroids))

    def _greedy_cluster_batch(self, all_tree, batch_map, batch_points, clusters, clustered_points):
        query_tree = KDTree(np.array(batch_points))
        result = query_tree.query_ball_tree(all_tree, self.radius, eps=0.1)
        for i, pts in enumerate(result):
            index_in_all_points = batch_map[i]
            clusters[index_in_all_points] = set([index_in_all_points])
            clustered_points.add(index_in_all_points)
            pts = set(pts)
            pts -= clustered_points
            clusters[index_in_all_points] |= pts
            clustered_points |= pts

    def _cluster_radius(self):
        all_dists = []
        for centroid, cluster in self.clusters.items():
            centroid, dists = self.raw[centroid], []
            for point in [self.raw[i] for i in cluster]:
                dists.append(hamming_distance(centroid, point))
            all_dists.append(pd.Series(dists).quantile([0.5, 0.80, 0.95, 1]))
        all_quants = pd.DataFrame(all_dists).mean()
        return all_quants

    def stats(self):
        r50, r80, r95, r100 = self._cluster_radius()
        return {
            'num_kmers': sum([len(clust) for clust in self.clusters.values()]),
            'num_singletons': sum([
                1 if len(clust) == 1 else 0 for clust in self.clusters.values()
            ]),
            'num_clusters': len(self.clusters),
            'radius_50': r50,
            'radius_80': r80,
            'radius_95': r95,
            'radius_100': r100,
        }
