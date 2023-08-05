# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Instance(pulumi.CustomResource):
    ami: pulumi.Output[str]
    """
    The AMI to use for the instance.
    """
    arn: pulumi.Output[str]
    """
    The ARN of the instance.
    """
    associate_public_ip_address: pulumi.Output[bool]
    """
    Associate a public ip address with an instance in a VPC.  Boolean value.
    """
    availability_zone: pulumi.Output[str]
    """
    The AZ to start the instance in.
    """
    cpu_core_count: pulumi.Output[float]
    """
    Sets the number of CPU cores for an instance. This option is
    only supported on creation of instance type that support CPU Options
    [CPU Cores and Threads Per CPU Core Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html#cpu-options-supported-instances-values) - specifying this option for unsupported instance types will return an error from the EC2 API.
    """
    cpu_threads_per_core: pulumi.Output[float]
    """
    If set to to 1, hyperthreading is disabled on the launched instance. Defaults to 2 if not set. See [Optimizing CPU Options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html) for more information.
    """
    credit_specification: pulumi.Output[dict]
    """
    Customize the credit specification of the instance. See Credit Specification below for more details.
    """
    disable_api_termination: pulumi.Output[bool]
    """
    If true, enables [EC2 Instance
    Termination Protection](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingDisableAPITermination)
    """
    ebs_block_devices: pulumi.Output[list]
    """
    Additional EBS block devices to attach to the
    instance.  Block device configurations only apply on resource creation. See Block Devices below for details on attributes and drift detection.
    """
    ebs_optimized: pulumi.Output[bool]
    """
    If true, the launched EC2 instance will be EBS-optimized.
    Note that if this is not set on an instance type that is optimized by default then
    this will show as disabled but if the instance type is optimized by default then
    there is no need to set this and there is no effect to disabling it.
    See the [EBS Optimized section](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSOptimized.html) of the AWS User Guide for more information.
    """
    ephemeral_block_devices: pulumi.Output[list]
    """
    Customize Ephemeral (also known as
    "Instance Store") volumes on the instance. See Block Devices below for details.
    """
    get_password_data: pulumi.Output[bool]
    """
    If true, wait for password data to become available and retrieve it. Useful for getting the administrator password for instances running Microsoft Windows. The password data is exported to the `password_data` attribute. See [GetPasswordData](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetPasswordData.html) for more information.
    """
    host_id: pulumi.Output[str]
    """
    The Id of a dedicated host that the instance will be assigned to. Use when an instance is to be launched on a specific dedicated host.
    """
    iam_instance_profile: pulumi.Output[str]
    """
    The IAM Instance Profile to
    launch the instance with. Specified as the name of the Instance Profile. Ensure your credentials have the correct permission to assign the instance profile according to the [EC2 documentation](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html#roles-usingrole-ec2instance-permissions), notably `iam:PassRole`.
    * `ipv6_address_count`- (Optional) A number of IPv6 addresses to associate with the primary network interface. Amazon EC2 chooses the IPv6 addresses from the range of your subnet.
    """
    instance_initiated_shutdown_behavior: pulumi.Output[str]
    """
    Shutdown behavior for the
    instance. Amazon defaults this to `stop` for EBS-backed instances and
    `terminate` for instance-store instances. Cannot be set on instance-store
    instances. See [Shutdown Behavior](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingInstanceInitiatedShutdownBehavior) for more information.
    """
    instance_state: pulumi.Output[str]
    """
    The state of the instance. One of: `pending`, `running`, `shutting-down`, `terminated`, `stopping`, `stopped`. See [Instance Lifecycle](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html) for more information.
    """
    instance_type: pulumi.Output[str]
    """
    The type of instance to start. Updates to this field will trigger a stop/start of the EC2 instance.
    """
    ipv6_address_count: pulumi.Output[float]
    ipv6_addresses: pulumi.Output[list]
    """
    Specify one or more IPv6 addresses from the range of the subnet to associate with the primary network interface
    """
    key_name: pulumi.Output[str]
    """
    The key name of the Key Pair to use for the instance; which can be managed using the `ec2.KeyPair` resource.
    """
    monitoring: pulumi.Output[bool]
    """
    If true, the launched EC2 instance will have detailed monitoring enabled. (Available since v0.6.0)
    """
    network_interfaces: pulumi.Output[list]
    """
    Customize network interfaces to be attached at instance boot time. See Network Interfaces below for more details.
    """
    password_data: pulumi.Output[str]
    """
    Base-64 encoded encrypted password data for the instance.
    Useful for getting the administrator password for instances running Microsoft Windows.
    This attribute is only exported if `get_password_data` is true.
    Note that this encrypted value will be stored in the state file, as with all exported attributes.
    See [GetPasswordData](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetPasswordData.html) for more information.
    """
    placement_group: pulumi.Output[str]
    """
    The Placement Group to start the instance in.
    """
    primary_network_interface_id: pulumi.Output[str]
    """
    The ID of the instance's primary network interface.
    """
    private_dns: pulumi.Output[str]
    """
    The private DNS name assigned to the instance. Can only be
    used inside the Amazon EC2, and only available if you've enabled DNS hostnames
    for your VPC
    """
    private_ip: pulumi.Output[str]
    """
    Private IP address to associate with the
    instance in a VPC.
    """
    public_dns: pulumi.Output[str]
    """
    The public DNS name assigned to the instance. For EC2-VPC, this
    is only available if you've enabled DNS hostnames for your VPC
    """
    public_ip: pulumi.Output[str]
    """
    The public IP address assigned to the instance, if applicable. **NOTE**: If you are using an [`ec2.Eip`](https://www.terraform.io/docs/providers/aws/r/eip.html) with your instance, you should refer to the EIP's address directly and not use `public_ip`, as this field will change after the EIP is attached.
    """
    root_block_device: pulumi.Output[dict]
    """
    Customize details about the root block
    device of the instance. See Block Devices below for details.
    """
    security_groups: pulumi.Output[list]
    """
    A list of security group names (EC2-Classic) or IDs (default VPC) to associate with.
    """
    source_dest_check: pulumi.Output[bool]
    """
    Controls if traffic is routed to the instance when
    the destination address does not match the instance. Used for NAT or VPNs. Defaults true.
    """
    subnet_id: pulumi.Output[str]
    """
    The VPC Subnet ID to launch in.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    tenancy: pulumi.Output[str]
    """
    The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of dedicated runs on single-tenant hardware. The host tenancy is not supported for the import-instance command.
    """
    user_data: pulumi.Output[str]
    """
    The user data to provide when launching the instance. Do not pass gzip-compressed data via this argument; see `user_data_base64` instead.
    """
    user_data_base64: pulumi.Output[str]
    """
    Can be used instead of `user_data` to pass base64-encoded binary data directly. Use this instead of `user_data` whenever the value is not a valid UTF-8 string. For example, gzip-encoded user data must be base64-encoded and passed via this argument to avoid corruption.
    """
    volume_tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the devices created by the instance at launch time.
    """
    vpc_security_group_ids: pulumi.Output[list]
    """
    A list of security group IDs to associate with.
    """
    def __init__(__self__, resource_name, opts=None, ami=None, associate_public_ip_address=None, availability_zone=None, cpu_core_count=None, cpu_threads_per_core=None, credit_specification=None, disable_api_termination=None, ebs_block_devices=None, ebs_optimized=None, ephemeral_block_devices=None, get_password_data=None, host_id=None, iam_instance_profile=None, instance_initiated_shutdown_behavior=None, instance_type=None, ipv6_address_count=None, ipv6_addresses=None, key_name=None, monitoring=None, network_interfaces=None, placement_group=None, private_ip=None, root_block_device=None, security_groups=None, source_dest_check=None, subnet_id=None, tags=None, tenancy=None, user_data=None, user_data_base64=None, volume_tags=None, vpc_security_group_ids=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an EC2 instance resource. This allows instances to be created, updated,
        and deleted. Instances also support [provisioning](https://www.terraform.io/docs/provisioners/index.html).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ami: The AMI to use for the instance.
        :param pulumi.Input[bool] associate_public_ip_address: Associate a public ip address with an instance in a VPC.  Boolean value.
        :param pulumi.Input[str] availability_zone: The AZ to start the instance in.
        :param pulumi.Input[float] cpu_core_count: Sets the number of CPU cores for an instance. This option is
               only supported on creation of instance type that support CPU Options
               [CPU Cores and Threads Per CPU Core Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html#cpu-options-supported-instances-values) - specifying this option for unsupported instance types will return an error from the EC2 API.
        :param pulumi.Input[float] cpu_threads_per_core: If set to to 1, hyperthreading is disabled on the launched instance. Defaults to 2 if not set. See [Optimizing CPU Options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html) for more information.
        :param pulumi.Input[dict] credit_specification: Customize the credit specification of the instance. See Credit Specification below for more details.
        :param pulumi.Input[bool] disable_api_termination: If true, enables [EC2 Instance
               Termination Protection](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingDisableAPITermination)
        :param pulumi.Input[list] ebs_block_devices: Additional EBS block devices to attach to the
               instance.  Block device configurations only apply on resource creation. See Block Devices below for details on attributes and drift detection.
        :param pulumi.Input[bool] ebs_optimized: If true, the launched EC2 instance will be EBS-optimized.
               Note that if this is not set on an instance type that is optimized by default then
               this will show as disabled but if the instance type is optimized by default then
               there is no need to set this and there is no effect to disabling it.
               See the [EBS Optimized section](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSOptimized.html) of the AWS User Guide for more information.
        :param pulumi.Input[list] ephemeral_block_devices: Customize Ephemeral (also known as
               "Instance Store") volumes on the instance. See Block Devices below for details.
        :param pulumi.Input[bool] get_password_data: If true, wait for password data to become available and retrieve it. Useful for getting the administrator password for instances running Microsoft Windows. The password data is exported to the `password_data` attribute. See [GetPasswordData](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetPasswordData.html) for more information.
        :param pulumi.Input[str] host_id: The Id of a dedicated host that the instance will be assigned to. Use when an instance is to be launched on a specific dedicated host.
        :param pulumi.Input[str] iam_instance_profile: The IAM Instance Profile to
               launch the instance with. Specified as the name of the Instance Profile. Ensure your credentials have the correct permission to assign the instance profile according to the [EC2 documentation](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html#roles-usingrole-ec2instance-permissions), notably `iam:PassRole`.
               * `ipv6_address_count`- (Optional) A number of IPv6 addresses to associate with the primary network interface. Amazon EC2 chooses the IPv6 addresses from the range of your subnet.
        :param pulumi.Input[str] instance_initiated_shutdown_behavior: Shutdown behavior for the
               instance. Amazon defaults this to `stop` for EBS-backed instances and
               `terminate` for instance-store instances. Cannot be set on instance-store
               instances. See [Shutdown Behavior](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingInstanceInitiatedShutdownBehavior) for more information.
        :param pulumi.Input[str] instance_type: The type of instance to start. Updates to this field will trigger a stop/start of the EC2 instance.
        :param pulumi.Input[list] ipv6_addresses: Specify one or more IPv6 addresses from the range of the subnet to associate with the primary network interface
        :param pulumi.Input[str] key_name: The key name of the Key Pair to use for the instance; which can be managed using the `ec2.KeyPair` resource.
        :param pulumi.Input[bool] monitoring: If true, the launched EC2 instance will have detailed monitoring enabled. (Available since v0.6.0)
        :param pulumi.Input[list] network_interfaces: Customize network interfaces to be attached at instance boot time. See Network Interfaces below for more details.
        :param pulumi.Input[str] placement_group: The Placement Group to start the instance in.
        :param pulumi.Input[str] private_ip: Private IP address to associate with the
               instance in a VPC.
        :param pulumi.Input[dict] root_block_device: Customize details about the root block
               device of the instance. See Block Devices below for details.
        :param pulumi.Input[list] security_groups: A list of security group names (EC2-Classic) or IDs (default VPC) to associate with.
        :param pulumi.Input[bool] source_dest_check: Controls if traffic is routed to the instance when
               the destination address does not match the instance. Used for NAT or VPNs. Defaults true.
        :param pulumi.Input[str] subnet_id: The VPC Subnet ID to launch in.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] tenancy: The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of dedicated runs on single-tenant hardware. The host tenancy is not supported for the import-instance command.
        :param pulumi.Input[str] user_data: The user data to provide when launching the instance. Do not pass gzip-compressed data via this argument; see `user_data_base64` instead.
        :param pulumi.Input[str] user_data_base64: Can be used instead of `user_data` to pass base64-encoded binary data directly. Use this instead of `user_data` whenever the value is not a valid UTF-8 string. For example, gzip-encoded user data must be base64-encoded and passed via this argument to avoid corruption.
        :param pulumi.Input[dict] volume_tags: A mapping of tags to assign to the devices created by the instance at launch time.
        :param pulumi.Input[list] vpc_security_group_ids: A list of security group IDs to associate with.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/instance.html.markdown.
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

            if ami is None:
                raise TypeError("Missing required property 'ami'")
            __props__['ami'] = ami
            __props__['associate_public_ip_address'] = associate_public_ip_address
            __props__['availability_zone'] = availability_zone
            __props__['cpu_core_count'] = cpu_core_count
            __props__['cpu_threads_per_core'] = cpu_threads_per_core
            __props__['credit_specification'] = credit_specification
            __props__['disable_api_termination'] = disable_api_termination
            __props__['ebs_block_devices'] = ebs_block_devices
            __props__['ebs_optimized'] = ebs_optimized
            __props__['ephemeral_block_devices'] = ephemeral_block_devices
            __props__['get_password_data'] = get_password_data
            __props__['host_id'] = host_id
            __props__['iam_instance_profile'] = iam_instance_profile
            __props__['instance_initiated_shutdown_behavior'] = instance_initiated_shutdown_behavior
            if instance_type is None:
                raise TypeError("Missing required property 'instance_type'")
            __props__['instance_type'] = instance_type
            __props__['ipv6_address_count'] = ipv6_address_count
            __props__['ipv6_addresses'] = ipv6_addresses
            __props__['key_name'] = key_name
            __props__['monitoring'] = monitoring
            __props__['network_interfaces'] = network_interfaces
            __props__['placement_group'] = placement_group
            __props__['private_ip'] = private_ip
            __props__['root_block_device'] = root_block_device
            __props__['security_groups'] = security_groups
            __props__['source_dest_check'] = source_dest_check
            __props__['subnet_id'] = subnet_id
            __props__['tags'] = tags
            __props__['tenancy'] = tenancy
            __props__['user_data'] = user_data
            __props__['user_data_base64'] = user_data_base64
            __props__['volume_tags'] = volume_tags
            __props__['vpc_security_group_ids'] = vpc_security_group_ids
            __props__['arn'] = None
            __props__['instance_state'] = None
            __props__['password_data'] = None
            __props__['primary_network_interface_id'] = None
            __props__['private_dns'] = None
            __props__['public_dns'] = None
            __props__['public_ip'] = None
        super(Instance, __self__).__init__(
            'aws:ec2/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, ami=None, arn=None, associate_public_ip_address=None, availability_zone=None, cpu_core_count=None, cpu_threads_per_core=None, credit_specification=None, disable_api_termination=None, ebs_block_devices=None, ebs_optimized=None, ephemeral_block_devices=None, get_password_data=None, host_id=None, iam_instance_profile=None, instance_initiated_shutdown_behavior=None, instance_state=None, instance_type=None, ipv6_address_count=None, ipv6_addresses=None, key_name=None, monitoring=None, network_interfaces=None, password_data=None, placement_group=None, primary_network_interface_id=None, private_dns=None, private_ip=None, public_dns=None, public_ip=None, root_block_device=None, security_groups=None, source_dest_check=None, subnet_id=None, tags=None, tenancy=None, user_data=None, user_data_base64=None, volume_tags=None, vpc_security_group_ids=None):
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ami: The AMI to use for the instance.
        :param pulumi.Input[str] arn: The ARN of the instance.
        :param pulumi.Input[bool] associate_public_ip_address: Associate a public ip address with an instance in a VPC.  Boolean value.
        :param pulumi.Input[str] availability_zone: The AZ to start the instance in.
        :param pulumi.Input[float] cpu_core_count: Sets the number of CPU cores for an instance. This option is
               only supported on creation of instance type that support CPU Options
               [CPU Cores and Threads Per CPU Core Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html#cpu-options-supported-instances-values) - specifying this option for unsupported instance types will return an error from the EC2 API.
        :param pulumi.Input[float] cpu_threads_per_core: If set to to 1, hyperthreading is disabled on the launched instance. Defaults to 2 if not set. See [Optimizing CPU Options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html) for more information.
        :param pulumi.Input[dict] credit_specification: Customize the credit specification of the instance. See Credit Specification below for more details.
        :param pulumi.Input[bool] disable_api_termination: If true, enables [EC2 Instance
               Termination Protection](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingDisableAPITermination)
        :param pulumi.Input[list] ebs_block_devices: Additional EBS block devices to attach to the
               instance.  Block device configurations only apply on resource creation. See Block Devices below for details on attributes and drift detection.
        :param pulumi.Input[bool] ebs_optimized: If true, the launched EC2 instance will be EBS-optimized.
               Note that if this is not set on an instance type that is optimized by default then
               this will show as disabled but if the instance type is optimized by default then
               there is no need to set this and there is no effect to disabling it.
               See the [EBS Optimized section](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSOptimized.html) of the AWS User Guide for more information.
        :param pulumi.Input[list] ephemeral_block_devices: Customize Ephemeral (also known as
               "Instance Store") volumes on the instance. See Block Devices below for details.
        :param pulumi.Input[bool] get_password_data: If true, wait for password data to become available and retrieve it. Useful for getting the administrator password for instances running Microsoft Windows. The password data is exported to the `password_data` attribute. See [GetPasswordData](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetPasswordData.html) for more information.
        :param pulumi.Input[str] host_id: The Id of a dedicated host that the instance will be assigned to. Use when an instance is to be launched on a specific dedicated host.
        :param pulumi.Input[str] iam_instance_profile: The IAM Instance Profile to
               launch the instance with. Specified as the name of the Instance Profile. Ensure your credentials have the correct permission to assign the instance profile according to the [EC2 documentation](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html#roles-usingrole-ec2instance-permissions), notably `iam:PassRole`.
               * `ipv6_address_count`- (Optional) A number of IPv6 addresses to associate with the primary network interface. Amazon EC2 chooses the IPv6 addresses from the range of your subnet.
        :param pulumi.Input[str] instance_initiated_shutdown_behavior: Shutdown behavior for the
               instance. Amazon defaults this to `stop` for EBS-backed instances and
               `terminate` for instance-store instances. Cannot be set on instance-store
               instances. See [Shutdown Behavior](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingInstanceInitiatedShutdownBehavior) for more information.
        :param pulumi.Input[str] instance_state: The state of the instance. One of: `pending`, `running`, `shutting-down`, `terminated`, `stopping`, `stopped`. See [Instance Lifecycle](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html) for more information.
        :param pulumi.Input[str] instance_type: The type of instance to start. Updates to this field will trigger a stop/start of the EC2 instance.
        :param pulumi.Input[list] ipv6_addresses: Specify one or more IPv6 addresses from the range of the subnet to associate with the primary network interface
        :param pulumi.Input[str] key_name: The key name of the Key Pair to use for the instance; which can be managed using the `ec2.KeyPair` resource.
        :param pulumi.Input[bool] monitoring: If true, the launched EC2 instance will have detailed monitoring enabled. (Available since v0.6.0)
        :param pulumi.Input[list] network_interfaces: Customize network interfaces to be attached at instance boot time. See Network Interfaces below for more details.
        :param pulumi.Input[str] password_data: Base-64 encoded encrypted password data for the instance.
               Useful for getting the administrator password for instances running Microsoft Windows.
               This attribute is only exported if `get_password_data` is true.
               Note that this encrypted value will be stored in the state file, as with all exported attributes.
               See [GetPasswordData](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetPasswordData.html) for more information.
        :param pulumi.Input[str] placement_group: The Placement Group to start the instance in.
        :param pulumi.Input[str] primary_network_interface_id: The ID of the instance's primary network interface.
        :param pulumi.Input[str] private_dns: The private DNS name assigned to the instance. Can only be
               used inside the Amazon EC2, and only available if you've enabled DNS hostnames
               for your VPC
        :param pulumi.Input[str] private_ip: Private IP address to associate with the
               instance in a VPC.
        :param pulumi.Input[str] public_dns: The public DNS name assigned to the instance. For EC2-VPC, this
               is only available if you've enabled DNS hostnames for your VPC
        :param pulumi.Input[str] public_ip: The public IP address assigned to the instance, if applicable. **NOTE**: If you are using an [`ec2.Eip`](https://www.terraform.io/docs/providers/aws/r/eip.html) with your instance, you should refer to the EIP's address directly and not use `public_ip`, as this field will change after the EIP is attached.
        :param pulumi.Input[dict] root_block_device: Customize details about the root block
               device of the instance. See Block Devices below for details.
        :param pulumi.Input[list] security_groups: A list of security group names (EC2-Classic) or IDs (default VPC) to associate with.
        :param pulumi.Input[bool] source_dest_check: Controls if traffic is routed to the instance when
               the destination address does not match the instance. Used for NAT or VPNs. Defaults true.
        :param pulumi.Input[str] subnet_id: The VPC Subnet ID to launch in.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] tenancy: The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of dedicated runs on single-tenant hardware. The host tenancy is not supported for the import-instance command.
        :param pulumi.Input[str] user_data: The user data to provide when launching the instance. Do not pass gzip-compressed data via this argument; see `user_data_base64` instead.
        :param pulumi.Input[str] user_data_base64: Can be used instead of `user_data` to pass base64-encoded binary data directly. Use this instead of `user_data` whenever the value is not a valid UTF-8 string. For example, gzip-encoded user data must be base64-encoded and passed via this argument to avoid corruption.
        :param pulumi.Input[dict] volume_tags: A mapping of tags to assign to the devices created by the instance at launch time.
        :param pulumi.Input[list] vpc_security_group_ids: A list of security group IDs to associate with.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/instance.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["ami"] = ami
        __props__["arn"] = arn
        __props__["associate_public_ip_address"] = associate_public_ip_address
        __props__["availability_zone"] = availability_zone
        __props__["cpu_core_count"] = cpu_core_count
        __props__["cpu_threads_per_core"] = cpu_threads_per_core
        __props__["credit_specification"] = credit_specification
        __props__["disable_api_termination"] = disable_api_termination
        __props__["ebs_block_devices"] = ebs_block_devices
        __props__["ebs_optimized"] = ebs_optimized
        __props__["ephemeral_block_devices"] = ephemeral_block_devices
        __props__["get_password_data"] = get_password_data
        __props__["host_id"] = host_id
        __props__["iam_instance_profile"] = iam_instance_profile
        __props__["instance_initiated_shutdown_behavior"] = instance_initiated_shutdown_behavior
        __props__["instance_state"] = instance_state
        __props__["instance_type"] = instance_type
        __props__["ipv6_address_count"] = ipv6_address_count
        __props__["ipv6_addresses"] = ipv6_addresses
        __props__["key_name"] = key_name
        __props__["monitoring"] = monitoring
        __props__["network_interfaces"] = network_interfaces
        __props__["password_data"] = password_data
        __props__["placement_group"] = placement_group
        __props__["primary_network_interface_id"] = primary_network_interface_id
        __props__["private_dns"] = private_dns
        __props__["private_ip"] = private_ip
        __props__["public_dns"] = public_dns
        __props__["public_ip"] = public_ip
        __props__["root_block_device"] = root_block_device
        __props__["security_groups"] = security_groups
        __props__["source_dest_check"] = source_dest_check
        __props__["subnet_id"] = subnet_id
        __props__["tags"] = tags
        __props__["tenancy"] = tenancy
        __props__["user_data"] = user_data
        __props__["user_data_base64"] = user_data_base64
        __props__["volume_tags"] = volume_tags
        __props__["vpc_security_group_ids"] = vpc_security_group_ids
        return Instance(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

