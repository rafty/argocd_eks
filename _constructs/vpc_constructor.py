import aws_cdk
from constructs import Construct
from aws_cdk import aws_ec2


class VpcConstructor(Construct):

    def __init__(self,
                 scope: Construct,
                 id: str,
                 env: aws_cdk.Environment,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.__vpc = aws_ec2.Vpc(
            self,
            'Vpc',
            max_azs=1,
            cidr='10.11.0.0/16',
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    subnet_type=aws_ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24),
                aws_ec2.SubnetConfiguration(
                    subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_NAT,
                    name="Private",
                    cidr_mask=24),
            ],
            nat_gateways=1
        )

    @property
    def vpc(self):
        return self.__vpc
