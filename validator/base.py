from typing import Dict, List

from resource.resource import KubernetesResource


class ClusterInfo:
    def __init__(self, res: KubernetesResource):
        self.version = res.version
        self.count = {
            "nodes": len(res.nodes),
            "pods": len(res.pods),
            "namespaces": len(res.namespaces),
            "deployments": len(res.deployments),
            "statefulSets": len(res.stateful_sets),
            "daemonSets": len(res.daemon_sets),
            "jobs": len(res.jobs),
            "cronJobs": len(res.cron_jobs),
        }


class ResultMessage:
    def __init__(self, id, message, type, category):
        self.id = id
        self.message = message
        self.type = type
        self.category = category


class CountSummary:
    def __init__(self, successes=0, errors=0, warnings=0):
        self.successes = successes
        self.warnings = warnings
        self.errors = errors

    def add(self, item):
        self.successes += item.successes
        self.warnings += item.warnings
        self.errors += item.errors


class ResultSummary:
    @property
    def totals(self):
        count = CountSummary()
        for k in self.by_category:
            count.add(self.by_category[k])
        return count

    def __init__(self, category_summary: Dict[str, CountSummary]):
        self.by_category = category_summary

    def add(self, res):
        if res is None:
            return
        for k in self.by_category:
            for j in res.by_category:
                if k == j:
                    self.by_category[k].add(res.by_category[j])


class ContainerResult:
    def __init__(self, name, messages: List[ResultMessage]):
        self.name = name
        self.messages = messages

    @property
    def summary(self):
        from validator.resource import RESOURCE_VALIDATION_ERROR, RESOURCE_VALIDATION_WARNING, \
            RESOURCE_VALIDATION_SUCCESS
        by_category = dict()
        for msg in self.messages:
            category_data = CountSummary()
            if msg.type == RESOURCE_VALIDATION_ERROR:
                category_data.errors += 1
            elif msg.type == RESOURCE_VALIDATION_WARNING:
                category_data.warnings += 1
            elif msg.type == RESOURCE_VALIDATION_SUCCESS:
                category_data.successes += 1
            if by_category.__contains__(msg.category):
                by_category[msg.category].add(category_data)
            else:
                by_category[msg.category] = category_data
        return ResultSummary(
            category_summary=by_category
        )


class PodResult:
    def __init__(self, messages: List[ResultMessage], container_results: List[ContainerResult]):
        self.messages = messages
        self.container_results = container_results

    @property
    def summary(self):
        s = None
        for cr in self.container_results:
            if s is None:
                s = cr.summary
            else:
                s.add(cr.summary)
        return s


class ControllerResult:
    def __init__(self, name, namespace, type, pod_result: PodResult):
        self.name = name
        self.namespace = namespace
        self.type = type
        self.pod_result = pod_result


class NamespaceResult:

    def __init__(self, name):
        self.controller_results = []
        self.name = name

    @property
    def summary(self):
        s = None
        for cr in self.controller_results:
            if s is None:
                s = cr.pod_result.summary
            else:
                s.add(cr.pod_result.summary)
        return s

    def append_controller_result(self, controller_result: ControllerResult):
        self.controller_results.append(controller_result)


class ClusterResult:
    def __init__(self, cluster_info, namespace_results):
        self.cluster_info = cluster_info
        self.namespace_results = namespace_results

    @property
    def summary(self):
        s = None
        for cr in self.namespace_results:
            if s is None:
                s = cr.summary
            else:
                s.add(cr.summary)
        return s
