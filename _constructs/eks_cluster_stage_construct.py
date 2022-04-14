import aws_cdk
from constructs import Construct
from _stacks.eks_cluster import EksClusterStack


class EksClusterStage(aws_cdk.Stage):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,  # EksClusterDev/EksClusterStage/EksClusterProd
                 env: aws_cdk.Environment,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.__eks_cluster_stack = EksClusterStack(
            self,
            'EksClusterStack',
            env=env
        )

    @property
    def cluster(self):
        return self.__eks_cluster_stack.cluster
