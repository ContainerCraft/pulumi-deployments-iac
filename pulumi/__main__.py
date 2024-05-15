"""A Python Pulumi Kubernetes IaC Program"""
# Import python packages
import os
import json
import pulumi
import pulumi_kubernetes as k8s

# Import python packages from the local src directory
from src.civo.deploy import deploy_civo_kubernetes
from src.cert_manager.deploy import deploy_cert_manager
from src.pulumi.deploy import pulumi_cloud_deployment
from src.pulumi.schedule import pulumi_schedule

##################################################################################
# Load the Pulumi Config
config = pulumi.Config()

# Set the Pulumi organization name from the project github repository
organization_name = config.get("organization") or "ContainerCraft"

# Set the Github repository name from the Pulumi.yaml
repository_name = config.get("repository") or "pulumi-deployments-iac"

# Set the Pulumi project name from the Pulumi.yaml
project_name = pulumi.get_project()

# Set stack name from the Pulumi stack
stack_name = pulumi.get_stack()

##################################################################################
## Deploy Kubernetes
##################################################################################

# Kubernetes Cluster on CIVO
# Check pulumi config 'civo_kubernetes.deploy' and deploy if true
# Enable CIVO Kubernetes with the following command:
#   ~$ pulumi config set civo_kubernetes.deploy true
enable = config.get_bool('civo_kubernetes.deploy') or False
if enable:
    # Collect CIVO Pulumi Configuration
    cloud_provider = "civo"
    civo_token = config.require_secret("civoApiToken")
    civo_region = config.get("civo_kubernetes.region") or "NYC1"
    worker_count = config.get_int("civo_kubernetes.worker_count") or 2
    kubernetes_distribution = config.get("civo_kubernetes.distribution") or "k3s"

    # Deploy CIVO Kubernetes Cluster
    kubernetes_cluster = deploy_civo_kubernetes(
        civo_token,
        stack_name,
        worker_count,
        civo_region,
        kubernetes_distribution
    )

    # Export the CIVO Kubernetes Cluster for use in other resources
    kubernetes_cluster_resource = kubernetes_cluster[0]

    # Create a Kubernetes Provider from the CIVO Kubernetes Cluster for export
    kubernetes_provider = kubernetes_cluster[1]
else:
    cloud_provider = ""
    kubernetes_distribution = ""
    kubernetes_cluster = (None, None)

##################################################################################
## Deploy Kubernetes Resources
##################################################################################

# Cert Manager
# Check pulumi config 'cert_manager.enable' and deploy if true
# Enable cert-manager with the following command:
#   ~$ pulumi config set cert_manager.enabled true
# Set cert-manager version override with the following command:
#   ~$ pulumi config set cert_manager.version v1.5.3
cert_manager_enabled = config.get_bool('cert_manager.enabled') or False
if cert_manager_enabled:
    # Collect Cert Manager Pulumi Configuration
    version = config.get('cert_manager.version') or None
    cluster = kubernetes_cluster_resource
    namespace = "cert-manager"

    # Deploy cert-manager
    cert_manager = deploy_cert_manager(
        namespace,
        version,
        kubernetes_distribution,
        kubernetes_provider,
        kubernetes_cluster_resource,
        stack_name
    )
else:
    cert_manager = (None, None)

##################################################################################
## Pulumi Cloud: Deployment Configuration
##################################################################################

# Deploy Pulumi Cloud Deployment
# Check pulumi config 'pulumi_cloud.deploy' and deploy if true
# Enable Pulumi Cloud Deployment with the following command:
#   ~$ pulumi config set pulumi_cloud.deploy true
pulumi_cloud_enabled = config.get_bool('pulumi_cloud.deployment') or False
if pulumi_cloud_enabled:
    pulumi_cloud_deployment = pulumi_cloud_deployment(
        organization_name,
        project_name,
        stack_name,
        repository_name
    )
else:
    pulumi_cloud_deployment = None

# Pulumi Cloud Deployment TTL/Drift/Schedule configuration
# Check pulumi config 'pulumi_cloud.schedule' and deploy if true
# Enable Pulumi Cloud Deployment Schedule with the following command:
#   ~$ pulumi config set pulumi_cloud.schedule true
pulumi_cloud_schedule = config.get_bool('pulumi_cloud.schedule') or False
if pulumi_cloud_schedule:
    pulumi_schedule(
        organization_name,
        project_name,
        stack_name,
        pulumi_cloud_deployment
    )
    # export the url for the Pulumi Deployments Stack Schedule Settings
    pulumi.export("DeploymentsURL:", f"https://app.pulumi.com/{organization_name}/{project_name}/{stack_name}/settings/schedule")
else:
    pulumi_schedule = (None, None, None, None)

##################################################################################
## Export Stack Outputs
##################################################################################

# Use pulumi.Output.all() to aggregate all Output values and then construct the dictionary
meta = pulumi.Output.all().apply(lambda args: json.dumps({"kubernetes": {
    "cloud": cloud_provider,
    "dist": kubernetes_distribution,
    "cert_manager": cert_manager_enabled,
    "pulumi_cloud_deployments": pulumi_cloud_enabled
}}, default=str))

# Create a dictionary of deployed resource versions
versions = pulumi.Output.all(
    cert_manager[0] or None
).apply(lambda args: json.dumps({
    "cert_manager": args[0]
}, default=str))

# Export the 'kube' dictionary as a stack output in json format
pulumi.export("meta", meta)

# Export the 'versions' dictionary as a stack output in json format
pulumi.export("versions", versions)
