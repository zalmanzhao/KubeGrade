from .resource import ResourceValidation
from kubernetes.client.models import V1PodSpec
from validator.config import check_list
from . import messages
from .base import PodResult
from .container import validate_container


class PodValidation(ResourceValidation):

    def __init__(self, pod):
        super().__init__()
        self.pod: V1PodSpec = pod

    def validate_security(self):
        category = messages.CategorySecurity

        def validate_security_host_ipc_set(pv):
            name = "hostIPCSet"
            security_conf = check_list.get("security", None)
            severity = security_conf.get(name, None)
            if pv.pod.host_ipc:
                pv.on_failure(messages.HostIPCFailure, severity, category, name)
            else:
                pv.on_success(messages.HostIPCSuccess, category, name)

        def validate_security_host_pid_set(pv):
            name = "hostPIDSet"
            security_conf = check_list.get("security", None)
            severity = security_conf.get(name, None)
            if pv.pod.host_pid:
                pv.on_failure(messages.HostPIDFailure, severity, category, name)
            else:
                pv.on_success(messages.HostPIDSuccess, category, name)

        validate_security_host_ipc_set(self)
        validate_security_host_pid_set(self)

    def validate_networking(self):
        category = messages.CategoryNetworking
        name = "HostNetworkSet"
        networking_conf = check_list.get("networking", None)
        severity = networking_conf.get(name, None)
        if self.pod.host_network:
            self.on_failure(messages.HostNetworkFailure, severity, category, name)
        else:
            self.on_success(messages.HostNetworkSuccess, category, name)

    def validate_containers(self):
        containers = self.pod.containers
        container_results = []
        for container in containers:
            res = validate_container(container, self.pod)
            container_results.append(res)
        return container_results


def validate_pod(pod: V1PodSpec):
    pv = PodValidation(pod)
    pv.validate_networking()
    pv.validate_security()
    containers_result = pv.validate_containers()
    return PodResult(messages=pv.messages, container_results=containers_result)
