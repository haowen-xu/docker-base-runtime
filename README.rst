Base Runtime
============

.. image:: https://travis-ci.org/haowen-xu/base-runtime.svg?branch=master
    :target: https://travis-ci.org/haowen-xu/base-runtime

This is a Ubuntu 16.04 Docker image with various runtime.

Major Packages
--------------

* Variants:
   * CPU variant: based on official Ubuntu 16.04 image
   * GPU variant: based on Nvidia Ubuntu 16.04 image, with CUDA and CUDNN
* Installed packages:
   * Mesos
   * Python
   * R Language
   * OpenJDK

Generate the Dockerfile
-----------------------

We use `configure.py` to generate the Dockerfile according to configurations.

You should first install the dependencies of `configure.py`::

    pip install -r requirements.txt

Then for example, you can use the following statement to generate the CPU
variant Dockerfile::

    python configure.py \
        -c config/cpu.yml \
        -c config/mesos1.7.yml \
        -c config/python3.6.yml \
        -c config/openjdk9.yml

Build the Docker Image
----------------------

After generate the Dockerfile, you can build the docker image by::

    docker build --build-arg MAKE_ARGS=-j4 .
