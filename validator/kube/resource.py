from datetime import datetime
from kubernetes import client
from kubernetes.client import ApiClient

__all__ = ["NamespaceKubernetesResource", "KubernetesResourceProvider"]


class NamespaceKubernetesResource:
    def __init__(self, namespace):
        super().__init__()
        self.namespaces = namespace
        self.deployments = []
        self.stateful_sets = []
        self.daemon_sets = []
        self.jobs = []
        self.cron_jobs = []
        self.pods = []


class KubernetesResourceProvider():
    def __init__(self, host, token):
        configuration = client.Configuration()
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.api_key['authorization'] = token
        configuration.host = "https://{}:6443".format(host)
        configuration.verify_ssl = False
        configuration.debug = False
        self.client = ApiClient(configuration)

    def fetch_namespaced_kubernetes_resource(self, namespace):
        result = NamespaceKubernetesResource(namespace)
        result.version = self.fetch_kubernetes_version()
        result.fetch_time = datetime.now()
        result.deployments = self.fetch_deployments(namespace)
        result.stateful_sets = self.fetch_stateful_sets(namespace)
        result.daemon_sets = self.fetch_daemon_sets(namespace)
        result.jobs = self.fetch_jobs(namespace)
        result.cron_jobs = self.fetch_corn_jobs(namespace)
        result.pods = self.fetch_pods(namespace)
        return result

    def fetch_namespaces(self):
        api = client.CoreV1Api(self.client)
        return api.list_namespace().items

    def fetch_nodes(self):
        api = client.CoreV1Api(self.client)
        return api.list_node().items

    def fetch_kubernetes_version(self):
        api = client.VersionApi(self.client)
        version = "{}.{}".format(api.get_code().major, api.get_code().minor)
        return version

    def fetch_pods(self, ns=None):
        api = client.CoreV1Api(self.client)
        if not ns:
            result = api.list_pod_for_all_namespaces().items
        else:
            result = api.list_namespaced_pod(ns).items
        return result

    def fetch_corn_jobs(self, ns=None):
        api = client.BatchV1beta1Api(self.client)
        if not ns:
            result = api.list_cron_job_for_all_namespaces().items
        else:
            result = api.list_namespaced_cron_job(ns).items
        return result

    def fetch_jobs(self, ns=None):
        api = client.BatchV1Api(self.client)
        if not ns:
            result = api.list_job_for_all_namespaces().items
        else:
            result = api.list_namespaced_job(ns).items
        return result

    def fetch_daemon_sets(self, ns=None):
        api = client.AppsV1Api(self.client)
        if not ns:
            result = api.list_daemon_set_for_all_namespaces().items
        else:
            result = api.list_namespaced_daemon_set(ns).items
        return result

    def fetch_stateful_sets(self, ns=None):
        api = client.AppsV1Api(self.client)
        if not ns:
            result = api.list_stateful_set_for_all_namespaces().items
        else:
            result = api.list_namespaced_stateful_set(ns).items
        return result

    def fetch_deployments(self, ns=None):
        api = client.AppsV1Api(self.client)
        if not ns:
            result = api.list_deployment_for_all_namespaces().items
        else:
            result = api.list_namespaced_deployment(ns).items
        return result
