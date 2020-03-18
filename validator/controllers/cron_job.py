from validator.controller import Controller
from kubernetes.client.models.v1beta1_cron_job import V1beta1CronJob

__all__ = ["CronJobController"]


class CronJobController(Controller):
    def __init__(self, res: V1beta1CronJob):
        self.name = res.metadata.name
        self.namespace = res.metadata.namespace
        self.resource = res

    @property
    def pod_template(self):
        return self.resource.spec.job_template.spec.template

    @property
    def pod_spec(self):
        return self.resource.spec.job_template.spec.template.spec

    @property
    def annotations(self):
        return self.resource.metadata.annotations

    @property
    def type(self):
        return "CronJobController"
