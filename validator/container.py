from kubernetes.client import V1SecurityContext, V1PodSpec, V1PodSecurityContext

from validator.config import check_list
from validator.resource import ResourceValidation
from . import messages
from kubernetes.client.models.v1_container import V1Container
from .base import ContainerResult


class ContainerValidation(ResourceValidation):
    def __init__(self, container, parent):
        super().__init__()
        self.container: V1Container = container
        self.init = True
        self.parent: V1PodSpec = parent

    def validate_resources(self):
        if not self.init:
            return
        category = messages.CategoryResources
        res = self.container.resources
        resource_conf = check_list.get("kube", None)

        def validate_cpu_request(cv: ContainerValidation):
            missing_name = "cpuRequestsMissing"
            if res.requests and res.requests.__contains__("cpu"):
                cv.on_success(messages.CPURequestsLabel, category, missing_name)
            else:
                severity = resource_conf.get(missing_name, None)
                cv.on_failure(messages.CPURequestsFailure, severity, category, missing_name)

        def validate_cpu_limits(cv: ContainerValidation):
            missing_name = "cpuLimitsMissing"
            if res.limits and res.limits.__contains__("cpu"):
                cv.on_success(messages.CPULimitsLabel, category, missing_name)
            else:
                severity = resource_conf.get(missing_name, None)
                cv.on_failure(messages.CPULimitsFailure, severity, category, missing_name)

        def validate_memory_request(cv: ContainerValidation):
            missing_name = "memoryRequestsMissing"
            if res.requests and res.requests.__contains__("memory"):
                cv.on_success(messages.MemoryRequestsLabel, category, missing_name)
            else:
                severity = resource_conf.get(missing_name, None)
                cv.on_failure(messages.MemoryRequestsFailure, severity, category, missing_name)

        def validate_memory_limits(cv: ContainerValidation):
            missing_name = "memoryLimitsMissing"
            if res.limits and res.limits.__contains__("memory"):
                cv.on_success(messages.MemoryLimitsLabel, category, missing_name)
            else:
                severity = resource_conf.get(missing_name, None)
                cv.on_failure(messages.MemoryLimitsFailure, severity, category, missing_name)

        validate_cpu_request(self)
        validate_cpu_limits(self)
        validate_memory_limits(self)
        validate_memory_request(self)

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

    def validate_security(self):
        category = messages.CategorySecurity
        security_conf = check_list.get("security", None)
        security_context = self.container.security_context
        pod_security_context = self.parent.security_context
        if not security_context:
            security_context = V1SecurityContext()
        if not pod_security_context:
            pod_security_context = V1PodSecurityContext()

        def validate_run_as_root_allowed(cv: ContainerValidation):
            name = "runAsRootAllowed"
            severity = security_conf.get(name, None)
            success = False
            if security_context.run_as_non_root or (
                    security_context.run_as_user is not None and security_context.run_as_user > 0):
                success = True
            elif security_context.run_as_non_root is None and security_context.run_as_user is None:
                success = pod_security_context.run_as_non_root or (
                        pod_security_context.run_as_user is not None and pod_security_context.run_as_user > 0)
            if success:
                cv.on_success(messages.RunAsRootSuccess, category, name)
            else:
                cv.on_failure(messages.RunAsRootFailure, severity, category, name)

        def validate_run_as_privileged(cv: ContainerValidation):
            name = "runAsPrivileged"
            severity = security_conf.get(name, None)
            if security_context.privileged:
                cv.on_failure(messages.RunAsPrivilegedFailure, severity, category, name)
            else:
                cv.on_success(messages.RunAsPrivilegedSuccess, category, name)

        def validate_not_read_only_root_file_system(cv: ContainerValidation):
            name = "notReadOnlyRootFileSystem"
            severity = security_conf.get(name, None)
            if security_context.read_only_root_filesystem:
                cv.on_success(messages.ReadOnlyFilesystemFailure, category, name)
            else:
                cv.on_failure(messages.ReadOnlyFilesystemSuccess, severity, category, name)

        def validate_privilege_escalation_allowed(cv: ContainerValidation):
            name = "privilegeEscalationAllowed"
            severity = security_conf.get(name, None)
            if security_context.allow_privilege_escalation:
                cv.on_failure(messages.PrivilegeEscalationFailure, severity, category, name)
            else:
                cv.on_success(messages.PrivilegeEscalationSuccess, category, name)

        validate_run_as_root_allowed(self)
        validate_run_as_privileged(self)
        validate_not_read_only_root_file_system(self)
        validate_privilege_escalation_allowed(self)


def validate_container(con, parent):
    cv = ContainerValidation(con, parent)
    cv.validate_resources()
    cv.validate_networking()
    cv.validate_health_checks()
    cv.validate_images()
    cv.validate_security()
    return ContainerResult(con.name, cv.messages)
