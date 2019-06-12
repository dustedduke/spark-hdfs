# spark-hdfs

## Usage 

Terminal 1
```bash
./startCluster <number of workers>
```

Terminal 2
```bash
docker exec -it hadoop-hdfs /bin/bash
hadoop fs -put data/data/ /data
```

Terminal 1
```bash
spark/bin/spark-submit --driver-memory 4g --executor-memory 3g --master spark://spark-master:7077 /local/scripts/500.py NASA_access_log_Aug95.gz NASA_access_log_Jul95.gz
```

## Results
```bash
http://localhost:50070/explorer.html#/log500.csv
http://localhost:50070/explorer.html#/time_series.csv
http://localhost:50070/explorer.html#/window.csv
```
