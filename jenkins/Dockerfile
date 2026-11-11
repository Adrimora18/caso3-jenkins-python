FROM jenkins/jenkins:lts-jdk21

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         python3 python3-venv python3-pip git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /opt/despliegue \
    && chown -R jenkins:jenkins /opt/despliegue

USER jenkins
COPY --chown=jenkins:jenkins plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
