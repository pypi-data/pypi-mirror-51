# catscii

[![DOI](https://zenodo.org/badge/125589988.svg)](https://zenodo.org/badge/latestdoi/125589988)

**catscii** is a very simple python module that allows one to extract in a very easy way columns or line from ascii catalogs. 


Installation
============

catscii is currently placed in the pypi test repository.
To install it 

    pip install -i https://test.pypi.org/simple/ catscii

The only dependency is numpy.

How to
======

Once you installed it you can get started importing the module:

    from catscii import catscii 


**1-Catalogs with header**

Then you must load your ascii catalog. For the purpose of this short tutorial we take a very easy catalog called *test_catscii.txt*: 

    #A	 B	C	D 
    X	 11	12	13 
    Y	 15	15	15 
    Z	 17	15	12


To read the catalog you must create a catalog with the **load_cat** class:

    >>cat = catscii.load_cat('test_catscii.txt', 'yes') 

The first argument is the name of your catalog, and the second tells if there is a proper header. A proper header is when each columns has a name and starts with a '#' symbol (see the example above). The catalog as some interesting attributes, like header or the catalog itself, number of columns/rows.

    >>cat.header
      ['A', 'B', 'C', 'D']

    >>cat.cat
    array([['X', 'Y', 'Z'],
       ['11', '15', '17'],
       ['12', '15', '15'],
       ['13', '15', '12']], dtype='<U2')

    >>cat.Nrows
    3

    >>cat.Ncolumns
    4


By default, the catalog is extracted with a string format. After you can extract columns calling the get_column method with:

    >>cat.get_column('A') 
    array(['11', '15', '17'], dtype='<U2')

By default the column is extracted in string format. If you want another type you can precise it like this:

    >>cat.get_column('B', 'int')
    array([11, 15, 17])


To extract a line you must use the get_line method. You have to give a given column and a given value in that column (as a string):

    >> cat.get_line('A', 'X')
    [{'A': 'X', 'B': '11', 'C': '12', 'D': '13'}]

It returns a list dictionnaries of key/value corresponding to column_name/value. In the case you have multiple line with the same value for a given column, the list will grow:

    >> cat.get_line('C', '15')
    [{'A': 'Y', 'B': '15', 'C': '15', 'D': '15'},
     {'A': 'Z', 'B': '17', 'C': '15', 'D': '12'}]  


Help
====

You can also display the help of the main class like this:

    >> help(catscii.load_cat)
	
Help on class load_cat in module catscii.catscii:

	class load_cat(builtins.object)
	 |  load_cat(catalog, header)
	 |  
	 |  This class creates, from an ascii catalog,
	 |  a python object
	 |  
	 |  Methods defined here:
	 |  
	 |  __init__(self, catalog, header)
	 |      Class constructor
	 |      
	 |      Parameters
	 |      ----------
	 |      catalog : str
	 |                this is the catalog (eventually with its path) you want to open
	 |      
	 |      header  : Boolean
	 |                True if the catalog contains a header, otherwise false
	 |      
	 |      Attributes
	 |      ----------
	 |      name    : str
	 |                Name of the catalog, as passed by the user
	 |      
	 |      cat     : numpy array
	 |                numpy array loaded from the catalog (all columns are string by default)
	 |      
	 |      header  : list of string
	 |                identification of each column. If no header is present in the catalog
	 |                then each column are renames col1, col2, ....colN
	 |      
	 |      Note
	 |      ----
	 |      For the header of the catalog to be recognized, it must start by an hash (#)
	 |      and provide a name for EVERY column Ex:
	 |      #X     Y   Xerrp   Xerrm   Yerrp   Yerrm
	 |      1       1   0.5     0.2     0.3     0.1
	 |      2       2   0.3     0.2     0.1     0.4
	 |      3      3   0.1     0.05    0.1     0.4
	 |      4      4   0.1     0.07    0.8     0.2
	 |      5      5   0.2     0.3     0.15    0.23
	 |      6      6   0.1     0.4     0.6     0.1
	 |      7      7   0.2     0.3     0.4     0.1
	 |  
	 |  get_column(self, name, datatype=None)
	 |      This method extracts the column given by the name in the parameter
	 |      from the loaded catalog.
	 |      
	 |      Parameters
	 |      ----------
	 |      name
	 |              str,  name of the column to extract
	 |      
	 |      datatype
	 |              str, optionnal, give the datatype of the column
	 |      
	 |      return
	 |      ------
	 |      column
	 |              numpy array, 1D numpy array of the column that 
	 |                           was extracted.
	 |  
	 |  get_line(self, column, line, datatype='None')
	 |      This method extract the line given in parameters
	 |      
	 |      Parameters
	 |      ----------
	 |      column
	 |              string, column where to look at for line identification
	 |      
	 |      line
	 |              string, in the given column, we will extract the line(s) where the value is
	 |      
	 |      
	 |      Return
	 |      ------
	 |      extracted_line
	 |                      list of dictionnary
	 |                      each dictionnary correspond to a line where the column given
	 |                      by the user is equal to the line value that was passed.
	 |                      The keywords of each dictionnary are the names of the column and the values
	 |                      are the values at the requested line
	 |  
	 |  ----------------------------------------------------------------------






Contribute
==========
If you want to contribute to catscii please drop me a mail [the.spartan.proj@gmail.com]


Citation
========
If you are willing to cite catscii please use: 

	@misc{catscii,
	  author    = {Thomas ,R},
	  title		= {catscii v1.2, 10.5281/zenodo.2587874}, 
	  version   = {1.2},
	  publisher = {Zenodo},
	  month     = March,
	  year      = 2019,
	  doi       = {10.5281/zenodo.2587874},
	  url       = {https://doi.org/10.5281/zenodo.2587874}
	}

