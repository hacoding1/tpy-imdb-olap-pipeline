# tpy-imdb-olap-pipeline



docker compose build --no-cache

docker images

docker compose up -d 
docker compose down -v

docker ps 

docker log spark-master
docker log spark-worker-1
docker log spark-worker-2

UI - http://localhost:8080 

docker exec -it spark-master bash
whoami 
python --version 
pip freeze 
spark-submit --version

import pyspark
print(pyspark.__version__)
exit()


