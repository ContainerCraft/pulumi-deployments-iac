import pulumi
from pulumi_pulumiservice import (
    DeploymentSettings,
    DeploymentSettingsGithubArgs,
    DeploymentSettingsGitSourceArgs,
    DeploymentSettingsOperationContextArgs,
    DeploymentSettingsSourceContextArgs,
    OperationContextOptionsArgs
)

# Deploy Pulumi Cloud Deployments Stack Configuration
def pulumi_cloud_deployment(
        organization_name: str,
        project_name: str,
        stack_name: str,
        repository_name: str
    ):

    pulumiservice_deploymentsettings = DeploymentSettings(
        "pulumiservice_deploymentsettings",
        stack="dev",
        project="kubernetes-platform",
        organization="ContainerCraft",
        agent_pool_id="",
        github=DeploymentSettingsGithubArgs(
            deploy_commits=True,
            preview_pull_requests=True,
            pull_request_template=False,
            repository="ContainerCraft/pulumi-deployments-iac",
        ),
        source_context=DeploymentSettingsSourceContextArgs(
            git=DeploymentSettingsGitSourceArgs(
                branch="main",
            ),
        ),
        operation_context=DeploymentSettingsOperationContextArgs(
            options=OperationContextOptionsArgs(),
        ),
        opts=pulumi.ResourceOptions(protect=False))

    return pulumiservice_deploymentsettings
