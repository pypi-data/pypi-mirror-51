# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class PrincipalAssociation(pulumi.CustomResource):
    principal: pulumi.Output[str]
    """
    The principal to associate with the resource share. Possible values are an AWS account ID, an AWS Organizations Organization ARN, or an AWS Organizations Organization Unit ARN.
    """
    resource_share_arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) of the resource share.
    """
    def __init__(__self__, resource_name, opts=None, principal=None, resource_share_arn=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a Resource Access Manager (RAM) principal association.
        
        > *NOTE:* For an AWS Account ID principal, the target account must accept the RAM association invitation after resource creation.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] principal: The principal to associate with the resource share. Possible values are an AWS account ID, an AWS Organizations Organization ARN, or an AWS Organizations Organization Unit ARN.
        :param pulumi.Input[str] resource_share_arn: The Amazon Resource Name (ARN) of the resource share.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/ram_principal_association.html.markdown.
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

            if principal is None:
                raise TypeError("Missing required property 'principal'")
            __props__['principal'] = principal
            if resource_share_arn is None:
                raise TypeError("Missing required property 'resource_share_arn'")
            __props__['resource_share_arn'] = resource_share_arn
        super(PrincipalAssociation, __self__).__init__(
            'aws:ram/principalAssociation:PrincipalAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, principal=None, resource_share_arn=None):
        """
        Get an existing PrincipalAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] principal: The principal to associate with the resource share. Possible values are an AWS account ID, an AWS Organizations Organization ARN, or an AWS Organizations Organization Unit ARN.
        :param pulumi.Input[str] resource_share_arn: The Amazon Resource Name (ARN) of the resource share.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/ram_principal_association.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["principal"] = principal
        __props__["resource_share_arn"] = resource_share_arn
        return PrincipalAssociation(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

