Base Runtime
============

This is a Ubuntu Docker image with various runtime.

Major Packages
--------------

All the variants can be retrieved at `Docker Hub <https://hub.docker.com/r/haowenxu/base-runtime>`_.

* Variants:
   * CPU variant: based on official Ubuntu image
   * GPU variant: based on Nvidia Ubuntu image, with CUDA and CUDNN
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
        -c config/openjdk8.yml

Build the Docker Image
----------------------

After generate the Dockerfile, you can build the docker image by::

    docker build --build-arg MAKE_ARGS=-j4 .
