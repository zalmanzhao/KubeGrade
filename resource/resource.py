from datetime import datetime
from kubernetes import client, config

__all__ = ["KubernetesResource", "fetch_kubernetes_resource"]


class KubernetesResource:
    def __init__(self):
        self.version = None
        self.fetch_time = None
        self.nodes = []
        self.deployments = []
        self.stateful_sets = []
        self.daemon_sets = []
        self.jobs = []
        self.cron_jobs = []
        self.replication_controllers = []
        self.namespaces = []
        self.pods = []


def fetch_pods():
    api = client.CoreV1Api()
    return api.list_pod_for_all_namespaces().items


def fetch_namespaces():
    api = client.CoreV1Api()
    return api.list_namespace().items


def fetch_nodes():
    api = client.CoreV1Api()
    return api.list_node().items


def fetch_replication_controllers():
    api = client.CoreV1Api()
    return api.list_replication_controller_for_all_namespaces().items


def fetch_corn_jobs():
    api = client.BatchV1beta1Api()
    return api.list_cron_job_for_all_namespaces().items


def fetch_jobs():
    api = client.BatchV1Api()
    return api.list_job_for_all_namespaces().items


def fetch_daemon_sets():
    api = client.AppsV1Api()
    return api.list_daemon_set_for_all_namespaces().items


def fetch_stateful_sets():
    api = client.AppsV1Api()
    return api.list_stateful_set_for_all_namespaces().items


def fetch_deployments():
    api = client.AppsV1Api()
    return api.list_deployment_for_all_namespaces().items


def fetch_kubernetes_version():
    api = client.VersionApi()
    version = "{}.{}".format(api.get_code().major, api.get_code().minor)
    return version


def fetch_kubernetes_resource():
    config.load_kube_config()
    result = KubernetesResource
    result.version = fetch_kubernetes_version()
    result.deployments = fetch_deployments()
    result.stateful_sets = fetch_stateful_sets()
    result.daemon_sets = fetch_daemon_sets()
    result.jobs = fetch_jobs()
    result.cron_jobs = fetch_corn_jobs()
    result.replication_controllers = fetch_replication_controllers()
    result.nodes = fetch_nodes()
    result.namespaces = fetch_namespaces()
    result.pods = fetch_pods()
    result.fetch_time = datetime.now()
    return result
