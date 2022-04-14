import aws_cdk as core
import aws_cdk.assertions as assertions

from argocd_eks.argocd_eks_stack import ArgocdEksStack

# example tests. To run these tests, uncomment this file along with the example
# resource in argocd_eks/argocd_eks_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ArgocdEksStack(app, "argocd-eks")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
