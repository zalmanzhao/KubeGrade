import logging

from validator.config import check_list
from validator.kube.resource import NamespaceKubernetesResource
from validator.base import ControllerResult

from validator.pod import validate_pod

log = logging.getLogger("controller")

__supported_controller = ["Deployments",
                          "StatefulSets",
                          "DaemonSets",
                          "Jobs",
                          "CronJobs"]


class Controller:
    name = None
    namespace = None

    @property
    def pod_template(self):
        return

    @property
    def pod_spec(self):
        return

    @property
    def type(self):
        return

    @property
    def annotations(self):
        return


def create_validate_controllers(res: NamespaceKubernetesResource):
    from validator.controllers import DeploymentController, DaemonSetController, JobController, CronJobController, \
        StateSetController
    ctr = []
    _config_ctr = check_list.get("controllers", [])
    for cctr in _config_ctr:
        if not cctr in __supported_controller:
            log.warning("not supported controller: {} skip it".format(cctr))
        else:
            if cctr == 'Deployments':
                for d in res.deployments:
                    ctr.append(DeploymentController(d))
            elif cctr == 'DaemonSets':
                for d in res.daemon_sets:
                    ctr.append(DaemonSetController(d))
            elif cctr == "Jobs":
                for d in res.jobs:
                    ctr.append(JobController(d))
            elif cctr == "CronJobs":
                for d in res.cron_jobs:
                    ctr.append(CronJobController(d))
            elif cctr == "StateSets":
                for d in res.stateful_sets:
                    ctr.append(StateSetController(d))
    return ctr


def validate_controller(c: Controller):
    pod_result = validate_pod(c.pod_spec)
    return ControllerResult(
        name=c.name,
        namespace=c.namespace,
        type=c.type,
        pod_result=pod_result
    )


def validate_controllers(res: NamespaceKubernetesResource):
    ctr = create_validate_controllers(res)
    controllers_result = []
    for c in ctr:
        controllers_result.append(validate_controller(c))
    return controllers_result
