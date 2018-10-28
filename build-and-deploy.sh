#!/bin/bash

VARIANT="$1"
if [[ "x${VARIANT}" = "x" ]]; then
    echo "build-and-deploy.sh cpu|gpu"
    exit -1
fi

MESOS=mesos1.7
PYTHON=python3.6
JDK=openjdk8
if [[ "x${MAKE_ARGS}" = "x" ]]; then
    MAKE_ARGS=-j8
fi
REPO="haowenxu/base-runtime"
TAG="${VARIANT}"
TAG2="${VARIANT}-${MESOS}-${PYTHON}-${JDK}"

WORK_DIR=/tmp/$(python -c "import uuid; print('docker-build-{}'.format(uuid.uuid4()))")
mkdir -p ${WORK_DIR} && \
    cp -R . ${WORK_DIR} && \
    cd ${WORK_DIR} && \
    pip install --user -r requirements.txt && \
    python configure.py -c "config/${VARIANT}.yml" -c "config/${MESOS}.yml" -c "config/${PYTHON}.yml" -c "config/${JDK}.yml" && \
    docker build -t "${REPO}:${TAG}" --build-arg MAKE_ARGS="${MAKE_ARGS}" . && \
    docker tag "${REPO}:${TAG}" "${REPO}:${TAG2}" && \
    docker login -u "${DOCKER_USER}" -p "${DOCKER_PASS}" && \
    docker push "${REPO}:${TAG}" && \
    docker push "${REPO}:${TAG2}"
