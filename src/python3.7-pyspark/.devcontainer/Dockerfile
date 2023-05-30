FROM mcr.microsoft.com/devcontainers/base:${templateOption:imageVariant}
# FROM mcr.microsoft.com/devcontainers/base:jammy 

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode

RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update \ 
    && apt-get install -y build-essential --no-install-recommends make \
        ca-certificates \
        git \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        wget \
        curl \
        llvm \
        libncurses5-dev \
        xz-utils \
        tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libffi-dev \
        liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the root Zscaler certificate
RUN mkdir /usr/local/share/ca-certificates/custom-ca
COPY --chmod=600 ZscalerRootCertificate-2048-SHA256.crt /usr/local/share/ca-certificates/custom-ca/
RUN update-ca-certificates

# Python and poetry installation
USER $USER
ARG HOME="/home/$USER"
ARG PYTHON_VERSION=${templateOption:pythonVersion}
ARG PYTHON_PYSPARK_VERSION=3.7.16
# ARG PYTHON_VERSION=3.10

ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${HOME}/.local/bin:$PATH"

# Pythons
RUN echo "done 0" \
    && curl https://pyenv.run | bash \
    && echo "done 1" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "done 2" \
    && pyenv global ${PYTHON_VERSION} \
    && echo "done 3" \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true \
    && echo "done 4" \
    && pip3 install "dvc[s3]" pre-commit \
    && echo "done 5" \
    && pyenv install ${PYTHON_PYSPARK_VERSION} \
    && echo "done 6." 

# Java & Spark
ARG JAVA_VERSION=17.0.7-tem
ARG SBT_VERSION=1.8.3
ARG SPARK_VERSION=3.3.1
RUN curl -s "https://get.sdkman.io" | bash \
    && bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && sdk install java ${JAVA_VERSION} && sdk install sbt ${SBT_VERSION}"
#    && wget -O- https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz --no-check-certificate | tar xvz -C $HOME

# Install cert file in python
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
COPY install_certs_python.py $HOME/install_certs_python.py
RUN $HOME/.pyenv/versions/${PYTHON_VERSION}/bin/python3 $HOME/install_certs_python.py
RUN $HOME/.pyenv/versions/${PYTHON_PYSPARK_VERSION}/bin/python3 $HOME/install_certs_python.py