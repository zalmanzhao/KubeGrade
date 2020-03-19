import logging
import threading

from validator.kube.resource import KubernetesResourceProvider
from .base import NamespaceResult, NamespaceInfo
from .controller import validate_controllers

__all__ = ["validate_namespaces"]

log = logging.getLogger("namespace validator")


def validate_namespace_resource(namespace, provider, results):
    namespace_resource = provider.fetch_namespaced_kubernetes_resource(namespace)
    controller_results = validate_controllers(namespace_resource)
    result = NamespaceResult(
        name=namespace,
        controller_results=controller_results
    )
    results.append(result)


def validate_namespaces(provider: KubernetesResourceProvider):
    namespaces = provider.fetch_namespaces()
    results = []
    pool = []
    for namespace in namespaces:
        namespace_name = namespace.metadata.name
        t = threading.Thread(target=validate_namespace_resource, args=(namespace_name, provider, results))
        t.start()
        pool.append(t)
        for t in pool:
            t.join()
    return results
