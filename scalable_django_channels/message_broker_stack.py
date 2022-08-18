from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_elasticache as elasticache,
    CfnOutput,
)

from constructs import Construct


class MessageBrokerStack(Stack):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            vpc: ec2.Vpc,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Security Groups
        self.redis_sec_group = ec2.SecurityGroup(
            self,
            "redis-sec-group",
            security_group_name="redis-sec-group",
            vpc=vpc,
            allow_all_outbound=True,
        )
        # Add ingress rules to redis security groups
        self.redis_sec_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            description="Allow Redis connection",
            connection=ec2.Port.tcp(6379),
        )
        isolated_subnets_ids = [ps.subnet_id for ps in vpc.isolated_subnets]
        self.redis_subnet_group = elasticache.CfnSubnetGroup(
            scope=self,
            id="redis_subnet_group",
            subnet_ids=isolated_subnets_ids,
            description="subnet group for redis",
        )
        # Elasticache for Redis cluster
        self.redis_cluster = elasticache.CfnCacheCluster(
            scope=self,
            id="redis_cluster",
            engine="redis",
            cache_node_type="cache.t3.micro",  # ToDo Large instance types support auto-scaling
            num_cache_nodes=1,
            cache_subnet_group_name=self.redis_subnet_group.ref,
            vpc_security_group_ids=[self.redis_sec_group.security_group_id],
        )
        self.endpoint_url = self.redis_cluster.attr_redis_endpoint_address
        CfnOutput(
            scope=self,
            id="endpoint_url",
            value=self.endpoint_url,
        )
