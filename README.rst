pySWEETCat
==========
 
A pure-Python package to download data from SWEET-Cat_.

This small package was developed as an exercise in a Python course (see CONTRIBUTORS_).
It downloads all the data from the SWEET-Cat online catalogue of stellar parameters 
and builds a (custom) dictionary with each column. 
It is a pure-Python package with no extra dependencies (see below).


|License MIT| |Travis build| |PyPI version|

How to use
----------

Install it from pip (**pySWEETCat** has no extra depencies)

::

    pip install pySWEETCat

and it's ready to use from Python

.. code:: python

    import pysweetcat


**pySWEETCat** has one simple function, ``get_data()``,
which downloads the data from the online archive and returns it in a dictionary.

.. code:: python

    >>> data = pysweetcat.get_data()

.. code::

    Downloading SWEET-Cat data
    Saved SWEET-Cat data to $HOME/.pysweetcat/SWEET_cat.tsv
    Data in `SWEET_cat.tsv` is recent.
    There are 25 columns with 2627 entries each in `SWEET_cat.tsv`

where ``$HOME`` will  be your home directory.
The second time you call ``get_data()`` it will check if the data was downloaded recently, 
and only conditionally download it again.

.. code:: python

    >>> data = pysweetcat.get_data()

.. code::

    Data in `SWEET_cat.tsv` is recent.
    There are 25 columns with 2627 entries each in `SWEET_cat.tsv`

Now, `data` is (basically) a Python dictionary with the each column as keys.
But it has a couple extra methods and properties. For example

.. code:: python

    data.size
    2627
    
returns the number of values in each column.

The columns can be accessed as in a normal dictionary,
as in 

.. code:: python

    data['feh']   # stellar metallicity
    data['name']  # name of the star


and both of these will work

.. code:: python

    data['σ_vmag']   
    data['sigma_vmag']
    
Also, to drop the NaN values in a column (for some columns there will be quite a few)
we can use

.. code:: python

    data['teff_nonan']
    
    np.isnan(data['teff']).any()       # True
    np.isnan(data['teff_nonan']).any() # False
    

which allows us to more easily do histograms of the values.

Finnally, the ``.to_numpy(inplace=True)`` method converts all the columns to numpy arrays, either in place or not
(this is the only function in **pySWEETCat** that requires numpy).


License
-------

Copyright 2018 João Faria.

**pySWEETCat** is free software made available under the MIT License. For
details see the LICENSE_ file.

.. _SWEET-Cat: https://www.astro.up.pt/resources/sweet-cat/
.. _CONTRIBUTORS: https://github.com/j-faria/pySWEETCat/blob/master/CONTRIBUTORS.md
.. _License: https://github.com/j-faria/pySWEETCat/blob/master/LICENSE
.. |License MIT| image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/j-faria/pySWEETCat/blob/master/LICENSE
.. |Travis build| image:: https://travis-ci.org/j-faria/pySWEETCat.svg?branch=master
    :target: https://travis-ci.org/j-faria/pySWEETCat
.. |PyPI version| image:: https://badge.fury.io/py/pySWEETCat.svg
    :target: https://badge.fury.io/py/pySWEETCat
