from validator.kube.resource import KubernetesResourceProvider
from validator.base import ClusterResult
from validator.namespace import validate_namespaces


def run_validate(host, token):
    provider = KubernetesResourceProvider(host, token)
    ns = validate_namespaces(provider)
    return ClusterResult(ns)



