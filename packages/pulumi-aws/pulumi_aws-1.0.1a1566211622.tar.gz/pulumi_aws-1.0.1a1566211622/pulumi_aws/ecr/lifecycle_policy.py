# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class LifecyclePolicy(pulumi.CustomResource):
    policy: pulumi.Output[str]
    """
    The policy document. This is a JSON formatted string. See more details about [Policy Parameters](http://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html#lifecycle_policy_parameters) in the official AWS docs.
    """
    registry_id: pulumi.Output[str]
    """
    The registry ID where the repository was created.
    """
    repository: pulumi.Output[str]
    """
    Name of the repository to apply the policy.
    """
    def __init__(__self__, resource_name, opts=None, policy=None, repository=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an ECR repository lifecycle policy.
        
        > **NOTE:** Only one `ecr.LifecyclePolicy` resource can be used with the same ECR repository. To apply multiple rules, they must be combined in the `policy` JSON.
        
        > **NOTE:** The AWS ECR API seems to reorder rules based on `rulePriority`. If you define multiple rules that are not sorted in ascending `rulePriority` order in the this provider code, the resource will be flagged for recreation every deployment.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string. See more details about [Policy Parameters](http://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html#lifecycle_policy_parameters) in the official AWS docs.
        :param pulumi.Input[str] repository: Name of the repository to apply the policy.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/ecr_lifecycle_policy.html.markdown.
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

            if policy is None:
                raise TypeError("Missing required property 'policy'")
            __props__['policy'] = policy
            if repository is None:
                raise TypeError("Missing required property 'repository'")
            __props__['repository'] = repository
            __props__['registry_id'] = None
        super(LifecyclePolicy, __self__).__init__(
            'aws:ecr/lifecyclePolicy:LifecyclePolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, policy=None, registry_id=None, repository=None):
        """
        Get an existing LifecyclePolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string. See more details about [Policy Parameters](http://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html#lifecycle_policy_parameters) in the official AWS docs.
        :param pulumi.Input[str] registry_id: The registry ID where the repository was created.
        :param pulumi.Input[str] repository: Name of the repository to apply the policy.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/ecr_lifecycle_policy.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["policy"] = policy
        __props__["registry_id"] = registry_id
        __props__["repository"] = repository
        return LifecyclePolicy(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

