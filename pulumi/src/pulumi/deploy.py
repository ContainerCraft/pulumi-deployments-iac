import pulumi
import pulumi_pulumiservice as pulumiservice
#from pulumi_pulumiservice import (
#    DeploymentSettings,
#    DeploymentSettingsGithubArgs,
#    DeploymentSettingsGitSourceArgs,
#    DeploymentSettingsOperationContextArgs,
#    DeploymentSettingsSourceContextArgs,
#    OperationContextOptionsArgs
#)

# Deploy Pulumi Cloud Deployments Stack Configuration
def pulumi_cloud_deployment(
        organization_name: str,
        project_name: str,
        stack_name: str,
        repository_name: str
    ):

    pulumiservice_deploymentsettings = pulumiservice.DeploymentSettings("pulumiservice_deploymentsettings",
        stack="dev",
        project="kubernetes-platform",
        organization="ContainerCraft",
        agent_pool_id="",
        github=pulumiservice.DeploymentSettingsGithubArgs(
            deploy_commits=True,
            preview_pull_requests=True,
            pull_request_template=False,
            repository="ContainerCraft/pulumi-deployments-iac",
        ),
        source_context=pulumiservice.DeploymentSettingsSourceContextArgs(
            git=pulumiservice.DeploymentSettingsGitSourceArgs(
                branch="main",
            ),
        ),
        operation_context=pulumiservice.DeploymentSettingsOperationContextArgs(
            options=pulumiservice.OperationContextOptionsArgs(),
        ),
        opts=pulumi.ResourceOptions(protect=False))

    ## Pulumi Cloud: Deployment Configuration
    #pulumi_cloud_deployment_config = pulumiservice.DeploymentSettings(
    #    f"{organization_name}/{project_name}/{stack_name}",
    #    stack=stack_name,
    #    project=project_name,
    #    organization=organization_name,
    #    github=pulumiservice.DeploymentSettingsGithubArgs(
    #        repository=f"{organization_name}/{repository_name}",
    #        deploy_commits=True,
    #        preview_pull_requests=True,
    #        pull_request_template=True,
    #        paths=["."]
    #    ),
    #    source_context=pulumiservice.DeploymentSettingsSourceContextArgs(
    #        git=pulumiservice.DeploymentSettingsGitSourceArgs(
    #            branch="main",
    #            repo_dir="."
    #        )
    #    ),
    #    executor_context=pulumiservice.DeploymentSettingsExecutorContextArgs(
    #        executor_image="docker.io/pulumi/pulumi"
    #    ),
    #    operation_context=pulumiservice.DeploymentSettingsOperationContextArgs(
    #        options=pulumiservice.OperationContextOptionsArgs(
    #            delete_after_destroy=False,
    #            shell="/bin/bash",
    #            skip_install_dependencies=False,
    #            skip_intermediate_deployments=False
    #        ),
    #        #environment_variables={
    #        #    "PULUMI_ACCESS_TOKEN": "YOUR_ACCESS_TOKEN",  # Ensure to secure or inject this securely
    #        #    "PULUMI_ORG": organization_name,
    #        #    "PULUMI_PROJECT": project_name,
    #        #    "PULUMI_STACK": stack_name
    #        #},
    #        #pre_run_commands=[
    #        #    "pip install -r requirements.txt",
    #        #    "pulumi up --yes"
    #        #]
    #    ),
    #    agent_pool_id="",
    #    opts=pulumi.ResourceOptions(
    #        protect=False
    #    )
    #)

    return pulumiservice_deploymentsettings

#import pulumi
#import pulumi_pulumiservice as pulumiservice
#
## Deploy Pulumi Cloud Deployments Stack Configuration
#def pulumi_cloud_deployment(
#        organization_name: str,
#        project_name: str,
#        stack_name: str,
#        repository_name: str
#    ):
#
#    # Pulumi Cloud: Deployment Configuration
#    pulumi_cloud_deployment_config = pulumiservice.DeploymentSettings(
#        f"{organization_name}/{project_name}/{stack_name}-deployment",
#        stack=stack_name,
#        project="kubernetes-platform",
#        organization="ContainerCraft",
#        agent_pool_id="",
#        github=pulumiservice.DeploymentSettingsGithubArgs(
#            paths=["."],
#            deploy_commits=True,
#            preview_pull_requests=True,
#            pull_request_template=True,
#            repository=f"ContainerCraft/{repository_name}",
#        ),
#        operation_context=pulumiservice.DeploymentSettingsOperationContextArgs(
#            options=pulumiservice.OperationContextOptionsArgs(),
#        ),
#        source_context=pulumiservice.DeploymentSettingsSourceContextArgs(
#            git=pulumiservice.DeploymentSettingsGitSourceArgs(
#                branch="main",
#            ),
#        ),
#        opts=pulumi.ResourceOptions(protect=False)
#    )
#
#    return pulumi_cloud_deployment_config
