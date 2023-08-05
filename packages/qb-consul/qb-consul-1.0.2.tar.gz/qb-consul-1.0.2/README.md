## Introduce to qb-consul

version: 1.0.2

how to install:

pip install qb-consul


If you want to use it locally:
```
from qb_consul import Consul


host = "127.0.0.1"  # consul服务器的ip
port = 8500  # consul服务器对外的端口
consul_client = Consul(host, port)

# register service
name = "qbzz-server"
host1 = "127.0.0.1"
port1 = 8001
service_id = "qbzz-server-%s" % port1
consul_client.register_service(name, service_id, host1, port1)

# get service
message = consul_client.get_service('qbzz-server')
host = message[0]
port = message[1]



```