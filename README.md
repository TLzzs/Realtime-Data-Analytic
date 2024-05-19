# DataStreamAnalytics

## Overview
DataStreamAnalytics is a project designed to process and analyze weather and social media data. This project leverages various tools and technologies including Kubernetes, Fission, and Elasticsearch to create a robust data pipeline.

## Repository Structure
- `.github/` - GitHub configuration files.
- `data/` - Data files used in the project.
- `es_index_create/` - Scripts for creating Elasticsearch indices.
- `fission_functions/` - Directory containing Fission functions and specifications.
  - `air_quality_extract_load/` - Functions for extracting and loading air quality data.
  - `http_handlers/` - HTTP handler functions for various endpoints.
  - `mstd_post_extract_load/` - Functions for extracting and loading Mastodon posts.
  - `weather_data_extract_load/` - Functions for extracting and loading weather data.
  - `weather_station_extract_load/` - Functions for extracting and loading weather station data.
  - `specs/` - Fission function specifications.
- `frontend/` - Frontend application files.
- `tests/` - Test cases for the project.

## Fission Functions

### Overview
Fission functions are used to retrieve and process real-time and non-real-time data, which is then indexed into Elasticsearch for further analysis and visualization. The following sections describe each function in detail.

### Air Quality Extract and Load
This function extracts air quality data from various sources and loads it into the Elasticsearch index. The process involves data cleaning, transformation, and enrichment before storing it for analytics.

### HTTP Handlers
These functions handle HTTP requests and act as entry points for the API. They route incoming requests to the appropriate data processing functions and ensure that data is processed and returned to the user in a timely manner.

### Mastodon Post Extract and Load
This function extracts posts from Mastodon, filtered by specific tags, and loads them into the Elasticsearch index `mstd_social_tag_data`. The data is used for sentiment analysis and correlation with crime data.

### Weather Data Extract and Load
This function extracts weather data at specific timestamps for different stations and loads it into the Elasticsearch index `bom_weather_data`. This index supports real-time data analytics and visualization.

### Weather Station Extract and Load
This function extracts information about weather stations, including their locations and other metadata, and loads it into the Elasticsearch index `bom_stations`. This data is crucial for mapping and correlating weather data with specific locations.

### Specifications
The `specs` directory contains the YAML files defining the configurations for Fission functions and environments. Each file describes the function's settings, including minscale and maxscale parameters to ensure optimal performance.

### Indexes
We use the following Elasticsearch indexes for storing and analyzing the data:
- `bom_stations`: Stores information about weather stations.
- `bom_weather_data`: Contains weather data at specific timestamps for different stations.
- `mstd_social_tag_data`: Collects tweets from Mastodon filtered by specific tags.
- `lga`: Reference for mapping LGA codes and suburb names.
- `sudo_au_locations`: Stores non-real-time data from Sudo about Australian locations.
- `sudo_crime`: Contains crime data from Sudo.

### Real-Time Data Processing
For real-time data processing, we utilize Fission functions to retrieve and process data, which is then indexed into Elasticsearch. This setup allows for real-time analytics and visualization through Kibana, directly impacting the project's ability to handle data-driven tasks efficiently.

### Non-Real-Time Data
In addition to real-time data, we process non-real-time data sourced from Sudo, which includes indices such as `sudo_au_locations` and `sudo_crime`. These indices provide historical context and additional insights for comprehensive data analysis.

## How to set up the working environment
1. **install openstack client**
    ```bash
    pip install python-openstackclient
    sudo pip install python-cinderclient
    sudo pip install python-glanceclient
    sudo pip install python-magnumclient
    sudo pip install python-neutronclient
    sudo pip install python-novaclient
    sudo pip install python-swiftclient
   ```
2. **install fission client**
    ```bash
    curl -Lo fission https://github.com/fission/fission/releases/download/v1.20.1/fission-v1.20.1-darwin-amd64 \
    && chmod +x fission && sudo mv fission /usr/local/bin/
    ```
3. **install plugin using brew**
    ``` bash
    brew install jq
    brew install asdf
    ```
4. **install kubectl**
    ```
    asdf plugin add kubectl
    sdf install kubectl 1.26.8
    ```
5. **source your openRC File**
    ```
    source ./<your sh file> 
    ```
6. **port forwarding to master node and pods**
    ```
    ssh -i ~/.ssh/<your private key> -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')
    kubectl port-forward service/kibana-kibana -n elastic 5601:5601
    kubectl port-forward service/router -n fission 9090:80
    kubectl port-forward service/elasticsearch-master -n elastic 9200:9200
    ```
## How to Use
1. **Deploy Fission Functions**:
    Deploy the functions defined in the `specs` directory using Fission CLI commands.

2. **Run the Frontend**:
    Navigate to the `frontend` directory , you will see jupyternode book as our frontend, please run them once you connected to k8s cluster

3. **Access Elasticsearch and Kibana**:
    Ensure Elasticsearch and Kibana are running in your Kubernetes cluster. Access Kibana for data visualization.

