# agent/collector.py

from kubernetes import client, config as k8s_config
import yaml
import hashlib
import logging
from agent.config import config as agent_config

class KubeCollector:
    def __init__(self):
        # Load Kubernetes configuration
        k8s_config.load_incluster_config()
        self.api_client = client.ApiClient()
        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()
        self.batch_api = client.BatchV1Api()
        self.networking_api = client.NetworkingV1Api()
        self.include_secrets_option = agent_config.include_secrets_option

    def collect_all(self):
        data = {}
        data['namespaces'] = self.collect_namespaces()
        data['pods'] = self.collect_pods()
        data['deployments'] = self.collect_deployments()
        data['services'] = self.collect_services()
        data['configmaps'] = self.collect_configmaps()
        data['secrets'] = self.collect_secrets()
        # Add more resources as needed
        return data

    def collect_namespaces(self):
        namespaces = self.core_api.list_namespace()
        return [ns.metadata.name for ns in namespaces.items]

    def collect_pods(self):
        pods = self.core_api.list_pod_for_all_namespaces(watch=False)
        return [pod.to_dict() for pod in pods.items]

    def collect_deployments(self):
        deployments = self.apps_api.list_deployment_for_all_namespaces(watch=False)
        return [dep.to_dict() for dep in deployments.items]

    def collect_services(self):
        services = self.core_api.list_service_for_all_namespaces(watch=False)
        return [svc.to_dict() for svc in services.items]

    def collect_configmaps(self):
        configmaps = self.core_api.list_config_map_for_all_namespaces(watch=False)
        return [cm.to_dict() for cm in configmaps.items]

    def collect_secrets(self):
        logging.info(f"Collecting secrets with option: {self.include_secrets_option}")
        secrets = self.core_api.list_secret_for_all_namespaces(watch=False)
        secret_list = []
        for secret in secrets.items:
            if self.include_secrets_option == 'exclude':
                continue  # Skip secrets entirely
            elif self.include_secrets_option == 'metadata':
                secret_data = {
                    'metadata': secret.metadata.to_dict(),
                    'type': secret.type,
                }
                secret_list.append(secret_data)
            elif self.include_secrets_option == 'hashed':
                if secret.data:
                    hashed_data = {
                        key: hashlib.sha256(value.encode()).hexdigest()
                        for key, value in secret.data.items()
                    }
                else:
                    hashed_data = {}
                secret_data = {
                    'metadata': secret.metadata.to_dict(),
                    'type': secret.type,
                    'data': hashed_data,
                }
                secret_list.append(secret_data)
        return secret_list