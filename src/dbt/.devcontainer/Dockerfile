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
ARG DBT_VERSION=${templateOption:dbtVersion}
ARG DBT_ATHENA_VERSION=${templateOption:dbtAthenaCommunityVersion}

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
    && pip3 install "dbt-core==${DBT_VERSION}" "dbt-athena-community==${DBT_ATHENA_VERSION}"\
    && echo "done 6"

# Install cert file in python
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV AWS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
COPY install_certs_python.py $HOME/install_certs_python.py
RUN $HOME/.pyenv/versions/${PYTHON_VERSION}/bin/python3 $HOME/install_certs_python.py
