# Prototype-based Machine Learning on Distance Data

Copyright (C) 2019 - Benjamin Paassen  
Machine Learning Research Group  
Center of Excellence Cognitive Interaction Technology (CITEC)  
Bielefeld University

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

## Introduction

This [scikit-learn][scikit] compatible, Python3 library provides several algorithms
to learn prototype models on distance data. At this time, this library features
the following algorithms:

* Relational Neural Gas ([Hammer and Hasenfuss, 2007][Ham2007]) for clustering,
* Relational Generalized Learning Vector Quantization ([Hammer, Hofmann, Schleif, and Zhu, 2014][Ham2014]) for classification, and
* Median Generalized Learning Vector Quantization ([Nebel, Hammer, Frohberg, and Villmann, 2015][Neb2015]) for classification.

Refer to the Quickstart Guide for a note on how to use these models and
refer to the Background section for more details on the algorithms.

Note that this library follows the 

If you intend to use this library in academic work, please cite the respective
reference paper.

## Installation

This package is available on `pypi` as `proto_dist_ml`. You can install
it via

```
pip install proto_dist_ml
```

## QuickStart Guide

For an example we recommend to take a look at the demo in the notebook
`demo.ipynb`. In general, all models in this library follow the [scikit-learn][scikit]
convention, i.e. you need to perform the following steps:

1. Instantiate your model, e.g. via `model = proto_dist_ml.rng.RNG(K)` where
    `K` is the number of prototypes.
2. Fit your model to training data, e.g. via `model.fit(D)`, where `D` is the
    matrix of pairwise distances between your training data points.
3. Perform a prediction for test data, e.g. via `model.predict(D)`, where `D`
    is the matrix of distances from the test to the training data points.

## Background

The basic idea of prototype models is that we can cluster and
classify data by assigning them to the cluster/class of the closest _prototype_,
where a prototype is a data point that represents the cluster/class well.

In case of distance data, we can not express a prototype in vectorial form but
instead need to use an indirect form, namely a convex combination of existing
data points. In other words, our $`k`$th prototype $`w_k`$ is defined as

```math
\vec w_k = \sum_{i=1}^m \alpha_{k, i} \cdot \vec x_i
\qquad \text{where } \sum_{i=1}^m \alpha_{k, i} = 1
\text{ and } \alpha_{k, i} \geq 0 \quad \forall i
```

where $`\vec x_1, \ldots, \vec x_m`$ are the training data points and where
$`\alpha_{k, 1}, \ldots, \alpha_{k, m}`$ are the convex coefficiants
representing prototype $`w_k`$. Because the prototype is fully specified by
the data and the convex coefficients, we do not need any explicit form for
$`w_k`$ anymore.

To cluster/classify new data, we now need to determine the distance between a
data point $`x`$ and a prototpe $`w_k`$. As it turns out, this distance can
also be expressed solely in terms of the convex coefficients and the
data-to-data distances. In particular, we obtain:

```math
d(x, w_k)^2 = \sum_{i=1}^m \alpha_{k, i} \cdot d(x, x_i)^2
- \frac{1}{2} \sum_{i=1}^m \sum_{j=1}^m \alpha_{k, i} \cdot \alpha_{k, j} \cdot d(x_i, x_j)^2
```

In matrix-vector notation we obtain:

```math
d(x, w_k)^2 = {\vec \alpha_k}^T \cdot \vec d^2
- \frac{1}{2} {\vec \alpha_k}^T \cdot D^2 \cdot \vec \alpha_k
```

where $`\vec d^2`$ the vector of distances between $`x`$ and all training
data points $`x_i`$ and where $`D^2`$ is the distance matrix between the
training data points.

The main challenge for distance-based prototype learning is now to optimize
the coefficients $`\alpha_{k, i}`$ according to some meaningful loss function.
The loss function and its optimization differs between the algorithms. In more
detail, we take the following approaches.

### Relational Neural Gas

Relational neural gas (RNG; [Hammer and Hasenfuss, 2007][Ham2007]) is a
clustering approach that tries to optimize the loss function

```math
\sum_{i=1}^m \sum_{k=1}^K h_{i, k} \cdot d(x_i, w_k)^2
```

where $`h_{i, k}`$ quantifies how responsible prototype $`w_k`$ is for
data point $`x_i`$. This term is calculated as follows:

```math
h_{i, k} = \exp(-r_{i, k} / \lambda) \qquad \text{where } r_{i, k} = |\{ l | d(x_i, w_l) < d(x_i, w_k) \}|
```

In other words, $`w_k`$ is the $`r_{i, k}`$-closest prototype to data point
$`x_i`$ and the lower ranked a prototype is (i.e. the closer it is), the higher
is its responsibility for the data point. $`\lambda`$ is a scaling factor that
expresses how many prototypes are still considered. Per default, we start with
$`\lambda = K / 2`$ and then anneal $`\lambda`$ until $`\lambda = 0.01`$, i.e.
only the closest prototype is considered. At that point, the loss above is
equivalent to the $`K`$-means loss.

Given the current values for $h_{i, k}$, optimizing the convex coefficients
$`\alpha_{k, i}`$ is possible in closed form. In particular, we obtain:
$`\alpha_{k, i} = h_{i, k} / \sum_j h_{j, k}`$. The RNG
training procedure thus consists of three steps which are iterated in each
training epoch:

1. Compute the responsibilities $`h_{i, k}`$.
2. Compute the new convex coefficients $`\alpha_{k, i}`$.
3. Decrease $`\lambda`$.

### Relational Generalized Learning Vector Quantization

Relational generalized learning vector quantization (RGLVQ; [Hammer, Hofmann, Schleif, and Zhu, 2014][Ham2014])
is a classification approach which aims at optimizing the generalized learning
vector quantization loss:

```math
\sum_{i=1}^m \Phi\Big(\frac{d_i^+ - d_i^-}{d_i^+ + d_i^-}\Big)
```

where $`d_i^+`$ is the distance of data point $`x_i`$ to the closest prototype
with the same label, $`d_i^-`$ is the distance of data point $`x_i`$ to the
closest prototype with a different label, and $`\Phi`$ is a squashing
function (such as tanh or the logistic function).
Note that data point $`x_i`$ is correctly classified if and only
if $`d_i^+ - d_i^- < 0`$. As such, the GLVQ loss can be regarded as a soft
approximation of the classification error.

Note that this loss has the drawback that distances need to be strictly
positive in order to guarantee a nonzero denominator. This excludes
non-Euclidean distances (i.e. distances which do not correspond to an inner
product) because these may imply negative data-to-prototype distances.

We optimize this loss via L-BFGS, restricting the coefficients to be convex
in each step. The gradient follows directly from the
formula above and the distance formula above. For more details, refer to
([Hammer et al., 2014][Ham2014]).

### Median Generalized Learning Vector Quantization

Median generalized learning vector quantization
(MGLVQ; [Nebel, Hammer, Frohberg, and Villmann, 2015][Neb2015]) is a variant
of GLVQ that restricts prototypes to be strictly data points, i.e. for each
prototype $`w_k`$ there exists exactly one $`i`$, such that $`\alpha_{k, i} = 1`$
and every other coefficient is zero. This has two key advantages. First, it
permits non-Euclidean and even asymmetric distances because we do not rely on
an interpolation between data points. Second, it is more efficient during
classification because we can compute the distances to the prototypes directly
and do not need to use the relational distance formula above.

However, MGLVQ is also more challenging to train because we can not perform a
smooth gradient method but instead must apply a discrete optimization scheme.
In this toolbox, we optimize the GLVQ loss (see above) via greedy hill climbing,
i.e. we try to find any prototype-datapoint combination that would reduce the
loss and apply the first such combination we find until no such move exists
anymore.

## Contents

This library contains the following files.

* `demo.ipynb` : A demo script illustrating how to use this library.
* `LICENSE.md` : A copy of the GPLv3 license.
* `mglvq_test.py` : A set of unit tests for `mglvq.py`.
* `proto_dist_ml/mglvq.py` : An implementation of median generalized
    learning vector quantization.
* `proto_dist_ml/rglvq.py` : An implementation of relational generalized
    learning vector quantization.
* `proto_dist_ml/rng.py` : An implementation of relational neural gas.
* `README.md` : This file.
* `rglvq_test.py` : A set of unit tests for `rglvq.py`.
* `rng_test.py` : A set of unit tests for `rng.py`.

## Licensing

This library is licensed under the [GNU General Public License Version 3][GPLv3].

## Dependencies

This library depends on [NumPy][np] for matrix operations, on [scikit-learn][scikit]
for the base interfaces and on [SciPy][scipy] for optimization.

## Literature

* Hammer, B. & Hasenfuss, A. (2007). Relational Neural Gas. Proceedings of the
    30th Annual German Conference on AI (KI 2007), 190-204. doi:[10.1007/978-3-540-74565-5_16](https://doi.org/10.1007/978-3-540-74565-5_16). [Link][Ham2007]
* Hammer, B., Hofmann, D., Schleif, F., & Zhu, X. (2014). Learning vector
    quantization for (dis-)similarities. Neurocomputing, 131, 43-51.
    doi:[10.1016/j.neucom.2013.05.054](https://doi.org/10.1016/j.neucom.2013.05.054). [Link][Ham2014]
* Nebel, D., Hammer, B., Frohberg, K., & Villmann, T. (2015). Median variants
    of learning vector quantization for learning of dissimilarity data.
    Neurocomputing, 169, 295-305. doi:[10.1016/j.neucom.2014.12.096][Neb2015]

<!-- References -->

[scikit]: https://scikit-learn.org/stable/ "Scikit-learn homepage"
[np]: http://numpy.org/ "Numpy homepage"
[scipy]: https://scipy.org/ "SciPy homepage"
[GPLv3]: https://www.gnu.org/licenses/gpl-3.0.en.html "The GNU General Public License Version 3"
[Ham2007]:https://www.researchgate.net/publication/221562215_Relational_Neural_Gas "Hammer, B. & Hasenfuss, A. (2007). Relational Neural Gas. Proceedings of the 30th Annual German Conference on AI (KI 2007), 190-204. doi:10.1007/978-3-540-74565-5_16"
[Ham2014]:http://www.techfak.uni-bielefeld.de/~fschleif/pdf/nc_diss_2014.pdf "Hammer, B., Hofmann, D., Schleif, F., & Zhu, X. (2014). Learning vector quantization for (dis-)similarities. Neurocomputing, 131, 43-51. doi:10.1016/j.neucom.2013.05.054"
[Neb2015]:https://doi.org/10.1016/j.neucom.2014.12.096 "Nebel, D., Hammer, B., Frohberg, K., & Villmann, T. (2015). Median variants of learning vector quantization for learning of dissimilarity data. Neurocomputing, 169, 295-305. doi:10.1016/j.neucom.2014.12.096"