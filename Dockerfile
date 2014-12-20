FROM  ubuntu:14.04
RUN sudo apt-get update
RUN sudo apt-get install -y python python-flask
RUN sudo apt-get install -y ipython python-flake8 pychecker python-requests python-doit
RUN sudo apt-get install -y vim
EXPOSE 5000
VOLUME ["/src"]
COPY . /src
WORKDIR /src
