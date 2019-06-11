FROM openjdk:8-alpine

RUN apk --update add wget tar bash python3
RUN wget http://apache.mirror.anlx.net/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz
RUN tar -xzf spark-2.4.3-bin-hadoop2.7.tgz && \
    mv spark-2.4.3-bin-hadoop2.7 /spark && \
    rm spark-2.4.3-bin-hadoop2.7.tgz

RUN wget -O /hadoop.tar.gz -q https://iu.box.com/shared/static/u9wy21nev5hxznhuhu0v6dzmcqhkhaz7.gz
RUN tar -xfz hadoop.tar.gz && \
	mv /hadoop-2.7.3 /usr/local/hadoop && \
	rm /hadoop.tar.gz


COPY start-master.sh /start-master.sh
COPY start-worker.sh /start-worker.sh
