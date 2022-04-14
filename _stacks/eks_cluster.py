import aws_cdk
from constructs import Construct
from aws_cdk import Stack
from aws_cdk import aws_iam
from aws_cdk import aws_eks
from _constructs.vpc_constructor import VpcConstructor


class EksClusterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env: aws_cdk.Environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ----------------------------------------------------------
        # VPC
        # ----------------------------------------------------------
        _vpc = VpcConstructor(self, 'VpcConstructor', env=env)

        # ----------------------------------------------------------
        # Owner role for EKS Cluster
        # ----------------------------------------------------------
        owner_role = aws_iam.Role(
            scope=self,
            id='EksClusterOwnerRole',
            role_name='EksClusterOwnerRole',
            assumed_by=aws_iam.AccountRootPrincipal()
        )

        # ----------------------------------------------------------
        # EKS Cluster
        # ----------------------------------------------------------
        self.__eks_cluster = aws_eks.Cluster(
            self,
            'EksCluster',
            output_cluster_name=True,
            version=aws_eks.KubernetesVersion.V1_21,
            endpoint_access=aws_eks.EndpointAccess.PUBLIC,
            vpc=_vpc.vpc,
            # vpc_subnets=_vpc.vpc.private_subnets, # Default: - All public and private subnets
            masters_role=owner_role,
            default_capacity=2
        )

    @property
    def cluster(self):
        return self.__eks_cluster
