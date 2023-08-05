# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetTableResult:
    """
    A collection of values returned by getTable.
    """
    def __init__(__self__, arn=None, attributes=None, billing_mode=None, global_secondary_indexes=None, hash_key=None, local_secondary_indexes=None, name=None, point_in_time_recovery=None, range_key=None, read_capacity=None, server_side_encryption=None, stream_arn=None, stream_enabled=None, stream_label=None, stream_view_type=None, tags=None, ttl=None, write_capacity=None, id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        __self__.arn = arn
        if attributes and not isinstance(attributes, list):
            raise TypeError("Expected argument 'attributes' to be a list")
        __self__.attributes = attributes
        if billing_mode and not isinstance(billing_mode, str):
            raise TypeError("Expected argument 'billing_mode' to be a str")
        __self__.billing_mode = billing_mode
        if global_secondary_indexes and not isinstance(global_secondary_indexes, list):
            raise TypeError("Expected argument 'global_secondary_indexes' to be a list")
        __self__.global_secondary_indexes = global_secondary_indexes
        if hash_key and not isinstance(hash_key, str):
            raise TypeError("Expected argument 'hash_key' to be a str")
        __self__.hash_key = hash_key
        if local_secondary_indexes and not isinstance(local_secondary_indexes, list):
            raise TypeError("Expected argument 'local_secondary_indexes' to be a list")
        __self__.local_secondary_indexes = local_secondary_indexes
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if point_in_time_recovery and not isinstance(point_in_time_recovery, dict):
            raise TypeError("Expected argument 'point_in_time_recovery' to be a dict")
        __self__.point_in_time_recovery = point_in_time_recovery
        if range_key and not isinstance(range_key, str):
            raise TypeError("Expected argument 'range_key' to be a str")
        __self__.range_key = range_key
        if read_capacity and not isinstance(read_capacity, float):
            raise TypeError("Expected argument 'read_capacity' to be a float")
        __self__.read_capacity = read_capacity
        if server_side_encryption and not isinstance(server_side_encryption, dict):
            raise TypeError("Expected argument 'server_side_encryption' to be a dict")
        __self__.server_side_encryption = server_side_encryption
        if stream_arn and not isinstance(stream_arn, str):
            raise TypeError("Expected argument 'stream_arn' to be a str")
        __self__.stream_arn = stream_arn
        if stream_enabled and not isinstance(stream_enabled, bool):
            raise TypeError("Expected argument 'stream_enabled' to be a bool")
        __self__.stream_enabled = stream_enabled
        if stream_label and not isinstance(stream_label, str):
            raise TypeError("Expected argument 'stream_label' to be a str")
        __self__.stream_label = stream_label
        if stream_view_type and not isinstance(stream_view_type, str):
            raise TypeError("Expected argument 'stream_view_type' to be a str")
        __self__.stream_view_type = stream_view_type
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        if ttl and not isinstance(ttl, dict):
            raise TypeError("Expected argument 'ttl' to be a dict")
        __self__.ttl = ttl
        if write_capacity and not isinstance(write_capacity, float):
            raise TypeError("Expected argument 'write_capacity' to be a float")
        __self__.write_capacity = write_capacity
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetTableResult(GetTableResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTableResult(
            arn=self.arn,
            attributes=self.attributes,
            billing_mode=self.billing_mode,
            global_secondary_indexes=self.global_secondary_indexes,
            hash_key=self.hash_key,
            local_secondary_indexes=self.local_secondary_indexes,
            name=self.name,
            point_in_time_recovery=self.point_in_time_recovery,
            range_key=self.range_key,
            read_capacity=self.read_capacity,
            server_side_encryption=self.server_side_encryption,
            stream_arn=self.stream_arn,
            stream_enabled=self.stream_enabled,
            stream_label=self.stream_label,
            stream_view_type=self.stream_view_type,
            tags=self.tags,
            ttl=self.ttl,
            write_capacity=self.write_capacity,
            id=self.id)

def get_table(name=None,server_side_encryption=None,tags=None,opts=None):
    """
    Provides information about a DynamoDB table.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/d/dynamodb_table.html.markdown.
    """
    __args__ = dict()

    __args__['name'] = name
    __args__['serverSideEncryption'] = server_side_encryption
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.ResourceOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:dynamodb/getTable:getTable', __args__, opts=opts).value

    return AwaitableGetTableResult(
        arn=__ret__.get('arn'),
        attributes=__ret__.get('attributes'),
        billing_mode=__ret__.get('billingMode'),
        global_secondary_indexes=__ret__.get('globalSecondaryIndexes'),
        hash_key=__ret__.get('hashKey'),
        local_secondary_indexes=__ret__.get('localSecondaryIndexes'),
        name=__ret__.get('name'),
        point_in_time_recovery=__ret__.get('pointInTimeRecovery'),
        range_key=__ret__.get('rangeKey'),
        read_capacity=__ret__.get('readCapacity'),
        server_side_encryption=__ret__.get('serverSideEncryption'),
        stream_arn=__ret__.get('streamArn'),
        stream_enabled=__ret__.get('streamEnabled'),
        stream_label=__ret__.get('streamLabel'),
        stream_view_type=__ret__.get('streamViewType'),
        tags=__ret__.get('tags'),
        ttl=__ret__.get('ttl'),
        write_capacity=__ret__.get('writeCapacity'),
        id=__ret__.get('id'))
