# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class ExternalKey(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) of the key.
    """
    deletion_window_in_days: pulumi.Output[float]
    """
    Duration in days after which the key is deleted after destruction of the resource. Must be between `7` and `30` days. Defaults to `30`.
    """
    description: pulumi.Output[str]
    """
    Description of the key.
    """
    enabled: pulumi.Output[bool]
    """
    Specifies whether the key is enabled. Keys pending import can only be `false`. Imported keys default to `true` unless expired.
    """
    expiration_model: pulumi.Output[str]
    """
    Whether the key material expires. Empty when pending key material import, otherwise `KEY_MATERIAL_EXPIRES` or `KEY_MATERIAL_DOES_NOT_EXPIRE`.
    """
    key_material_base64: pulumi.Output[str]
    """
    Base64 encoded 256-bit symmetric encryption key material to import. The CMK is permanently associated with this key material. The same key material can be reimported, but you cannot import different key material.
    """
    key_state: pulumi.Output[str]
    """
    The state of the CMK.
    """
    key_usage: pulumi.Output[str]
    """
    The cryptographic operations for which you can use the CMK.
    """
    policy: pulumi.Output[str]
    """
    A key policy JSON document. If you do not provide a key policy, AWS KMS attaches a default key policy to the CMK.
    """
    tags: pulumi.Output[dict]
    """
    A key-value map of tags to assign to the key.
    """
    valid_to: pulumi.Output[str]
    """
    Time at which the imported key material expires. When the key material expires, AWS KMS deletes the key material and the CMK becomes unusable. If not specified, key material does not expire. Valid values: [RFC3339 time string](https://tools.ietf.org/html/rfc3339#section-5.8) (`YYYY-MM-DDTHH:MM:SSZ`)
    """
    def __init__(__self__, resource_name, opts=None, deletion_window_in_days=None, description=None, enabled=None, key_material_base64=None, policy=None, tags=None, valid_to=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a KMS Customer Master Key that uses external key material. To instead manage a KMS Customer Master Key where AWS automatically generates and potentially rotates key material, see the [`kms.Key` resource](https://www.terraform.io/docs/providers/aws/r/kms_key.html).
        
        > **Note:** All arguments including the key material will be stored in the raw state as plain-text. [Read more about sensitive data in state](https://www.terraform.io/docs/state/sensitive-data.html).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] deletion_window_in_days: Duration in days after which the key is deleted after destruction of the resource. Must be between `7` and `30` days. Defaults to `30`.
        :param pulumi.Input[str] description: Description of the key.
        :param pulumi.Input[bool] enabled: Specifies whether the key is enabled. Keys pending import can only be `false`. Imported keys default to `true` unless expired.
        :param pulumi.Input[str] key_material_base64: Base64 encoded 256-bit symmetric encryption key material to import. The CMK is permanently associated with this key material. The same key material can be reimported, but you cannot import different key material.
        :param pulumi.Input[str] policy: A key policy JSON document. If you do not provide a key policy, AWS KMS attaches a default key policy to the CMK.
        :param pulumi.Input[dict] tags: A key-value map of tags to assign to the key.
        :param pulumi.Input[str] valid_to: Time at which the imported key material expires. When the key material expires, AWS KMS deletes the key material and the CMK becomes unusable. If not specified, key material does not expire. Valid values: [RFC3339 time string](https://tools.ietf.org/html/rfc3339#section-5.8) (`YYYY-MM-DDTHH:MM:SSZ`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/kms_external_key.html.markdown.
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

            __props__['deletion_window_in_days'] = deletion_window_in_days
            __props__['description'] = description
            __props__['enabled'] = enabled
            __props__['key_material_base64'] = key_material_base64
            __props__['policy'] = policy
            __props__['tags'] = tags
            __props__['valid_to'] = valid_to
            __props__['arn'] = None
            __props__['expiration_model'] = None
            __props__['key_state'] = None
            __props__['key_usage'] = None
        super(ExternalKey, __self__).__init__(
            'aws:kms/externalKey:ExternalKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, deletion_window_in_days=None, description=None, enabled=None, expiration_model=None, key_material_base64=None, key_state=None, key_usage=None, policy=None, tags=None, valid_to=None):
        """
        Get an existing ExternalKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the key.
        :param pulumi.Input[float] deletion_window_in_days: Duration in days after which the key is deleted after destruction of the resource. Must be between `7` and `30` days. Defaults to `30`.
        :param pulumi.Input[str] description: Description of the key.
        :param pulumi.Input[bool] enabled: Specifies whether the key is enabled. Keys pending import can only be `false`. Imported keys default to `true` unless expired.
        :param pulumi.Input[str] expiration_model: Whether the key material expires. Empty when pending key material import, otherwise `KEY_MATERIAL_EXPIRES` or `KEY_MATERIAL_DOES_NOT_EXPIRE`.
        :param pulumi.Input[str] key_material_base64: Base64 encoded 256-bit symmetric encryption key material to import. The CMK is permanently associated with this key material. The same key material can be reimported, but you cannot import different key material.
        :param pulumi.Input[str] key_state: The state of the CMK.
        :param pulumi.Input[str] key_usage: The cryptographic operations for which you can use the CMK.
        :param pulumi.Input[str] policy: A key policy JSON document. If you do not provide a key policy, AWS KMS attaches a default key policy to the CMK.
        :param pulumi.Input[dict] tags: A key-value map of tags to assign to the key.
        :param pulumi.Input[str] valid_to: Time at which the imported key material expires. When the key material expires, AWS KMS deletes the key material and the CMK becomes unusable. If not specified, key material does not expire. Valid values: [RFC3339 time string](https://tools.ietf.org/html/rfc3339#section-5.8) (`YYYY-MM-DDTHH:MM:SSZ`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/kms_external_key.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["deletion_window_in_days"] = deletion_window_in_days
        __props__["description"] = description
        __props__["enabled"] = enabled
        __props__["expiration_model"] = expiration_model
        __props__["key_material_base64"] = key_material_base64
        __props__["key_state"] = key_state
        __props__["key_usage"] = key_usage
        __props__["policy"] = policy
        __props__["tags"] = tags
        __props__["valid_to"] = valid_to
        return ExternalKey(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

