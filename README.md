# DataStreamAnalytics
Our peoject integrates Kubernetes (K8s), Fission for serverless functions, Kafka, and Elasticsearch for handling real-time data and analytics

### Package environment_extract_load
- we are using EPA provided API , fetch the real time data of Air quality data comes 
directly from air monitoring stations operated by the EPA.
- we are doing simple transformations and load into Elastic Search Index  : Environmental
- Below are the commands we used to deploy our package to Fission 
``` 
(
  cd fission_functions
  fission specs init
)  
(
  cd fission_functions
  fission env create --spec --name python --image fission/python-env --builder fission/python-builder
  fission env create --spec --name nodejs --image fission/node-env --builder fission/node-builder
)  
(
  cd fission_functions/air_quality_extract_load
  zip -r airextract.zip .
  mv airextract.zip ../
)

(
  cd fission_functions
  fission package create  --spec --sourcearchive ./airextract.zip\
  --env python\
  --name airextract\
  --buildcmd './build.sh'

fission fn create --spec --name airextract\
  --pkg airextract\
  --env python\
  --entrypoint "airextract.main"
)


(
cd fission_functions
fission spec apply --specdir specs --wait
)
```