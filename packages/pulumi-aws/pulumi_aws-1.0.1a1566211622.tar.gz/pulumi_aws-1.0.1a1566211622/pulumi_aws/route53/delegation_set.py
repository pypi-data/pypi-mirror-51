# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class DelegationSet(pulumi.CustomResource):
    name_servers: pulumi.Output[list]
    """
    A list of authoritative name servers for the hosted zone
    (effectively a list of NS records).
    """
    reference_name: pulumi.Output[str]
    """
    This is a reference name used in Caller Reference
    (helpful for identifying single delegation set amongst others)
    """
    def __init__(__self__, resource_name, opts=None, reference_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a [Route53 Delegation Set](https://docs.aws.amazon.com/Route53/latest/APIReference/API-actions-by-function.html#actions-by-function-reusable-delegation-sets) resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] reference_name: This is a reference name used in Caller Reference
               (helpful for identifying single delegation set amongst others)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/route53_delegation_set.html.markdown.
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

            __props__['reference_name'] = reference_name
            __props__['name_servers'] = None
        super(DelegationSet, __self__).__init__(
            'aws:route53/delegationSet:DelegationSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, name_servers=None, reference_name=None):
        """
        Get an existing DelegationSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] name_servers: A list of authoritative name servers for the hosted zone
               (effectively a list of NS records).
        :param pulumi.Input[str] reference_name: This is a reference name used in Caller Reference
               (helpful for identifying single delegation set amongst others)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/route53_delegation_set.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["name_servers"] = name_servers
        __props__["reference_name"] = reference_name
        return DelegationSet(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

