# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Webhook(pulumi.CustomResource):
    authentication: pulumi.Output[str]
    """
    The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
    """
    authentication_configuration: pulumi.Output[dict]
    """
    An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
    """
    filters: pulumi.Output[list]
    """
    One or more `filter` blocks. Filter blocks are documented below.
    """
    name: pulumi.Output[str]
    """
    The name of the webhook.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    target_action: pulumi.Output[str]
    """
    The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
    """
    target_pipeline: pulumi.Output[str]
    """
    The name of the pipeline.
    """
    url: pulumi.Output[str]
    """
    The CodePipeline webhook's URL. POST events to this endpoint to trigger the target.
    """
    def __init__(__self__, resource_name, opts=None, authentication=None, authentication_configuration=None, filters=None, name=None, tags=None, target_action=None, target_pipeline=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a CodePipeline Webhook.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication: The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
        :param pulumi.Input[dict] authentication_configuration: An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
        :param pulumi.Input[list] filters: One or more `filter` blocks. Filter blocks are documented below.
        :param pulumi.Input[str] name: The name of the webhook.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] target_action: The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        :param pulumi.Input[str] target_pipeline: The name of the pipeline.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/codepipeline_webhook.html.markdown.
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

            if authentication is None:
                raise TypeError("Missing required property 'authentication'")
            __props__['authentication'] = authentication
            __props__['authentication_configuration'] = authentication_configuration
            if filters is None:
                raise TypeError("Missing required property 'filters'")
            __props__['filters'] = filters
            __props__['name'] = name
            __props__['tags'] = tags
            if target_action is None:
                raise TypeError("Missing required property 'target_action'")
            __props__['target_action'] = target_action
            if target_pipeline is None:
                raise TypeError("Missing required property 'target_pipeline'")
            __props__['target_pipeline'] = target_pipeline
            __props__['url'] = None
        super(Webhook, __self__).__init__(
            'aws:codepipeline/webhook:Webhook',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, authentication=None, authentication_configuration=None, filters=None, name=None, tags=None, target_action=None, target_pipeline=None, url=None):
        """
        Get an existing Webhook resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication: The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
        :param pulumi.Input[dict] authentication_configuration: An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
        :param pulumi.Input[list] filters: One or more `filter` blocks. Filter blocks are documented below.
        :param pulumi.Input[str] name: The name of the webhook.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] target_action: The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        :param pulumi.Input[str] target_pipeline: The name of the pipeline.
        :param pulumi.Input[str] url: The CodePipeline webhook's URL. POST events to this endpoint to trigger the target.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/codepipeline_webhook.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["authentication"] = authentication
        __props__["authentication_configuration"] = authentication_configuration
        __props__["filters"] = filters
        __props__["name"] = name
        __props__["tags"] = tags
        __props__["target_action"] = target_action
        __props__["target_pipeline"] = target_pipeline
        __props__["url"] = url
        return Webhook(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

