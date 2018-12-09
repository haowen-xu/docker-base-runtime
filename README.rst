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
   * Python 2.7: `/usr/bin/python2.7`
   * Python 3.6: `/usr/local/bin/python3.6`
   * R Language: `/usr/bin/R`
   * OpenJDK 8: `/usr/lib/jvm/java-8-openjdk-amd64/bin/java`
   * Scala 2.11: `/usr/bin/scala`
   * SBT

Also, `/usr/local/bin/python` is linked to `/usr/local/bin/python3.6`, while
`/usr/bin/python` is linked to `/usr/bin/python2.7`.  The default Python
interpreter is thus Python 3.6.

Installation
------------

Generate the Dockerfile
~~~~~~~~~~~~~~~~~~~~~~~

We use `configure.py` to generate the Dockerfile according to configurations.

You should first install the dependencies of `configure.py`::

    pip install -r requirements.txt

Then for example, you can use the following statement to generate the CPU
variant Dockerfile::

    python configure.py \
        -c config/cpu.yml \
        -c config/mesos1.7.yml \
        -c config/python3.6.yml \
        -c config/openjdk8.yml \
        -c config/scala2.11.yml

Build the Docker Image
~~~~~~~~~~~~~~~~~~~~~~

After generate the Dockerfile, you can build the docker image by::

    docker build --build-arg MAKE_ARGS=-j4 .

Usage
-----

The basic usage of this docker image is shown as below.
Note that you may specify the `TZ` environmental variable, such that the
container will have the correct timezone::

    docker run \
        -ti --rm -e TZ=Asia/Shanghai \
        haowenxu/base-runtime:cpu \
        /bin/bash
