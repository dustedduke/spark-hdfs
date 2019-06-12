#!/bin/bash

N=$1

sudo chmod +x init-hadoop.sh
sudo chmod +x start-master.sh
sudo chmod +x start-worker.sh

docker network create --driver bridge sparkNet
docker-compose up -d --scale spark-worker=$N

#docker run -v `pwd`:/data --name hadoop --hostname hadoop --network sparkNet -p 50070:50070 -p 9000:9000 -p 50075:50075 -p 50010:50010 #teivah/hadoop:2.9.2
docker exec -it hadoop-hdfs data/init-hadoop.sh

docker run -it -e SPARK_MASTER="spark://spark-master:7077" -e PYSPARK_PYTHON=/usr/bin/python3.6 -v `pwd`:/local --network sparkNet dustedduke/spark:latest /bin/bash








