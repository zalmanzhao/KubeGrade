__all__ = ["check_list"]

__default_check_list = {
    "security": {
        "hostIPCSet": "error",
        "hostPIDSet": "error",
        "notReadOnlyRootFileSystem": "warning",
        "privilegeEscalationAllowed": "error",
        "runAsRootAllowed": "warning",
        "runAsPrivileged": "error",
    },
    "kube": {
        "cpuRequestsMissing": "warning",
        "cpuLimitsMissing": "warning",
        "memoryRequestsMissing": "warning",
        "memoryLimitsMissing": "warning",
    },
    "images": {
        "tagNotSpecified": "error",
        "pullPolicyNotAlways": "ignore"
    },
    "healthChecks": {
        "readinessProbeMissing": "warning",
        "livenessProbeMissing": "warning"
    },
    "networking": {
        "hostNetworkSet": "warning",
        "hostPortSet": "warning"
    },
    "controllers": ["Deployments", "StatefulSets", "DaemonSets", "CronJobs", "Jobs"]
}

check_list = __default_check_list
