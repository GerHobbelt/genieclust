Example: Sparse Data and Movie Recommendation
=============================================

To illustrate how *genieclust* handles
`sparse data <https://en.wikipedia.org/wiki/Sparse_matrix>`_,
let's perform a simple exercise in movie recommendation based on
`MovieLens <https://grouplens.org/datasets/movielens/latest/>`_ data.


.. code-block:: python

    import numpy as np
    import scipy.sparse
    import pandas as pd








First we load the `ratings` data frame
and map the movie IDs to consecutive integers.


.. code-block:: python

    ratings = pd.read_csv("ml-9-2018-small/ratings.csv")
    ratings["movieId"] -= 1
    ratings["userId"] -= 1
    old_movieId_map = np.unique(ratings["movieId"])
    ratings["movieId"] = np.searchsorted(old_movieId_map, ratings["movieId"])
    ratings.head()


::

    ##    userId  movieId  rating  timestamp
    ## 0       0        0     4.0  964982703
    ## 1       0        2     4.0  964981247
    ## 2       0        5     4.0  964982224
    ## 3       0       43     5.0  964983815
    ## 4       0       46     5.0  964982931



Then we read the movie meta data and transform the movie IDs
in the same way:


.. code-block:: python

    movies = pd.read_csv("ml-9-2018-small/movies.csv")
    movies["movieId"] -= 1
    movies = movies.loc[movies.movieId.isin(old_movieId_map), :]
    movies["movieId"] = np.searchsorted(old_movieId_map, movies["movieId"])
    movies.iloc[:, :2].head()


::

    ##    movieId                               title
    ## 0        0                    Toy Story (1995)
    ## 1        1                      Jumanji (1995)
    ## 2        2             Grumpier Old Men (1995)
    ## 3        3            Waiting to Exhale (1995)
    ## 4        4  Father of the Bride Part II (1995)




Conversion of ratings to a CSR-format sparse matrix:


.. code-block:: python

    n = ratings.movieId.max()+1
    d = ratings.userId.max()+1
    X = scipy.sparse.dok_matrix((n,d), dtype=np.float32)
    X[ratings.movieId, ratings.userId] = ratings.rating
    X = X.tocsr()
    print(repr(X))


::

    ## <9724x610 sparse matrix of type '<class 'numpy.float32'>'
    ##         with 100836 stored elements in Compressed Sparse Row format>




First few observations:


.. code-block:: python

    X[:5, :10].todense()


::

    ## matrix([[4. , 0. , 0. , 0. , 4. , 0. , 4.5, 0. , 0. , 0. ],
    ##         [0. , 0. , 0. , 0. , 0. , 4. , 0. , 4. , 0. , 0. ],
    ##         [4. , 0. , 0. , 0. , 0. , 5. , 0. , 0. , 0. , 0. ],
    ##         [0. , 0. , 0. , 0. , 0. , 3. , 0. , 0. , 0. , 0. ],
    ##         [0. , 0. , 0. , 0. , 0. , 5. , 0. , 0. , 0. , 0. ]],
    ## dtype=float32)



Let's extract 200 clusters with Genie with respect to  cosine similarity between films' ratings
as given by users (two movies considered similar if they get similar reviews).
Sparse inputs are supported by the approximate version of the algorithm
which  relies on the
near-neighbour search routines implemented in the `nmslib` package.



.. code-block:: python

    import genieclust
    g = genieclust.Genie(n_clusters=200, exact=False, affinity="cosinesimil_sparse")
    movies["cluster"] = g.fit_predict(X)




Here are the members of an example cluster:


.. code-block:: python

    movies["cluster"] = g.fit_predict(X)
    which_cluster = movies.cluster[movies.title=="Monty Python's The Meaning of Life (1983)"]
    movies.loc[movies.cluster == int(which_cluster)].title.sort_values()


::

    ## 2097                                     Airplane! (1980)
    ## 2907                                 Almost Famous (2000)
    ## 1914                                  Analyze This (1999)
    ## 969                             Back to the Future (1985)
    ## 1486                    Back to the Future Part II (1989)
    ## 1487                   Back to the Future Part III (1990)
    ## 2259                          Being John Malkovich (1999)
    ## 2916                                  Best in Show (2000)
    ## 921                            Blues Brothers, The (1980)
    ## 89                                   Bottle Rocket (1996)
    ## 2084                                     Bowfinger (1999)
    ## 2190                                Boys Don't Cry (1999)
    ## 2888                                     Cell, The (2000)
    ## 955                                      Duck Soup (1933)
    ## 836                     E.T. the Extra-Terrestrial (1982)
    ## 1960                                      Election (1999)
    ## 2036                                Eyes Wide Shut (1999)
    ## 819                           Fish Called Wanda, A (1988)
    ## 1232                               Full Monty, The (1997)
    ## 964                                  Groundhog Day (1993)
    ## 2605                                 High Fidelity (2000)
    ## 1211                     Hunt for Red October, The (1990)
    ## 2382                                      Magnolia (1999)
    ## 863                Monty Python and the Holy Grail (1975)
    ## 2094    Monty Python's And Now for Something Completel...
    ## 820                   Monty Python's Life of Brian (1979)
    ## 4581            Monty Python's The Meaning of Life (1983)
    ## 2892       Naked Gun 2 1/2: The Smell of Fear, The (1991)
    ## 2891    Naked Gun: From the Files of Police Squad!, Th...
    ## 3010                    O Brother, Where Art Thou? (2000)
    ## 1394                                  Out of Sight (1998)
    ## 2443                                 Patriot Games (1992)
    ## 850                    People vs. Larry Flynt, The (1996)
    ## 899                            Princess Bride, The (1987)
    ## 2020                     Run Lola Run (Lola rennt) (1998)
    ## 1796                                      Rushmore (1998)
    ## 1979     Star Wars: Episode I - The Phantom Menace (1999)
    ## 224             Star Wars: Episode IV - A New Hope (1977)
    ## 898     Star Wars: Episode V - The Empire Strikes Back...
    ## 911     Star Wars: Episode VI - Return of the Jedi (1983)
    ## 934                                     Sting, The (1973)
    ## 987                             This Is Spinal Tap (1984)
    ## 2174                                   Three Kings (1999)
    ## 839                                        Top Gun (1986)
    ## 3016                                       Traffic (2000)
    ## 1113                           Waiting for Guffman (1996)
    ## 977                             Young Frankenstein (1974)
    ## Name: title, dtype: object






The above was performed on an abridged version of the MovieLens dataset.
The project's `website <https://grouplens.org/datasets/movielens/latest/>`_
also features a full database that yields a 53889x283228 ratings table
(with 27753444  non-zero elements) -- such a matrix would definitely
not fit into our RAM if it was in the dense form.
Determining the whole cluster hierarchy takes only 144 secs.
Here is one of 500 clusters extracted:

.. code::

    ## 13327                       Blackadder Back & Forth (1999)
    ## 13328                  Blackadder's Christmas Carol (1988)
    ## 3341                              Creature Comforts (1989)
    ## 1197       Grand Day Out with Wallace and Gromit, A (1989)
    ## 2778                            Hard Day's Night, A (1964)
    ## 2861                                          Help! (1965)
    ## 2963                              How I Won the War (1967)
    ## 6006        Monty Python Live at the Hollywood Bowl (1982)
    ## 1113                Monty Python and the Holy Grail (1975)
    ## 2703     Monty Python's And Now for Something Completel...
    ## 1058                   Monty Python's Life of Brian (1979)
    ## 6698             Monty Python's The Meaning of Life (1983)
    ## 27284                                  Oliver Twist (1997)
    ## 2216                                 Producers, The (1968)
    ## 4716                                   Quadrophenia (1979)
    ## 6027             Secret Policeman's Other Ball, The (1982)
    ## 27448                                    The Basket (2000)
    ## 2792                                          Tommy (1975)
    ## 10475    Wallace & Gromit in The Curse of the Were-Rabb...
    ## 732                 Wallace & Gromit: A Close Shave (1995)
    ## 708      Wallace & Gromit: The Best of Aardman Animatio...
    ## 1125           Wallace & Gromit: The Wrong Trousers (1993)
    ## 13239    Wallace and Gromit in 'A Matter of Loaf and De...
    ## 2772                               Yellow Submarine (1968)
    ## 1250                             Young Frankenstein (1974)
    ## Name: title, dtype: object



