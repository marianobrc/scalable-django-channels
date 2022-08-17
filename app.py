#!/usr/bin/env python3
import os
import aws_cdk as cdk
from aws_cdk import (
    Environment,
)
from scalable_django_channels.pipeline_stack import MyDjangoChatAppPipelineStack


app = cdk.App()
pipeline = MyDjangoChatAppPipelineStack(
    app,
    "MyDjangoChatPipeline",
    repository="marianobrc/scalable-django-channels",
    branch="master",
    ssm_gh_connection_param="/Github/Connection",
    env=Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)
app.synth()
