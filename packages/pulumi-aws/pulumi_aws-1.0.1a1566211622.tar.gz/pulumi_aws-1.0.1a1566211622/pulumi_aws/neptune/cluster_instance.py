# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class ClusterInstance(pulumi.CustomResource):
    address: pulumi.Output[str]
    """
    The hostname of the instance. See also `endpoint` and `port`.
    """
    apply_immediately: pulumi.Output[bool]
    """
    Specifies whether any instance modifications
    are applied immediately, or during the next maintenance window. Default is`false`.
    """
    arn: pulumi.Output[str]
    """
    Amazon Resource Name (ARN) of neptune instance
    """
    auto_minor_version_upgrade: pulumi.Output[bool]
    """
    Indicates that minor engine upgrades will be applied automatically to the instance during the maintenance window. Default is `true`.
    """
    availability_zone: pulumi.Output[str]
    """
    The EC2 Availability Zone that the neptune instance is created in.
    """
    cluster_identifier: pulumi.Output[str]
    """
    The identifier of the [`neptune.Cluster`](https://www.terraform.io/docs/providers/aws/r/neptune_cluster.html) in which to launch this instance.
    """
    dbi_resource_id: pulumi.Output[str]
    """
    The region-unique, immutable identifier for the neptune instance.
    """
    endpoint: pulumi.Output[str]
    """
    The connection endpoint in `address:port` format.
    """
    engine: pulumi.Output[str]
    """
    The name of the database engine to be used for the neptune instance. Defaults to `neptune`. Valid Values: `neptune`.
    """
    engine_version: pulumi.Output[str]
    """
    The neptune engine version.
    """
    identifier: pulumi.Output[str]
    """
    The indentifier for the neptune instance, if omitted, this provider will assign a random, unique identifier.
    """
    identifier_prefix: pulumi.Output[str]
    """
    Creates a unique identifier beginning with the specified prefix. Conflicts with `identifier`.
    """
    instance_class: pulumi.Output[str]
    """
    The instance class to use.
    """
    kms_key_arn: pulumi.Output[str]
    """
    The ARN for the KMS encryption key if one is set to the neptune cluster.
    """
    neptune_parameter_group_name: pulumi.Output[str]
    """
    The name of the neptune parameter group to associate with this instance.
    """
    neptune_subnet_group_name: pulumi.Output[str]
    """
    A subnet group to associate with this neptune instance. **NOTE:** This must match the `neptune_subnet_group_name` of the attached [`neptune.Cluster`](https://www.terraform.io/docs/providers/aws/r/neptune_cluster.html).
    """
    port: pulumi.Output[float]
    """
    The port on which the DB accepts connections. Defaults to `8182`.
    """
    preferred_backup_window: pulumi.Output[str]
    """
    The daily time range during which automated backups are created if automated backups are enabled. Eg: "04:00-09:00"
    """
    preferred_maintenance_window: pulumi.Output[str]
    """
    The window to perform maintenance in.
    Syntax: "ddd:hh24:mi-ddd:hh24:mi". Eg: "Mon:00:00-Mon:03:00".
    """
    promotion_tier: pulumi.Output[float]
    """
    Default 0. Failover Priority setting on instance level. The reader who has lower tier has higher priority to get promoter to writer.
    """
    publicly_accessible: pulumi.Output[bool]
    """
    Bool to control if instance is publicly accessible. Default is `false`.
    """
    storage_encrypted: pulumi.Output[bool]
    """
    Specifies whether the neptune cluster is encrypted.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the instance.
    """
    writer: pulumi.Output[bool]
    """
    Boolean indicating if this instance is writable. `False` indicates this instance is a read replica.
    """
    def __init__(__self__, resource_name, opts=None, apply_immediately=None, auto_minor_version_upgrade=None, availability_zone=None, cluster_identifier=None, engine=None, engine_version=None, identifier=None, identifier_prefix=None, instance_class=None, neptune_parameter_group_name=None, neptune_subnet_group_name=None, port=None, preferred_backup_window=None, preferred_maintenance_window=None, promotion_tier=None, publicly_accessible=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        A Cluster Instance Resource defines attributes that are specific to a single instance in a Neptune Cluster.
        
        You can simply add neptune instances and Neptune manages the replication. You can use the [count][1]
        meta-parameter to make multiple instances and join them all to the same Neptune Cluster, or you may specify different Cluster Instance resources with various `instance_class` sizes.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] apply_immediately: Specifies whether any instance modifications
               are applied immediately, or during the next maintenance window. Default is`false`.
        :param pulumi.Input[bool] auto_minor_version_upgrade: Indicates that minor engine upgrades will be applied automatically to the instance during the maintenance window. Default is `true`.
        :param pulumi.Input[str] availability_zone: The EC2 Availability Zone that the neptune instance is created in.
        :param pulumi.Input[str] cluster_identifier: The identifier of the [`neptune.Cluster`](https://www.terraform.io/docs/providers/aws/r/neptune_cluster.html) in which to launch this instance.
        :param pulumi.Input[str] engine: The name of the database engine to be used for the neptune instance. Defaults to `neptune`. Valid Values: `neptune`.
        :param pulumi.Input[str] engine_version: The neptune engine version.
        :param pulumi.Input[str] identifier: The indentifier for the neptune instance, if omitted, this provider will assign a random, unique identifier.
        :param pulumi.Input[str] identifier_prefix: Creates a unique identifier beginning with the specified prefix. Conflicts with `identifier`.
        :param pulumi.Input[str] instance_class: The instance class to use.
        :param pulumi.Input[str] neptune_parameter_group_name: The name of the neptune parameter group to associate with this instance.
        :param pulumi.Input[str] neptune_subnet_group_name: A subnet group to associate with this neptune instance. **NOTE:** This must match the `neptune_subnet_group_name` of the attached [`neptune.Cluster`](https://www.terraform.io/docs/providers/aws/r/neptune_cluster.html).
        :param pulumi.Input[float] port: The port on which the DB accepts connections. Defaults to `8182`.
        :param pulumi.Input[str] preferred_backup_window: The daily time range during which automated backups are created if automated backups are enabled. Eg: "04:00-09:00"
        :param pulumi.Input[str] preferred_maintenance_window: The window to perform maintenance in.
               Syntax: "ddd:hh24:mi-ddd:hh24:mi". Eg: "Mon:00:00-Mon:03:00".
        :param pulumi.Input[float] promotion_tier: Default 0. Failover Priority setting on instance level. The reader who has lower tier has higher priority to get promoter to writer.
        :param pulumi.Input[bool] publicly_accessible: Bool to control if instance is publicly accessible. Default is `false`.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the instance.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/neptune_cluster_instance.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['apply_immediately'] = apply_immediately
            __props__['auto_minor_version_upgrade'] = auto_minor_version_upgrade
            __props__['availability_zone'] = availability_zone
            if cluster_identifier is None:
                raise TypeError("Missing required property 'cluster_identifier'")
            __props__['cluster_identifier'] = cluster_identifier
            __props__['engine'] = engine
            __props__['engine_version'] = engine_version
            __props__['identifier'] = identifier
            __props__['identifier_prefix'] = identifier_prefix
            if instance_class is None:
                raise TypeError("Missing required property 'instance_class'")
            __props__['instance_class'] = instance_class
            __props__['neptune_parameter_group_name'] = neptune_parameter_group_name
            __props__['neptune_subnet_group_name'] = neptune_subnet_group_name
            __props__['port'] = port
            __props__['preferred_backup_window'] = preferred_backup_window
            __props__['preferred_maintenance_window'] = preferred_maintenance_window
            __props__['promotion_tier'] = promotion_tier
            __props__['publicly_accessible'] = publicly_accessible
            __props__['tags'] = tags
            __props__['address'] = None
            __props__['arn'] = None
            __props__['dbi_resource_id'] = None
            __props__['endpoint'] = None
            __props__['kms_key_arn'] = None
            __props__['storage_encrypted'] = None
            __props__['writer'] = None
        super(ClusterInstance, __self__).__init__(
            'aws:neptune/clusterInstance:ClusterInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, address=None, apply_immediately=None, arn=None, auto_minor_version_upgrade=None, availability_zone=None, cluster_identifier=None, dbi_resource_id=None, endpoint=None, engine=None, engine_version=None, identifier=None, identifier_prefix=None, instance_class=None, kms_key_arn=None, neptune_parameter_group_name=None, neptune_subnet_group_name=None, port=None, preferred_backup_window=None, preferred_maintenance_window=None, promotion_tier=None, publicly_accessible=None, storage_encrypted=None, tags=None, writer=None):
        """
        Get an existing ClusterInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The hostname of the instance. See also `endpoint` and `port`.
        :param pulumi.Input[bool] apply_immediately: Specifies whether any instance modifications
               are applied immediately, or during the next maintenance window. Default is`false`.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of neptune instance
        :param pulumi.Input[bool] auto_minor_version_upgrade: Indicates that minor engine upgrades will be applied automatically to the instance during the maintenance window. Default is `true`.
        :param pulumi.Input[str] availability_zone: The EC2 Availability Zone that the neptune instance is created in.
        :param pulumi.Input[str] cluster_identifier: The identifier of the [`neptune.Cluster`](https://www.terraform.io/docs/providers/aws/r/neptune_cluster.html) in which to launch this instance.
        :param pulumi.Input[str] dbi_resource_id: The region-unique, immutable identifier for the neptune instance.
        :param pulumi.Input[str] endpoint: The connection endpoint in `address:port` format.
        :param pulumi.Input[str] engine: The name of the database engine to be used for the neptune instance. Defaults to `neptune`. Valid Values: `neptune`.
        :param pulumi.Input[str] engine_version: The neptune engine version.
        :param pulumi.Input[str] identifier: The indentifier for the neptune instance, if omitted, this provider will assign a random, unique identifier.
        :param pulumi.Input[str] identifier_prefix: Creates a unique identifier beginning with the specified prefix. Conflicts with `identifier`.
        :param pulumi.Input[str] instance_class: The instance class to use.
        :param pulumi.Input[str] kms_key_arn: The ARN for the KMS encryption key if one is set to the neptune cluster.
        :param pulumi.Input[str] neptune_parameter_group_name: The name of the neptune parameter group to associate with this instance.
        :param pulumi.Input[str] neptune_subnet_group_name: A subnet group to associate with this neptune instance. **NOTE:** This must match the `neptune_subnet_group_name` of the attached [`neptune.Cluster`](https://www.terraform.io/docs/providers/aws/r/neptune_cluster.html).
        :param pulumi.Input[float] port: The port on which the DB accepts connections. Defaults to `8182`.
        :param pulumi.Input[str] preferred_backup_window: The daily time range during which automated backups are created if automated backups are enabled. Eg: "04:00-09:00"
        :param pulumi.Input[str] preferred_maintenance_window: The window to perform maintenance in.
               Syntax: "ddd:hh24:mi-ddd:hh24:mi". Eg: "Mon:00:00-Mon:03:00".
        :param pulumi.Input[float] promotion_tier: Default 0. Failover Priority setting on instance level. The reader who has lower tier has higher priority to get promoter to writer.
        :param pulumi.Input[bool] publicly_accessible: Bool to control if instance is publicly accessible. Default is `false`.
        :param pulumi.Input[bool] storage_encrypted: Specifies whether the neptune cluster is encrypted.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the instance.
        :param pulumi.Input[bool] writer: Boolean indicating if this instance is writable. `False` indicates this instance is a read replica.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/neptune_cluster_instance.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["address"] = address
        __props__["apply_immediately"] = apply_immediately
        __props__["arn"] = arn
        __props__["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        __props__["availability_zone"] = availability_zone
        __props__["cluster_identifier"] = cluster_identifier
        __props__["dbi_resource_id"] = dbi_resource_id
        __props__["endpoint"] = endpoint
        __props__["engine"] = engine
        __props__["engine_version"] = engine_version
        __props__["identifier"] = identifier
        __props__["identifier_prefix"] = identifier_prefix
        __props__["instance_class"] = instance_class
        __props__["kms_key_arn"] = kms_key_arn
        __props__["neptune_parameter_group_name"] = neptune_parameter_group_name
        __props__["neptune_subnet_group_name"] = neptune_subnet_group_name
        __props__["port"] = port
        __props__["preferred_backup_window"] = preferred_backup_window
        __props__["preferred_maintenance_window"] = preferred_maintenance_window
        __props__["promotion_tier"] = promotion_tier
        __props__["publicly_accessible"] = publicly_accessible
        __props__["storage_encrypted"] = storage_encrypted
        __props__["tags"] = tags
        __props__["writer"] = writer
        return ClusterInstance(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

