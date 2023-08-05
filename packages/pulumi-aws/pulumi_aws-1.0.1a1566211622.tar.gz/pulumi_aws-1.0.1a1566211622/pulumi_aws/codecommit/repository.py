# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Repository(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN of the repository
    """
    clone_url_http: pulumi.Output[str]
    """
    The URL to use for cloning the repository over HTTPS.
    """
    clone_url_ssh: pulumi.Output[str]
    """
    The URL to use for cloning the repository over SSH.
    """
    default_branch: pulumi.Output[str]
    """
    The default branch of the repository. The branch specified here needs to exist.
    """
    description: pulumi.Output[str]
    """
    The description of the repository. This needs to be less than 1000 characters
    """
    repository_id: pulumi.Output[str]
    """
    The ID of the repository
    """
    repository_name: pulumi.Output[str]
    """
    The name for the repository. This needs to be less than 100 characters.
    """
    tags: pulumi.Output[dict]
    """
    Key-value mapping of resource tags
    """
    def __init__(__self__, resource_name, opts=None, default_branch=None, description=None, repository_name=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a CodeCommit Repository Resource.
        
        > **NOTE on CodeCommit Availability**: The CodeCommit is not yet rolled out
        in all regions - available regions are listed
        [the AWS Docs](https://docs.aws.amazon.com/general/latest/gr/rande.html#codecommit_region).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_branch: The default branch of the repository. The branch specified here needs to exist.
        :param pulumi.Input[str] description: The description of the repository. This needs to be less than 1000 characters
        :param pulumi.Input[str] repository_name: The name for the repository. This needs to be less than 100 characters.
        :param pulumi.Input[dict] tags: Key-value mapping of resource tags

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/codecommit_repository.html.markdown.
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

            __props__['default_branch'] = default_branch
            __props__['description'] = description
            if repository_name is None:
                raise TypeError("Missing required property 'repository_name'")
            __props__['repository_name'] = repository_name
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['clone_url_http'] = None
            __props__['clone_url_ssh'] = None
            __props__['repository_id'] = None
        super(Repository, __self__).__init__(
            'aws:codecommit/repository:Repository',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, clone_url_http=None, clone_url_ssh=None, default_branch=None, description=None, repository_id=None, repository_name=None, tags=None):
        """
        Get an existing Repository resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the repository
        :param pulumi.Input[str] clone_url_http: The URL to use for cloning the repository over HTTPS.
        :param pulumi.Input[str] clone_url_ssh: The URL to use for cloning the repository over SSH.
        :param pulumi.Input[str] default_branch: The default branch of the repository. The branch specified here needs to exist.
        :param pulumi.Input[str] description: The description of the repository. This needs to be less than 1000 characters
        :param pulumi.Input[str] repository_id: The ID of the repository
        :param pulumi.Input[str] repository_name: The name for the repository. This needs to be less than 100 characters.
        :param pulumi.Input[dict] tags: Key-value mapping of resource tags

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/codecommit_repository.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["clone_url_http"] = clone_url_http
        __props__["clone_url_ssh"] = clone_url_ssh
        __props__["default_branch"] = default_branch
        __props__["description"] = description
        __props__["repository_id"] = repository_id
        __props__["repository_name"] = repository_name
        __props__["tags"] = tags
        return Repository(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

