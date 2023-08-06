================
django-paginator
================

Simple Django Paginator

Installation
============

::

    pip install django-paginator2


Usage
=====

::

    In [1]: from paginator import pagination

    In [2]: pagination(range(100), 1)
    Out[2]: ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 1)

    In [3]: pagination(range(100), 1, strict=True)
    Out[3]: ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 90)

    In [4]: pagination(range(100), 1, 20, strict=True)
    Out[4]: ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 80)

