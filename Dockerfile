FROM jupyter/base-notebook:python-3.11

LABEL maintainer="Adrian Alvarez - HITL <sdadrianalvarez@gmail.com>"
LABEL description="HITL Lab - Multi-cloud AI demos con cobertura ISO 27001/42001/22301"
LABEL version="1.0.0"

USER root

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# Dependencias Python
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copiar adapters al path de Python
COPY adapters/ /home/jovyan/adapters/

# Jupyter config — sin browser, acepta conexiones externas
RUN jupyter lab --generate-config && \
    echo "c.ServerApp.ip = '0.0.0.0'" >> /home/jovyan/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.open_browser = False" >> /home/jovyan/.jupyter/jupyter_lab_config.py

WORKDIR /home/jovyan

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
