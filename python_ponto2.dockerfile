FROM python
# MAINTAINER Samuel Thomaz
# RUN mkdir /var/controle_funcionarios_obras
COPY ./configfiles/python/requirements.txt /var/.
WORKDIR /var/controle_funcionarios_obras
RUN pip install -r /var/requirements.txt
# ENV ponto=2
