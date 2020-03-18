from validator.controller import Controller
from kubernetes.client.models.v1_daemon_set import V1DaemonSet

__all__ = ['DaemonSetController']


class DaemonSetController(Controller):
    def __init__(self, res: V1DaemonSet):
        self.name = res.metadata.name
        self.namespace = res.metadata.namespace
        self.resource = res

    @property
    def pod_template(self):
        return self.resource.spec.template

    @property
    def pod_spec(self):
        return self.resource.spec.template.spec

    @property
    def annotations(self):
        return self.resource.metadata.annotations

    @property
    def type(self):
        return "DaemonSets"
