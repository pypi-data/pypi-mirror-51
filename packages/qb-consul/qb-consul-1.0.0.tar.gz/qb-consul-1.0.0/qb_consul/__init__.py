# -*- coding:utf-8 -*-
import consul
from random import randint


class Consul:
    def __init__(self, host, port):
        """
        初始化，连接consul服务器
        """
        self._consul = consul.Consul(host, port)

    def register_service(self, name, service_id, host, port, tags=None):
        tags = tags or []
        # 注册服务
        self._consul.agent.service.register(
            name,
            service_id,
            host,
            port,
            tags,
            # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：None
            check=consul.Check().tcp(host, port, "5s", "30s", None))

    def get_service(self, name):
        # services = self._consul.agent.services()
        services = self._consul.health.service(name)
        service_list = []  # 服务列表 初始化

        service_list_data = services[1]

        for _sd in service_list_data:
            address = _sd.get('Service').get('Address')
            port = _sd.get('Service').get('Port')
            service_list.append({'port': port, 'address': address})
        if len(service_list) == 0:
            raise Exception('no service can be used')
        else:
            service = service_list[randint(0, len(service_list) - 1)]  # 随机获取一个可用的服务实例
            return service['address'], int(service['port'])
