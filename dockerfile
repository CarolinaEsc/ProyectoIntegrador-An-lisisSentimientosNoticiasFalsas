FROM ubuntu:latest
MAINTAINER  Carolina 
MAINTAINER  Andrea
MAINTAINER  Michael cgm0026431@gmail.com
RUN apt-get update
RUN apt-get install bash -y
RUN apt install python3 -y
Run apt-get install python3-pip -y
Run apt-get install python3 python3-wheel -y
RUN apt-get install wget -y
Run pip install pyspark
Run pip install findspark
RUN pip install wheel
RUN pip install emoji==1.5.0
Run pip install tweepy
RUN pip install pandas
Run apt install default-jdk -y
Run pip install -U textblob
RUN spark-shell
RUN wget -O aconda.sh https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
#RUN bash aconda.sh Ejecutar este comando dentro de ubuntu para acabar la instalacion
copy resources /home/resources/
#RUN wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh 
#RUN bash Anaconda3-2021.05-Linux-x86_64.sh

#RUN pip install python-csv Instalar dentro de ubuntu

