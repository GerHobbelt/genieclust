# compare_partitions: External Cluster Validity Measures and Pairwise Partition Similarity Scores

## Description

The functions described in this section quantify the similarity between two label vectors `x` and `y` which represent two partitions of a set of $n$ elements into, respectively, $K$ and $L$ nonempty and pairwise disjoint subsets.

For instance, `x` and `y` can be two clusterings of a dataset with $n$ observations specified by two vectors of labels. These functions can be used as external cluster validity measures, where we assume that `x` is the reference (ground-truth) partition (compare Gagolewski, 2022).

## Usage

``` r
adjusted_asymmetric_accuracy(x, y = NULL)

normalized_accuracy(x, y = NULL)

pair_sets_index(x, y = NULL, simplified = FALSE)

adjusted_rand_score(x, y = NULL)

rand_score(x, y = NULL)

adjusted_fm_score(x, y = NULL)

fm_score(x, y = NULL)

mi_score(x, y = NULL)

normalized_mi_score(x, y = NULL)

adjusted_mi_score(x, y = NULL)

normalized_confusion_matrix(x, y = NULL)

normalizing_permutation(x, y = NULL)
```

## Arguments

|              |                                                                                                                                                                                                                                                                           |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `x`          | an integer vector of length n (or an object coercible to) representing a K-partition of an n-set (e.g., a reference partition), or a confusion matrix with K rows and L columns (see [`table(x, y)`](https://stat.ethz.ch/R-manual/R-devel/library/base/html/table.html)) |
| `y`          | an integer vector of length n (or an object coercible to) representing an L-partition of the same set (e.g., the output of a clustering algorithm we wish to compare with `x`), or NULL (if x is an K\*L confusion matrix)                                                |
| `simplified` | whether to assume E=1 in the definition of the pair sets index index, i.e., use Eq. (20) instead of (18); see (Rezaei, Franti, 2016).                                                                                                                                     |

## Details

Each index except `adjusted_asymmetric_accuracy()` can act as a pairwise partition similarity score: it is symmetric, i.e., `index(x, y) == index(y, x)`.

Each index except `mi_score()` (which computes the mutual information score) outputs 1 given two identical partitions. Note that partitions are always defined up to a bijection of the set of possible labels, e.g., (1, 1, 2, 1) and (4, 4, 2, 4) represent the same 2-partition.

`adjusted_asymmetric_accuracy()` (Gagolewski, 2022) is an external cluster validity measure which assumes that the label vector `x` (or rows in the confusion matrix) represents the reference (ground truth) partition. It is a corrected-for-chance summary of the proportion of correctly classified points in each cluster (with cluster matching based on the solution to the maximal linear sum assignment problem; see [`normalized_confusion_matrix`](compare_partitions.md)), given by: $(\max_\sigma \sum_{i=1}^K (c_{i, \sigma(i)}/(c_{i, 1}+...+c_{i, K})) - 1)/(K - 1)$, where $C$ is the confusion matrix.

`normalized_accuracy()` is defined as $(Accuracy(C_\sigma)-1/max(K,L))/(1-1/max(K,L))$, where $C_\sigma$ is a version of the confusion matrix for given `x` and `y` with columns permuted based on the solution to the maximal linear sum assignment problem. The $Accuracy(C_\sigma)$ part is sometimes referred to as set-matching classification rate or pivoted accuracy.

`pair_sets_index()` gives the Pair Sets Index (PSI) adjusted for chance (Rezaei, Franti, 2016). Pairing is based on the solution to the linear sum assignment problem of a transformed version of the confusion matrix. Its simplified version assumes E=1 in the definition of the index, i.e., uses Eq. (20) instead of (18).

`rand_score()` gives the Rand score (the \"probability\" of agreement between the two partitions) and `adjusted_rand_score()` is its version corrected for chance, see (Hubert, Arabie, 1985), its expected value is 0.0 given two independent partitions. Due to the adjustment, the resulting index might also be negative for some inputs.

Similarly, `fm_score()` gives the Fowlkes-Mallows (FM) score and `adjusted_fm_score()` is its adjusted-for-chance version, see (Hubert, Arabie, 1985).

Note that both the (unadjusted) Rand and FM scores are bounded from below by $1/(K+1)$ if $K=L$, hence their adjusted versions are preferred.

`mi_score()`, `adjusted_mi_score()` and `normalized_mi_score()` are information-theoretic scores, based on mutual information, see the definition of $AMI_{sum}$ and $NMI_{sum}$ in (Vinh et al., 2010).

`normalized_confusion_matrix()` computes the confusion matrix and permutes its rows and columns so that the sum of the elements of the main diagonal is the largest possible (by solving the maximal assignment problem). The function only accepts $K \leq L$. The sole reordering of the columns of a confusion matrix can be determined by calling `normalizing_permutation()`.

Also note that the built-in [`table()`](https://stat.ethz.ch/R-manual/R-devel/library/base/html/table.html) determines the standard confusion matrix.

## Value

Each cluster validity measure is a single numeric value.

`normalized_confusion_matrix()` returns an integer matrix.

## Author(s)

[Marek Gagolewski](https://www.gagolewski.com/) and other contributors

## References

Gagolewski M., *A Framework for Benchmarking Clustering Algorithms*, 2022, <https://clustering-benchmarks.gagolewski.com>.

Gagolewski M., Adjusted asymmetric accuracy: A well-behaving external cluster validity measure, 2022, under review (preprint), [doi:10.48550/arXiv.2209.02935](https://doi.org/10.48550/arXiv.2209.02935).

Hubert L., Arabie P., Comparing partitions, *Journal of Classification* 2(1), 1985, 193-218, esp. Eqs. (2) and (4).

Meila M., Heckerman D., An experimental comparison of model-based clustering methods, *Machine Learning* 42, 2001, pp. 9-29, [doi:10.1023/A:1007648401407](https://doi.org/10.1023/A%3A1007648401407).

Rezaei M., Franti P., Set matching measures for external cluster validity, *IEEE Transactions on Knowledge and Data Mining* 28(8), 2016, 2173-2186.

Steinley D., Properties of the Hubert-Arabie adjusted Rand index, *Psychological Methods* 9(3), 2004, pp. 386-396, [doi:10.1037/1082-989X.9.3.386](https://doi.org/10.1037/1082-989X.9.3.386).

Vinh N.X., Epps J., Bailey J., Information theoretic measures for clusterings comparison: Variants, properties, normalization and correction for chance, *Journal of Machine Learning Research* 11, 2010, 2837-2854.

## See Also

The official online manual of <span class="pkg">genieclust</span> at <https://genieclust.gagolewski.com/>

Gagolewski M., <span class="pkg">genieclust</span>: Fast and robust hierarchical clustering, *SoftwareX* 15:100722, 2021, [doi:10.1016/j.softx.2021.100722](https://doi.org/10.1016/j.softx.2021.100722).

## Examples




```r
y_true <- iris[[5]]
y_pred <- kmeans(as.matrix(iris[1:4]), 3)$cluster
adjusted_asymmetric_accuracy(y_true, y_pred)
## [1] 0.84
normalized_accuracy(y_true, y_pred)
## [1] 0.84
pair_sets_index(y_true, y_pred)
## [1] 0.7568238
pair_sets_index(y_true, y_pred, simplified=TRUE)
## [1] 0.7470968
adjusted_rand_score(y_true, y_pred)
## [1] 0.7302383
rand_score(table(y_true, y_pred)) # the same
## [1] 0.8797315
adjusted_fm_score(y_true, y_pred)
## [1] 0.7304411
fm_score(y_true, y_pred)
## [1] 0.8208081
mi_score(y_true, y_pred)
## [1] 0.8255911
normalized_mi_score(y_true, y_pred)
## [1] 0.7581757
adjusted_mi_score(y_true, y_pred)
## [1] 0.7551192
normalized_confusion_matrix(y_true, y_pred)
##      [,1] [,2] [,3]
## [1,]   50    0    0
## [2,]    0   48    2
## [3,]    0   14   36
normalizing_permutation(y_true, y_pred)
## [1] 1 2 3
```