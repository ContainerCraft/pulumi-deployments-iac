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
        # Arbitrary name for the resource
        f"{stack_name}/deploymentsettings",

        # Pulumi stack, project and organization names
        stack=stack_name,
        project=project_name,
        organization=organization_name,

        # Agent pool ID for deployments
        agent_pool_id="",

        # Github integration configuration
        github=DeploymentSettingsGithubArgs(
            deploy_commits=True,
            preview_pull_requests=True,
            pull_request_template=False,
            repository=f"{organization_name}/{repository_name}",
        ),

        # Source code context configuration
        source_context=DeploymentSettingsSourceContextArgs(
            git=DeploymentSettingsGitSourceArgs(
                branch="main",
            ),
        ),
        operation_context=DeploymentSettingsOperationContextArgs(
            options=OperationContextOptionsArgs(),
        ),
        opts=pulumi.ResourceOptions(protect=False)
    )

    return pulumiservice_deploymentsettings
