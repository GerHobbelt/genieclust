# *genieclust*: Fast and Robust Hierarchical Clustering with Noise Point Detection

::::{epigraph}
**Genie finds meaningful clusters and is fast even on large data sets.**
::::

::::{image} _static/img/genie_toy_example.png
:class: img-right-align-always
:alt: Genie
:width: 128px
::::


The *genieclust* package {cite}`genieclust` equips Python and R users with
a faster and more powerful version of *Genie* {cite}`genieins` — a robust
and outlier resistant clustering algorithm, originally published as an R package
[*genie*](https://cran.r-project.org/web/packages/genie).

The idea behind *Genie* is beautifully simple. First, make each individual
point the sole member of its own cluster. Then, keep merging pairs
of the closest clusters, one after another. However, to **prevent
the formation of clusters of highly imbalanced sizes**
a point group of the smallest size will sometimes be matched with its nearest
neighbours.

Genie's appealing simplicity goes hand in hand with its usability;
it **often outperforms other clustering approaches**
such as K-means, BIRCH, or average, Ward, and complete linkage
on {any}`benchmark data <weave/benchmarks_ar>`.

Genie is also **very fast** — determining the whole cluster hierarchy
for datasets of millions of points, can be completed within
{any}`minutes <weave/timings>`.
Therefore, it is capable of solving **extreme clustering tasks**
(large datasets with any number of clusters to detect)
on data that fit into memory.
Thanks to the use of *nmslib* {cite}`nmslib`,
sparse or string inputs are also supported.

Genie also allows clustering with respect to mutual reachability distances
so that it can act as a **noise point detector** or a robustified version
of *HDBSCAN\** {cite}`hdbscan` that is able to detect a predefined
number of clusters and so it doesn't dependent on the *DBSCAN*'s somewhat
difficult-to-set `eps` parameter.



The **Python version** of *genieclust* is available via
[PyPI](https://pypi.org/project/genieclust/), e.g.,
via a call to

```bash
pip3 install genieclust
```

from the command line or through your favourite package manager.
Note a familiar *scikit-learn*-like {cite}`sklearn_api` look-and-feel:

```python
import genieclust
X = ...  # some data
g = genieclust.Genie(n_clusters=2)
labels = g.fit_predict(X)
```

::::{epigraph}
*To learn more about Python, check out Marek's recent open-access (free!) textbook*
[Minimalist Data Wrangling in Python](https://datawranglingpy.gagolewski.com/)
{cite}`datawranglingpy`.
::::



The **R version** of *genieclust* can be downloaded from
[CRAN](https://cran.r-project.org/web/packages/genieclust/)
by calling:

```r
install.packages("genieclust")
```

Its interface is compatible with the classic `stats::hclust()`, but there is more.

```r
X <- ...  # some data
h <- gclust(X)
plot(h)  # plot cluster dendrogram
cutree(h, k=2)
# or simply:  genie(X, k=2)
```



*genieclust* is distributed
under the open source GNU AGPL v3 license and can be downloaded from
[GitHub](https://github.com/gagolews/genieclust).
The core functionality is implemented in the form of a header-only C++
library, so it may be adapted to new environments relatively easily —
any contributions are welcome (Julia, Matlab, etc.).

**Author and Maintainer**: [Marek Gagolewski](https://www.gagolewski.com)

**Contributors**:
[Maciej Bartoszuk](http://bartoszuk.rexamine.com), [Anna Cena](https://cena.rexamine.com) (R packages
[*genie*](https://cran.r-project.org/web/packages/genie) /*genieclust*'s predecessor {cite}`genieins`/
and [*CVI*](https://github.com/gagolews/optim_cvi) /some internal cluster validity measures {cite}`cvi`/),
[Peter M. Larsen](https://github.com/pmla/)
(an [implementation](https://github.com/scipy/scipy/blob/main/scipy/optimize/rectangular_lsap/rectangular_lsap.cpp)
of the shortest augmenting path algorithm for the rectangular assignment problem
which we use for computing the normalised accuracy and pair sets index).



::::{toctree}
:maxdepth: 2
:caption: genieclust
:hidden:

About <self>
Author <https://www.gagolewski.com/>
::::


::::{toctree}
:maxdepth: 2
:caption: Examples and Tutorials

weave/basics
weave/sklearn_toy_example
weave/benchmarks_ar
weave/timings
weave/noise
weave/sparse
weave/string
weave/r
::::


::::{toctree}
:maxdepth: 1
:caption: API Documentation

genieclust
rapi
::::


::::{toctree}
:maxdepth: 1
:caption: See Also

Source Code (GitHub) <https://github.com/gagolews/genieclust>
Bug Tracker and Feature Suggestions <https://github.com/gagolews/genieclust/issues>
PyPI Entry <https://pypi.org/project/genieclust/>
CRAN Entry <https://CRAN.R-project.org/package=genieclust>
Clustering Benchmarks <https://github.com/gagolews/clustering-benchmarks>
Data Wrangling in Python <https://datawranglingpy.gagolewski.com/>
::::


::::{toctree}
:maxdepth: 1
:caption: Appendix

news
weave/benchmarks_details
weave/benchmarks_approx
z_bibliography
::::


<!--
Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
-->