# Adevinta Yapo BI Configuration

This microservices contain the python class conf. This class enable read configuration file getting the variables for connect to different data source such as Blocket, DataWarehouse and payment and delivery.

## Usage

For publish python package, you must be do the following commands

```
docker build -t adevinta.yapo.bi.configuration .
```

Later you must be do download package in your develop enviroment.

````
pip install -I adevinta_yapo_bi_configuration
python
>>> from adevinta_yapo_bi_configuration import conf
````
