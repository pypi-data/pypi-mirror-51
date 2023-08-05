# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class UserLoginProfile(pulumi.CustomResource):
    encrypted_password: pulumi.Output[str]
    """
    The encrypted password, base64 encoded. Only available if password was handled on this provider resource creation, not import.
    """
    key_fingerprint: pulumi.Output[str]
    """
    The fingerprint of the PGP key used to encrypt the password. Only available if password was handled on this provider resource creation, not import.
    """
    password_length: pulumi.Output[float]
    """
    The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument.
    """
    password_reset_required: pulumi.Output[bool]
    """
    Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument.
    """
    pgp_key: pulumi.Output[str]
    """
    Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
    """
    user: pulumi.Output[str]
    """
    The IAM user's name.
    """
    def __init__(__self__, resource_name, opts=None, password_length=None, password_reset_required=None, pgp_key=None, user=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an IAM User Login Profile with limited support for password creation during this provider resource creation. Uses PGP to encrypt the password for safe transport to the user. PGP keys can be obtained from Keybase.
        
        > To reset an IAM User login password via this provider, you can use delete and recreate this resource or change any of the arguments.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] password_length: The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument.
        :param pulumi.Input[bool] password_reset_required: Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
        :param pulumi.Input[str] user: The IAM user's name.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/iam_user_login_profile.html.markdown.
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

            __props__['password_length'] = password_length
            __props__['password_reset_required'] = password_reset_required
            if pgp_key is None:
                raise TypeError("Missing required property 'pgp_key'")
            __props__['pgp_key'] = pgp_key
            if user is None:
                raise TypeError("Missing required property 'user'")
            __props__['user'] = user
            __props__['encrypted_password'] = None
            __props__['key_fingerprint'] = None
        super(UserLoginProfile, __self__).__init__(
            'aws:iam/userLoginProfile:UserLoginProfile',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, encrypted_password=None, key_fingerprint=None, password_length=None, password_reset_required=None, pgp_key=None, user=None):
        """
        Get an existing UserLoginProfile resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] encrypted_password: The encrypted password, base64 encoded. Only available if password was handled on this provider resource creation, not import.
        :param pulumi.Input[str] key_fingerprint: The fingerprint of the PGP key used to encrypt the password. Only available if password was handled on this provider resource creation, not import.
        :param pulumi.Input[float] password_length: The length of the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument.
        :param pulumi.Input[bool] password_reset_required: Whether the user should be forced to reset the generated password on resource creation. Only applies on resource creation. Drift detection is not possible with this argument.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:username`. Only applies on resource creation. Drift detection is not possible with this argument.
        :param pulumi.Input[str] user: The IAM user's name.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/iam_user_login_profile.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["encrypted_password"] = encrypted_password
        __props__["key_fingerprint"] = key_fingerprint
        __props__["password_length"] = password_length
        __props__["password_reset_required"] = password_reset_required
        __props__["pgp_key"] = pgp_key
        __props__["user"] = user
        return UserLoginProfile(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

