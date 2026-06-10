FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Berlin

# Base utilities
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-dev python3-pip \
    git curl wget build-essential \
    software-properties-common gnupg2 lsb-release \
    locales sudo \
    && rm -rf /var/lib/apt/lists/*

# Set locale
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# ROS2 Humble
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
      -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
      http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
      > /etc/apt/sources.list.d/ros2.list && \
    apt-get update && apt-get install -y ros-humble-desktop && \
    rm -rf /var/lib/apt/lists/*

# LaTeX
RUN apt-get update && apt-get install -y \
    texlive-full latexmk biber \
    && rm -rf /var/lib/apt/lists/*

# Python pip upgrade
RUN python3.10 -m pip install --upgrade pip

# Non-root user
RUN useradd -m -s /bin/bash researcher && \
    echo "researcher ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# ROS2 in bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> /home/researcher/.bashrc

COPY requirements.txt /tmp/requirements.txt
RUN python3.10 -m pip install -r /tmp/requirements.txt

USER researcher
WORKDIR /workspace
