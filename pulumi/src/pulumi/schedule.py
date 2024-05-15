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
        # Arbitrary resource name
        f"{stack_name}/scheduled-deploy",

        # Pulumi deploy schedule running each Tuesday at 10:00 UTC
        schedule_cron="0 10 * * 2",

        # Pulumi Operation to perform (Accepts: PREVIEW, UPDATE, DESTROY)
        pulumi_operation=PulumiOperation.UPDATE,

        # Pulumi Cloud Organization, Project, and Stack names
        organization=organization_name,
        project=project_name,
        stack=stack_name,

        # General Pulumi Resource Options
        opts=ResourceOptions(

            # Parent Stack Deployment settings resource
            # for Deployment Schedule resources
            parent=pulumi_cloud_deployment
        )
    )

    preview_schedule = DeploymentSchedule(
        f"{stack_name}/scheduled-preview",

        # Execute the Pulumi preview operation on May 17, 2024 at midnight UTC
        timestamp="2024-05-17T00:00:00Z",

        # Pulumi Operation to perform (PREVIEW)
        pulumi_operation=PulumiOperation.PREVIEW,

        # Pulumi Cloud Organization, Project, and Stack names
        organization=organization_name,
        project=project_name,
        stack=stack_name,

        opts=ResourceOptions(
            parent=pulumi_cloud_deployment
        )
    )

    # https://www.pulumi.com/docs/pulumi-cloud/deployments/drift
    drift_schedule = DriftSchedule(
        f"{stack_name}/scheduled-drift",

        # Pulumi drift detection each day at 10:00 UTC
        schedule_cron="0 10 * * *",

        # Auto-remediate drift issues
        # True: Auto-remediate drift issues by executing a Pulumi Update operation
        # False: Do not auto-remediate drift issues, use for drift detection and reporting
        auto_remediate=False,

        # Pulumi Cloud Organization, Project, and Stack names
        organization=organization_name,
        project=project_name,
        stack=stack_name,

        opts=ResourceOptions(
            parent=pulumi_cloud_deployment
        )
    )

    # https://www.pulumi.com/docs/pulumi-cloud/deployments/ttl
    ttl_schedule = TtlSchedule(
        f"{stack_name}/scheduled-ttl",

        # Destroy stack on May 18, 2024 at midnight UTC
        timestamp="2024-05-18T00:00:00Z",

        # Delete stack resources after destroying the stack
        # True: Delete stack resources from Pulumi Cloud including all stack state and history
        # False: Do not delete stack resources from Pulumi Cloud, retain stack state and history
        delete_after_destroy=False,

        # Pulumi Cloud Organization, Project, and Stack names
        organization=organization_name,
        project=project_name,
        stack=stack_name,

        opts=ResourceOptions(
            parent=pulumi_cloud_deployment
        )
    )

    # return pulumi schedules as a single tuple
    return (deploy_schedule, drift_schedule, preview_schedule, ttl_schedule)
