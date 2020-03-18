import logging
from typing import List
from resource.resource import KubernetesResource
from .base import ControllerResult, NamespaceResult, ClusterInfo, ClusterResult
from .controller import validate_controllers

log = logging.getLogger("validator")


def run_validate(resource: KubernetesResource):
    ctrls_result = validate_controllers(resource)
    aggregated_ns = __aggregate_by_namespace(ctrls_result, resource.namespaces)
    cluster_info = ClusterInfo(resource)
    cr = ClusterResult(cluster_info=cluster_info, namespace_results=aggregated_ns)
    return cr


def __aggregate_by_namespace(ctrl_results: List[ControllerResult], namespaces):
    ns_map = {}
    list_values = []
    for n in namespaces:
        n = n.metadata.name
        nr = NamespaceResult(name=n)
        for ctrl_result in ctrl_results:
            if ctrl_result.namespace == n:
                nr.append_controller_result(ctrl_result)
        ns_map[n] = nr
        list_values = [i for i in ns_map.values()]
    return list_values
