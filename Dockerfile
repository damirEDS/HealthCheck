FROM python:3.8.13-slim-buster

ENV http_proxy=http://erg-krb.group.erg.kz:8080 \
    https_proxy=http://erg-krb.group.erg.kz:8080 \
    no_proxy=erg.kz,localhost \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
  && apt-get -y install libpq-dev netcat gcc && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

#Fix openssl default security level
RUN sed -i "s/CipherString = DEFAULT@SECLEVEL=2/CipherString = DEFAULT@SECLEVEL=1/g" /etc/ssl/openssl.cnf

# COPY ./ssl_cert/erg_ca.crt /usr/local/share/ca-certificates
# RUN update-ca-certificates


COPY requirements.txt .
RUN pip install --upgrade pip &&  pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade --no-cache-dir -r requirements.txt

COPY . .
WORKDIR /Health_Check


CMD ["python", "/Health_Check/Health_check.py"]

