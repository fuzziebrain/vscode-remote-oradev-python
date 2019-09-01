FROM oraclelinux:7-slim
LABEL MAINTAINER="Adrian Png <adrian.png@fuzziebrain.com>"

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG RELEASE=19
ARG UPDATE=3

RUN yum install -y \
        tar \
        gzip \
        sudo \
        git \
        oracle-release-el7 && \
    yum-config-manager --enable ol7_oracle_instantclient && \
    yum install -y \
        oracle-instantclient${RELEASE}.${UPDATE}-basic \
        oracle-instantclient${RELEASE}.${UPDATE}-devel \
        oracle-instantclient${RELEASE}.${UPDATE}-sqlplus \
        python3 \
        python3-pip && \
    rm -rf /var/cache/yum && \
    groupadd --gid $USER_GID $USERNAME && \
    mkdir -p /home/$USERNAME && \
    chown $USER_UID:$USER_GID /home/$USERNAME && \
    useradd -m -d /home/vscode -s /bin/bash --uid $USER_UID --gid $USER_GID $USERNAME && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    python3 -m pip install \
        pylint \
        cx_Oracle \
        --upgrade

USER ${USERNAME}