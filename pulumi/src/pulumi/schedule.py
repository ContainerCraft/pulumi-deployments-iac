from pulumi import ResourceOptions
from pulumi_pulumiservice import TtlSchedule, DriftSchedule, DeploymentSchedule, PulumiOperation

def pulumi_schedule(
        organization_name: str,
        project_name: str,
        stack_name: str,
        pulumi_cloud_deployment
    ):

    # https://www.pulumi.com/docs/pulumi-cloud/deployments/schedules
    deploy_schedule = DeploymentSchedule(
        f"{project_name}/{stack_name}-scheduled-deploy",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        # Pulumi deploy (update) each Tuesday at 10:00 UTC
        schedule_cron="0 10 * * 2",
        pulumi_operation=PulumiOperation.UPDATE,
        opts=ResourceOptions(
            depends_on=[pulumi_cloud_deployment]
        )
    )

    # https://www.pulumi.com/docs/pulumi-cloud/deployments/drift
    drift_schedule = DriftSchedule(
        f"{project_name}/{stack_name}-scheduled-drift",
        # Pulumi drift detection each day at 10:00 UTC
        schedule_cron="0 10 * * *",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        auto_remediate=False,
        opts=ResourceOptions(
            depends_on=[pulumi_cloud_deployment]
        )
    )

    preview_schedule = DeploymentSchedule(
        f"{project_name}/{stack_name}-scheduled-preview",
        # Preview stack on May 17, 2024 at midnight UTC
        timestamp="2024-05-17T00:00:00Z",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        pulumi_operation=PulumiOperation.PREVIEW,
        opts=ResourceOptions(
            depends_on=[pulumi_cloud_deployment]
        )
    )

    # https://www.pulumi.com/docs/pulumi-cloud/deployments/ttl
    ttl_schedule = TtlSchedule(
        f"{project_name}/{stack_name}-scheduled-ttl",
        # Destroy stack on May 18, 2024 at midnight UTC
        timestamp="2024-05-18T00:00:00Z",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        delete_after_destroy=False,
        opts=ResourceOptions(
            depends_on=[pulumi_cloud_deployment]
        )
    )

    # return pulumi schedules as a single tuple
    return (deploy_schedule, drift_schedule, preview_schedule, ttl_schedule)
