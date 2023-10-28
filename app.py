#!/usr/bin/env python3

import aws_cdk as cdk

from axr_public_demo.axr_public_demo_stack import AxrPublicDemoStack


app = cdk.App()
AxrPublicDemoStack(app, "AxrPublicDemoStack")

app.synth()
