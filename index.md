---
layout: home
---

The JuliaFEM project develops open-source software for reliable, scalable,
distributed Finite Element Method.

The JuliaFEM software library is a framework that allows for the distributed
processing of large Finite Element Models across clusters of computers using
simple programming models. It is designed to scale up from single servers to 
thousands of machines, each offering local computation and storage. The basic 
design principle is: everything is nonlinear. All physics models are nonlinear 
from which the linearization are made as a special cases. 

## Initial road map

JuliaFEM current status: **project planning**

| Version | Number of degree of freedom | Number of cores |
| ------: | --------------------------: | --------------: |
|   0.1.0 |                   1 000 000 |              10 |
|   0.2.0 |                  10 000 000 |             100 |
|   1.0.0 |                 100 000 000 |           1 000 |
|   2.0.0 |               1 000 000 000 |          10 000 |
|   3.0.0 |              10 000 000 000 |         100 000 |

We strongly believe in the test driven development as well as building on top
of previous work. Thus all the new code in this project should be 100% tested.
Also other people have wisdom in style as well:

[The Zen of Python](https://www.python.org/dev/peps/pep-0020/):

```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Errors should never pass silently.
```

## Contributing

Interested in participating? Please start by reading [CONTRIBUTING]({{ site.baseurl }}{% link contributing.md %}).

## Installing packages

Installing packages to Julia is done

```julia
Pkg.add("<package name>")
```

Testing is done

```julia
Pkg.test("<package name>")
```

`JuliaFEM.jl` is the main package and rest are supporting packages, so you get
everything installed by typing `Pkg.add("JuliaFEM")`. The easiest way to evaluate
packages is probably [www.juliabox.org](JuliaBox), so you don't have to install
on a local machine anything in order to test functionality of packages.
