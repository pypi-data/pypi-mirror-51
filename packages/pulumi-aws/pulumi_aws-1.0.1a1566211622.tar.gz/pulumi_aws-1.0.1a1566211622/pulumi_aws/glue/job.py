# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Job(pulumi.CustomResource):
    allocated_capacity: pulumi.Output[float]
    """
    **DEPRECATED** (Optional) The number of AWS Glue data processing units (DPUs) to allocate to this Job. At least 2 DPUs need to be allocated; the default is 10. A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory.
    """
    command: pulumi.Output[dict]
    """
    The command of the job. Defined below.
    """
    connections: pulumi.Output[list]
    """
    The list of connections used for this job.
    """
    default_arguments: pulumi.Output[dict]
    """
    The map of default arguments for this job. You can specify arguments here that your own job-execution script consumes, as well as arguments that AWS Glue itself consumes. For information about how to specify and consume your own Job arguments, see the [Calling AWS Glue APIs in Python](http://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html) topic in the developer guide. For information about the key-value pairs that AWS Glue consumes to set up your job, see the [Special Parameters Used by AWS Glue](http://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-glue-arguments.html) topic in the developer guide.
    """
    description: pulumi.Output[str]
    """
    Description of the job.
    """
    execution_property: pulumi.Output[dict]
    """
    Execution property of the job. Defined below.
    """
    max_capacity: pulumi.Output[float]
    """
    The maximum number of AWS Glue data processing units (DPUs) that can be allocated when this job runs.
    """
    max_retries: pulumi.Output[float]
    """
    The maximum number of times to retry this job if it fails.
    """
    name: pulumi.Output[str]
    """
    The name of the job command. Defaults to `glueetl`
    """
    role_arn: pulumi.Output[str]
    """
    The ARN of the IAM role associated with this job.
    """
    security_configuration: pulumi.Output[str]
    """
    The name of the Security Configuration to be associated with the job. 
    """
    timeout: pulumi.Output[float]
    """
    The job timeout in minutes. The default is 2880 minutes (48 hours).
    """
    def __init__(__self__, resource_name, opts=None, allocated_capacity=None, command=None, connections=None, default_arguments=None, description=None, execution_property=None, max_capacity=None, max_retries=None, name=None, role_arn=None, security_configuration=None, timeout=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a Glue Job resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] allocated_capacity: **DEPRECATED** (Optional) The number of AWS Glue data processing units (DPUs) to allocate to this Job. At least 2 DPUs need to be allocated; the default is 10. A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory.
        :param pulumi.Input[dict] command: The command of the job. Defined below.
        :param pulumi.Input[list] connections: The list of connections used for this job.
        :param pulumi.Input[dict] default_arguments: The map of default arguments for this job. You can specify arguments here that your own job-execution script consumes, as well as arguments that AWS Glue itself consumes. For information about how to specify and consume your own Job arguments, see the [Calling AWS Glue APIs in Python](http://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html) topic in the developer guide. For information about the key-value pairs that AWS Glue consumes to set up your job, see the [Special Parameters Used by AWS Glue](http://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-glue-arguments.html) topic in the developer guide.
        :param pulumi.Input[str] description: Description of the job.
        :param pulumi.Input[dict] execution_property: Execution property of the job. Defined below.
        :param pulumi.Input[float] max_capacity: The maximum number of AWS Glue data processing units (DPUs) that can be allocated when this job runs.
        :param pulumi.Input[float] max_retries: The maximum number of times to retry this job if it fails.
        :param pulumi.Input[str] name: The name of the job command. Defaults to `glueetl`
        :param pulumi.Input[str] role_arn: The ARN of the IAM role associated with this job.
        :param pulumi.Input[str] security_configuration: The name of the Security Configuration to be associated with the job. 
        :param pulumi.Input[float] timeout: The job timeout in minutes. The default is 2880 minutes (48 hours).

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/glue_job.html.markdown.
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

            __props__['allocated_capacity'] = allocated_capacity
            if command is None:
                raise TypeError("Missing required property 'command'")
            __props__['command'] = command
            __props__['connections'] = connections
            __props__['default_arguments'] = default_arguments
            __props__['description'] = description
            __props__['execution_property'] = execution_property
            __props__['max_capacity'] = max_capacity
            __props__['max_retries'] = max_retries
            __props__['name'] = name
            if role_arn is None:
                raise TypeError("Missing required property 'role_arn'")
            __props__['role_arn'] = role_arn
            __props__['security_configuration'] = security_configuration
            __props__['timeout'] = timeout
        super(Job, __self__).__init__(
            'aws:glue/job:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, allocated_capacity=None, command=None, connections=None, default_arguments=None, description=None, execution_property=None, max_capacity=None, max_retries=None, name=None, role_arn=None, security_configuration=None, timeout=None):
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] allocated_capacity: **DEPRECATED** (Optional) The number of AWS Glue data processing units (DPUs) to allocate to this Job. At least 2 DPUs need to be allocated; the default is 10. A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory.
        :param pulumi.Input[dict] command: The command of the job. Defined below.
        :param pulumi.Input[list] connections: The list of connections used for this job.
        :param pulumi.Input[dict] default_arguments: The map of default arguments for this job. You can specify arguments here that your own job-execution script consumes, as well as arguments that AWS Glue itself consumes. For information about how to specify and consume your own Job arguments, see the [Calling AWS Glue APIs in Python](http://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html) topic in the developer guide. For information about the key-value pairs that AWS Glue consumes to set up your job, see the [Special Parameters Used by AWS Glue](http://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-glue-arguments.html) topic in the developer guide.
        :param pulumi.Input[str] description: Description of the job.
        :param pulumi.Input[dict] execution_property: Execution property of the job. Defined below.
        :param pulumi.Input[float] max_capacity: The maximum number of AWS Glue data processing units (DPUs) that can be allocated when this job runs.
        :param pulumi.Input[float] max_retries: The maximum number of times to retry this job if it fails.
        :param pulumi.Input[str] name: The name of the job command. Defaults to `glueetl`
        :param pulumi.Input[str] role_arn: The ARN of the IAM role associated with this job.
        :param pulumi.Input[str] security_configuration: The name of the Security Configuration to be associated with the job. 
        :param pulumi.Input[float] timeout: The job timeout in minutes. The default is 2880 minutes (48 hours).

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/glue_job.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["allocated_capacity"] = allocated_capacity
        __props__["command"] = command
        __props__["connections"] = connections
        __props__["default_arguments"] = default_arguments
        __props__["description"] = description
        __props__["execution_property"] = execution_property
        __props__["max_capacity"] = max_capacity
        __props__["max_retries"] = max_retries
        __props__["name"] = name
        __props__["role_arn"] = role_arn
        __props__["security_configuration"] = security_configuration
        __props__["timeout"] = timeout
        return Job(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

