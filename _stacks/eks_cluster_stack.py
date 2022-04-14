import aws_cdk
from aws_cdk import Stack
from constructs import Construct
from aws_cdk.pipelines import CodePipeline
from aws_cdk.pipelines import CodePipelineSource
from aws_cdk.pipelines import ShellStep
from _constructs.eks_cluster_stage_construct import EksClusterStage

class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env: aws_cdk.Environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ----------------------------------------------------------
        # Source
        # ----------------------------------------------------------
        repository_name = self.node.try_get_context('repository-name')
        github_connection_arn = self.node.try_get_context('github-connection-arn')
        github_connection = CodePipelineSource.connection(
            repo_string=repository_name,
            branch='master',
            connection_arn=github_connection_arn
        )

        # ----------------------------------------------------------
        # Pipeline: Stage: Source, Build(CDK), UpdatePipeline
        # ----------------------------------------------------------
        pipeline_name = self.node.try_get_context('pipeline-name')
        pipeline = CodePipeline(
            scope=self,
            id=pipeline_name,
            pipeline_name=pipeline_name,
            self_mutation=True,
            synth=ShellStep(
                id='Synth',
                input=github_connection,
                commands=[
                    'npm install -g aws-cdk',
                    'python -m pip install -r requirements.txt',
                    'cdk synth'
                ]
            )
        )

        # ----------------------------------------
        # Add Stage: EKS Cluster
        # ----------------------------------------
        eks_cluster_dev_stage = EksClusterStage(
            scope=self,
            construct_id='EksClusterDev',
            env=env
        )
        pipeline.add_stage(eks_cluster_dev_stage)
