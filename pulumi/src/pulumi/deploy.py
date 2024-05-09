import pulumi
import pulumi_pulumiservice as pulumiservice

# Deploy Pulumi Cloud Deployments Stack Configuration
def pulumi_cloud_deployment(
        organization_name: str,
        project_name: str,
        stack_name: str,
        repository_name: str
    ):

    # Pulumi Cloud: Deployment Configuration
    pulumi_cloud_deployment_config = pulumiservice.DeploymentSettings(
        f"{organization_name}/{project_name}/{stack_name}-deployment",
        stack="dev",
        project="kubernetes-platform",
        organization="ContainerCraft",
        agent_pool_id="",
        github=pulumiservice.DeploymentSettingsGithubArgs(
            deploy_commits=True,
            paths=["."],
            preview_pull_requests=False,
            pull_request_template=True,
            repository="ContainerCraft/pulumi-deployments-iac",
        ),
        operation_context=pulumiservice.DeploymentSettingsOperationContextArgs(
            options=pulumiservice.OperationContextOptionsArgs(),
        ),
        source_context=pulumiservice.DeploymentSettingsSourceContextArgs(
            git=pulumiservice.DeploymentSettingsGitSourceArgs(
                branch="main",
            ),
        ),
        opts=pulumi.ResourceOptions(protect=True)
    )

    return pulumi_cloud_deployment_config
