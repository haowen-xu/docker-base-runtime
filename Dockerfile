FROM ubuntu:16.04

MAINTAINER Haowen Xu <haowen.xu@outlook.com>

ARG PYTHON_VERSION=3.6.6
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PIP_DEFAULT_TIMEOUT=120
ENV SHELL=/bin/bash


ENV RUNTIME_VARIANT="cpu"


# do configuration and update packages
RUN chsh -s /bin/bash && \
    mkdir -p /var/run/sshd && \
    DEBIAN_FRONTEND=noninteractive apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        apt-utils apt-transport-https lsb-release openssl gnupg dirmngr software-properties-common \
        build-essential ca-certificates wget git mercurial \
        locales language-pack-en tzdata vim ssh \
        libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
        libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev \
        libnlopt-dev libpq-dev libffi-dev libcairo-dev libedit-dev \
    && \
    add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -c -s)/" && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9 && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-overwrite" \
        install -y --no-install-recommends openjdk-9-jdk \
    && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        r-base r-base-dev maven \
    && \
    wget -O /tmp/Python-${PYTHON_VERSION}.tgz https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz  && \
        cd /tmp && tar -xzvf Python-${PYTHON_VERSION}.tgz && \
        cd Python-${PYTHON_VERSION} && \
        ./configure --enable-optimizations && \
        make -j8 && \
        make altinstall && \
        rm /tmp/Python-${PYTHON_VERSION}.tgz && \
        rm -rf /tmp/Python-${PYTHON_VERSION} && \
    ln -sf /usr/local/bin/python3.6 /usr/bin/python && \
    ln -sf /usr/local/bin/pip3.6 /usr/bin/pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python --version && \
    python -m pip --version && \
    python -m pip install --no-cache-dir --upgrade setuptools pip six && \
    python -m pip install --no-cache-dir rpy2 && \
    rm -rf /root/.cache

# Install the entry script
ADD entry.sh /entry.sh
CMD ["/entry.sh"]