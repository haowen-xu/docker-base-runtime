Base Runtime
============

.. image:: https://travis-ci.org/haowen-xu/base-runtime.svg?branch=master
    :target: https://travis-ci.org/haowen-xu/base-runtime

This is a Ubuntu 16.04 Docker image with various runtime.

Major Packages
--------------

* Python 3.6
* R Language
* OpenJDK 9
* CUDA 9.0 + CUDNN 7 (for GPU variant)

Build Docker Image
------------------

::
    pip install -r requirements.txt

    # build the cpu image
    python configure.py --variant=cpu && docker build -t ipwx/base-runtime:cpu .

    # build the gpu image
    python configure.py --variant=gpu && docker build -t ipwx/base-runtime:gpu .
