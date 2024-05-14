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
# https://www.pulumi.com/docs/pulumi-cloud/deployments
def pulumi_cloud_deployment(
        organization_name: str,
        project_name: str,
        stack_name: str,
        repository_name: str
    ):

    # https://www.pulumi.com/registry/packages/pulumiservice/api-docs/deploymentsettings
    pulumiservice_deploymentsettings = DeploymentSettings(
        f"{stack_name}/deploymentsettings",
        stack=stack_name,
        project=project_name,
        organization=organization_name,
        agent_pool_id="",
        github=DeploymentSettingsGithubArgs(
            deploy_commits=True,
            preview_pull_requests=True,
            pull_request_template=False,
            repository=f"{organization_name}/{repository_name}",
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
