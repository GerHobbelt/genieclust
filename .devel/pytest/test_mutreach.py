import numpy as np
import scipy.spatial.distance
import genieclust
import time
import gc

def mutual_reachability_distance_old(D, M):
    if M <= 2: return D.copy()
    argD = np.argsort(D, axis=1)
    # argD should be read row-wise, i.e.,
    # argD[i,:] is the ordering permutation for ith point's NNs
    Dcore = D[np.arange(D.shape[0]),argD[:, M-1]]
    res = np.maximum(np.maximum(D, Dcore.reshape(-1, 1)), Dcore.reshape(1, -1))
    res[np.arange(D.shape[0]),np.arange(D.shape[0])] = 0.0
    return res



import os
if os.path.exists(".devel/benchmark_data"):
    path = ".devel/benchmark_data"
elif os.path.exists("benchmark_data"):
    path = "benchmark_data"
else:
    path = "../benchmark_data"



def test_mutreach():
    for dataset in ["jain", "pathbased"]:#, "s1", "Aggregation", "WUT_Smile", "unbalance", "a1"]:
        X = np.loadtxt("%s/%s.data.gz" % (path,dataset), ndmin=2)
        labels = np.loadtxt("%s/%s.labels0.gz" % (path,dataset), dtype=np.intc)
        label_counts = np.unique(labels,return_counts=True)[1]
        k = len(label_counts)
        D = scipy.spatial.distance.pdist(X)
        D = scipy.spatial.distance.squareform(D)

        for M in [2, 3, 5, 10]:
            gc.collect()
            t0 = time.time()
            D1 = genieclust.tools._mutual_reachability_distance(
                D,
                genieclust.tools._core_distance(D, M))
            print("%-20s\tM=%2d\tt=%.3f" % (dataset, M, time.time()-t0), end="\t")
            t0 = time.time()

            D2 = mutual_reachability_distance_old(D, M)
            print("t_old=%.3f" % (time.time()-t0,))
            dist = np.mean((D1 - D2)**2)
            assert dist < 1e-12

            for g in [0.01, 0.3, 0.5, 0.7, 1.0]:
                for k in [2, 3, 5]:
                    cl = genieclust.Genie(k, gini_threshold=g, M=M).fit_predict(X)+1
                    assert max(cl) == k
                    assert np.unique(cl).shape[0] == k+1

                    cl2 = genieclust.Genie(k, gini_threshold=g, M=M, postprocess='all').fit_predict(X)+1
                    assert np.all(cl2[cl>0] == cl[cl>0])

                    cl3 = genieclust.Genie(k, gini_threshold=g, M=M, postprocess='none').fit_predict(X)+1
                    assert np.all(cl3[cl3>0] == cl[cl3>0])
                    assert np.all(cl3[cl3>0] == cl2[cl3>0])

                    # TODO: what other tests?

            D1 = None
            D2 = None


# Note that CDistanceMutualReachability is tested in test_mst.py




if __name__ == "__main__":
    test_mutreach()
