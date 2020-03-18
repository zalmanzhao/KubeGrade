from config import check_list
from .resource import ResourceValidation
from . import messages
from kubernetes.client.models.v1_container import V1Container
from kubernetes.client.models.v1_pod import V1Pod
from .base import ContainerResult


class ContainerValidation(ResourceValidation):
    def __init__(self, container, parent):
        super().__init__()
        self.container: V1Container = container
        self.init = True
        self.parent: V1Pod = parent

    def validate_resources(self):
        if not self.init:
            return
        category = messages.CategoryResources
        res = self.container.resources
        resource_conf = check_list.get("resource", None)

        def validate_cpu_request(cv: ContainerValidation):
            missing_name = "cpuRequestsMissing"
            # range_name = "CPURequestRanges"
            if res.requests and res.requests.__contains__("cpu"):
                cv.on_success(messages.CPURequestsLabel, category, missing_name)
            else:
                severity = resource_conf.get(missing_name, None)
                cv.on_failure(messages.CPURequestsFailure, severity, category, missing_name)

        def validate_cpu_limits(cv: ContainerValidation):
            missing_name = "cpuLimitsMissing"
            # range_name = "CPURequestRanges"
            if res.limits and res.limits.__contains__("cpu"):
                cv.on_success(messages.CPULimitsLabel, category, missing_name)
            else:
                severity = resource_conf.get(missing_name, None)
                cv.on_failure(messages.CPULimitsFailure, severity, category, missing_name)

        validate_cpu_request(self)
        validate_cpu_limits(self)

    def validate_health_checks(self):
        category = messages.CategoryHealthChecks
        health_check_conf = check_list.get("healthChecks", None)

        def validate_readiness_probe(cv: ContainerValidation):
            name = "readinessProbeMissing"
            if not cv.container.readiness_probe:
                severity = health_check_conf.get(name, None)
                cv.on_failure(messages.ReadinessProbeFailure, severity, category, name)
            else:
                cv.on_success(messages.ReadinessProbeSuccess, category, name)

        def validate_liveness_probe(cv: ContainerValidation):
            name = "livenessProbeMissing"
            if not cv.container.liveness_probe:
                severity = health_check_conf.get(name, None)
                cv.on_failure(messages.LivenessProbeFailure, severity, category, name)
            else:
                cv.on_success(messages.LivenessProbeSuccess, category, name)

        validate_liveness_probe(self)
        validate_readiness_probe(self)

    def validate_images(self):
        category = messages.CategoryImages
        images_conf = check_list.get("images", None)

        def validate_pull_policy(cv: ContainerValidation):
            name = "pullPolicyNotAlways"
            severity = images_conf.get(name, None)
            if not cv.container.image_pull_policy == 'Always':
                cv.on_failure(messages.ImagePullPolicyFailure, severity, category, name)
            else:
                cv.on_success(messages.ImagePullPolicySuccess, category, name)

        def validate_tag_not_specified(cv: ContainerValidation):
            name = "tagNotSpecified"
            severity = images_conf.get(name, None)
            image = cv.container.image.split(":")
            if len(image) == 1 or image[-1] == "latest":
                cv.on_failure(messages.ImageTagFailure, severity, category, name)
            else:
                cv.on_success(messages.ImageTagSuccess, category, name)

        validate_pull_policy(self)
        validate_tag_not_specified(self)

    def validate_networking(self):
        category = messages.CategoryNetworking
        networking_conf = check_list.get("networking", None)

        def validate_host_port_set(cv: ContainerValidation):
            name = "hostPortSet"
            severity = networking_conf.get(name, None)
            host_port_set = False
            if cv.container.ports:
                for port in cv.container.ports:
                    if not port.host_port:
                        host_port_set = True
                        break
            if host_port_set:
                cv.on_failure(messages.HostPortFailure, severity, category, name)
            else:
                cv.on_success(messages.HostNetworkSuccess, category, name)

        validate_host_port_set(self)


def validate_container(con, parent):
    cv = ContainerValidation(con, parent)
    cv.validate_resources()
    cv.validate_networking()
    cv.validate_health_checks()
    cv.validate_images()
    return ContainerResult(con.name, cv.messages)
