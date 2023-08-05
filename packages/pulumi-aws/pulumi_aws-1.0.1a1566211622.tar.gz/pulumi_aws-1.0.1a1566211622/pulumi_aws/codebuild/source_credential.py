# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class SourceCredential(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN of Source Credential.
    """
    auth_type: pulumi.Output[str]
    """
    The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
    """
    server_type: pulumi.Output[str]
    """
    The source provider used for this project.
    """
    token: pulumi.Output[str]
    """
    For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
    """
    user_name: pulumi.Output[str]
    """
    The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.
    """
    def __init__(__self__, resource_name, opts=None, auth_type=None, server_type=None, token=None, user_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a CodeBuild Source Credentials Resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auth_type: The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
        :param pulumi.Input[str] server_type: The source provider used for this project.
        :param pulumi.Input[str] token: For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
        :param pulumi.Input[str] user_name: The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/codebuild_source_credential.html.markdown.
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

            if auth_type is None:
                raise TypeError("Missing required property 'auth_type'")
            __props__['auth_type'] = auth_type
            if server_type is None:
                raise TypeError("Missing required property 'server_type'")
            __props__['server_type'] = server_type
            if token is None:
                raise TypeError("Missing required property 'token'")
            __props__['token'] = token
            __props__['user_name'] = user_name
            __props__['arn'] = None
        super(SourceCredential, __self__).__init__(
            'aws:codebuild/sourceCredential:SourceCredential',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, auth_type=None, server_type=None, token=None, user_name=None):
        """
        Get an existing SourceCredential resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of Source Credential.
        :param pulumi.Input[str] auth_type: The type of authentication used to connect to a GitHub, GitHub Enterprise, or Bitbucket repository. An OAUTH connection is not supported by the API.
        :param pulumi.Input[str] server_type: The source provider used for this project.
        :param pulumi.Input[str] token: For `GitHub` or `GitHub Enterprise`, this is the personal access token. For `Bitbucket`, this is the app password.
        :param pulumi.Input[str] user_name: The Bitbucket username when the authType is `BASIC_AUTH`. This parameter is not valid for other types of source providers or connections.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/codebuild_source_credential.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["auth_type"] = auth_type
        __props__["server_type"] = server_type
        __props__["token"] = token
        __props__["user_name"] = user_name
        return SourceCredential(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

