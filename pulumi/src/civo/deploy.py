import pulumi
import pulumi_civo as civo
import pulumi_kubernetes as k8s
from pulumi_civo import KubernetesClusterPoolsArgs

# Deploy CIVO Kubernetes Cluster
def deploy_civo_kubernetes(
        civo_token: str,
        cluster_name: str,
        cluster_size: int,
        civo_region: str,
        kubernetes_distribution: str
    ):

    # Create CIVO Provider with the CIVO API Token
    civo_provider = civo.Provider(
        "civo-provider",
        token=civo_token
    )

    # Export the CIVO Provider
    pulumi.export("civo_provider", civo_provider)

    # Create a CIVO Firewall with default rules
    firewall = civo.Firewall(
        f"{cluster_name}-firewall",
        name=cluster_name,
        region=civo_region,
        create_default_rules=True,
        opts=pulumi.ResourceOptions(
            provider=civo_provider
        )
    )

    # Create the CIVO Kubernetes Cluster Pools
    pools = KubernetesClusterPoolsArgs(
        node_count=cluster_size,
        size="g4s.kube.medium"
    )

    # Create a CIVO Kubernetes Cluster
    kubernetes_cluster = civo.KubernetesCluster(
        f"{cluster_name}-cluster",
        name=f"{cluster_name}-cluster",
        pools=pools,
        cni="cilium",
        cluster_type=kubernetes_distribution,
        region=civo_region,
        firewall_id=firewall.id,
        #kubernetes_version=get_most_recent_kubernetes_version(civo_token),
        opts=pulumi.ResourceOptions(
            depends_on=[firewall],
            provider=civo_provider
        )
    )

    # Create a Kubernetes Kubeconfig for export
    kubeconfig = kubernetes_cluster.kubeconfig

    # Export the CIVO Kubernetes Cluster Kubeconfig
    pulumi.export("kubeconfig", kubeconfig)

    # Create a Kubernetes Provider for the CIVO Kubernetes Cluster
    kubernetes_provider = k8s.Provider(
        "k8s-provider",
        kubeconfig=kubeconfig
    )

    # Export the Kubernetes Provider
    pulumi.export("kubernetes_provider", kubernetes_provider)

    return kubernetes_cluster, kubernetes_provider

#import requests
#
#def get_most_recent_kubernetes_version(civo_token: str):
#    url = 'https://api.civo.com/v2/kubernetes/versions'
#    headers = {'Authorization': f'Bearer {civo_token}'}
#
#    try:
#        response = requests.get(url, headers=headers)
#        response.raise_for_status()
#        versions = response.json()
#
#        # Extract version numbers and sort them in descending order
#        sorted_versions = sorted(versions, key=lambda x: x['version'], reverse=True)
#
#        # Return the most recent version
#        return sorted_versions[0]['version'] if sorted_versions else None
#    except requests.RequestException as e:
#        print(f"An error occurred: {e}")
#        return None
#
## Usage
#most_recent_version = get_most_recent_kubernetes_version(api_key)
