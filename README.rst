Base Runtime
============

.. image:: https://travis-ci.org/haowen-xu/base-runtime.svg?branch=master
    :target: https://travis-ci.org/haowen-xu/base-runtime

This is a Ubuntu 16.04 Docker image with various runtime.

Major Packages
--------------

* Python 3.6
* R Language
* OpenJDK 11
* CUDA 9.0 + CUDNN 7 (for GPU variant)
    
Development
-----------

We have two variants of Dockerfiles, the CPU variant (without CUDA) and the GPU variant (with CUDA).
To populate the Dockerfiles of both variants, execute the following command::

    pip install jinja2
    python Dockerfile.py

Installation
------------

::

    # build the cpu image
    docker build -t ipwx/base-runtime:gpu cpu

    # build the gpu image
    docker build -t ipwx/python3-ml:gpu gpu
