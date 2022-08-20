Clustering with Noise Points Detection
======================================


.. code-block:: python

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import genieclust









Let's load an example data set that can be found
the on `hdbscan <https://github.com/scikit-learn-contrib/hdbscan>`_
package's project site:


.. code-block:: python

    dataset = "hdbscan"
    X = np.loadtxt("%s.data.gz" % dataset, ndmin=2)
    labels_true = np.loadtxt("%s.labels0.gz" % dataset, dtype=np.intp)-1
    n_clusters = len(np.unique(labels_true[labels_true>=0]))






Here are the "reference" labels as identified by an expert (of course,
each dataset might reveal many different clusterings that a user might
find useful for whatever their goal is).
Labels -1 denote noise points (light grey markers).


.. code-block:: python

    genieclust.plots.plot_scatter(X, labels=labels_true, alpha=0.5)
    plt.title("(n=%d, true n_clusters=%d)" % (X.shape[0], n_clusters))
    plt.axis("equal")
    plt.show()


.. figure:: figures/noise_noise-scatter_1.png
   :width: 15 cm

   Reference labels.





Smoothing Factor
----------------


The `genieclust` package allows for clustering with respect
to a mutual reachability distance,
:math:`d_M`,
known from the HDBSCAN\* algorithm :cite:`hdbscan`\ .
It is parameterised with *a smoothing factor*, ``M``, which
controls how eagerly we tend to classify points as noise.

Here are the effects of playing with the `M` parameter
(we keep the default `gini_threshold`):


.. code-block:: python

    Ms = [2, 5, 10, 25]
    for i in range(len(Ms)):
        g = genieclust.Genie(n_clusters=n_clusters, M=Ms[i])
        labels_genie = g.fit_predict(X)
        plt.subplot(2, 2, i+1)
        genieclust.plots.plot_scatter(X, labels=labels_genie, alpha=0.5)
        plt.title("(gini_threshold=%g, M=%d)"%(g.gini_threshold, g.M))
        plt.axis("equal")
    plt.show()


.. figure:: figures/noise_noise-Genie1_1.png
   :width: 15 cm

   Labels predicted by Genie with noise point detection.



For a more natural look-and-feel, it can be a good idea to first identify
the noise points with Genie, remove them from the data set (or at least
temporarily disable), and then apply the clustering procedure once again
(did we mention that our algorithm is fast?)
but now with respect to the original distance (here: Euclidean):


.. code-block:: python

    # Step 1: Noise point identification
    g1 = genieclust.Genie(n_clusters=n_clusters, M=50)
    labels_noise = g1.fit_predict(X)
    non_noise = (labels_noise >= 0) # True == non-noise point
    # Step 2: Clustering of non-noise points:
    g2 = genieclust.Genie(n_clusters=n_clusters)
    labels_genie = g2.fit_predict(X[non_noise, :])
    # Replace old labels with the new ones:
    labels_noise[non_noise] = labels_genie
    # Scatter plot:
    genieclust.plots.plot_scatter(X, labels=labels_noise, alpha=0.5)
    plt.title("(gini_threshold=%g, noise points removed first; M=%d)"%(g2.gini_threshold, g1.M))
    plt.axis("equal")
    plt.show()


.. figure:: figures/noise_noise-Genie2_1.png
   :width: 15 cm

   Labels predicted by Genie when noise points were removed from the dataset.




However, contrary to an excellent implementation of HDBSCAN\*
that is featured in the `hdbscan <https://github.com/scikit-learn-contrib/hdbscan>`_
package :cite:`hdbscanpkg` and which also relies on a minimum spanning tree w.r.t. :math:`d_M`,
here we still have the hierarchical Genie :cite:`genieins` algorithm under the hood.
This means we can ask for any number of clusters and get what we asked for.
Moreover, we can easily switch between partitions
of finer or coarser granularity.



.. code-block:: python

    ncs = [5, 6, 7, 8, 10, 15]
    for i in range(len(ncs)):
        g = genieclust.Genie(n_clusters=ncs[i])
        labels_genie = g.fit_predict(X[non_noise, :])
        plt.subplot(3, 2, i+1)
        labels_noise[non_noise] = labels_genie
        genieclust.plots.plot_scatter(X, labels=labels_noise, alpha=0.5)
        plt.title("(n_clusters=%d)"%(g.n_clusters))
        plt.axis("equal")
    plt.show()


.. figure:: figures/noise_noise-Genie3_1.png
   :width: 15 cm

   Labels predicted by Genie when noise points were removed from the dataset.





A Comparision with HDBSCAN\*
----------------------------


Here are the results returned by `hdbscan` with default parameters:


.. code-block:: python

    import hdbscan





.. code-block:: python

    h = hdbscan.HDBSCAN()
    labels_hdbscan = h.fit_predict(X)
    genieclust.plots.plot_scatter(X, labels=labels_hdbscan, alpha=0.5)
    plt.title("(min_cluster_size=%d, min_samples=%d)" % (
        h.min_cluster_size, h.min_samples or h.min_cluster_size))
    plt.axis("equal")
    plt.show()


.. figure:: figures/noise_noise-HDBSCAN1_1.png
   :width: 15 cm

   Labels predicted by HDBSCAN\*.




By tuning `min_cluster_size` and/or `min_samples` (which corresponds to our `M` parameter;
by the way, `min_samples` defaults to `min_cluster_size` if not provided explicitly),
we can obtain a partition that is even closer to the reference one:



.. code-block:: python

    mcss = [5, 10, 25]
    mss = [5, 10]
    for i in range(len(mcss)):
        for j in range(len(mss)):
            h = hdbscan.HDBSCAN(min_cluster_size=mcss[i], min_samples=mss[j])
            labels_hdbscan = h.fit_predict(X)
            plt.subplot(3, 2, i*len(mss)+j+1)
            genieclust.plots.plot_scatter(X, labels=labels_hdbscan, alpha=0.5)
            plt.title("(min_cluster_size=%d, min_samples=%d)" % (
                h.min_cluster_size, h.min_samples or h.min_cluster_size))
            plt.axis("equal")
    plt.show()


.. figure:: figures/noise_noise-HDBSCAN2_1.png
   :width: 15 cm

   Labels predicted by HDBSCAN\*.



Neat.

