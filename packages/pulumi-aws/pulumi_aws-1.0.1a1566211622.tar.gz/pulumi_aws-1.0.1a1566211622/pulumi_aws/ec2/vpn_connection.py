# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class VpnConnection(pulumi.CustomResource):
    customer_gateway_configuration: pulumi.Output[str]
    """
    The configuration information for the VPN connection's customer gateway (in the native XML format).
    """
    customer_gateway_id: pulumi.Output[str]
    """
    The ID of the customer gateway.
    """
    routes: pulumi.Output[list]
    static_routes_only: pulumi.Output[bool]
    """
    Whether the VPN connection uses static routes exclusively. Static routes must be used for devices that don't support BGP.
    """
    tags: pulumi.Output[dict]
    """
    Tags to apply to the connection.
    """
    transit_gateway_attachment_id: pulumi.Output[str]
    """
    When associated with an EC2 Transit Gateway (`transit_gateway_id` argument), the attachment ID.
    """
    transit_gateway_id: pulumi.Output[str]
    """
    The ID of the EC2 Transit Gateway.
    """
    tunnel1_address: pulumi.Output[str]
    """
    The public IP address of the first VPN tunnel.
    """
    tunnel1_bgp_asn: pulumi.Output[str]
    """
    The bgp asn number of the first VPN tunnel.
    """
    tunnel1_bgp_holdtime: pulumi.Output[float]
    """
    The bgp holdtime of the first VPN tunnel.
    """
    tunnel1_cgw_inside_address: pulumi.Output[str]
    """
    The RFC 6890 link-local address of the first VPN tunnel (Customer Gateway Side).
    """
    tunnel1_inside_cidr: pulumi.Output[str]
    """
    The CIDR block of the inside IP addresses for the first VPN tunnel.
    """
    tunnel1_preshared_key: pulumi.Output[str]
    """
    The preshared key of the first VPN tunnel.
    """
    tunnel1_vgw_inside_address: pulumi.Output[str]
    """
    The RFC 6890 link-local address of the first VPN tunnel (VPN Gateway Side).
    """
    tunnel2_address: pulumi.Output[str]
    """
    The public IP address of the second VPN tunnel.
    """
    tunnel2_bgp_asn: pulumi.Output[str]
    """
    The bgp asn number of the second VPN tunnel.
    """
    tunnel2_bgp_holdtime: pulumi.Output[float]
    """
    The bgp holdtime of the second VPN tunnel.
    """
    tunnel2_cgw_inside_address: pulumi.Output[str]
    """
    The RFC 6890 link-local address of the second VPN tunnel (Customer Gateway Side).
    """
    tunnel2_inside_cidr: pulumi.Output[str]
    """
    The CIDR block of the inside IP addresses for the second VPN tunnel.
    """
    tunnel2_preshared_key: pulumi.Output[str]
    """
    The preshared key of the second VPN tunnel.
    """
    tunnel2_vgw_inside_address: pulumi.Output[str]
    """
    The RFC 6890 link-local address of the second VPN tunnel (VPN Gateway Side).
    """
    type: pulumi.Output[str]
    """
    The type of VPN connection. The only type AWS supports at this time is "ipsec.1".
    """
    vgw_telemetries: pulumi.Output[list]
    vpn_gateway_id: pulumi.Output[str]
    """
    The ID of the Virtual Private Gateway.
    """
    def __init__(__self__, resource_name, opts=None, customer_gateway_id=None, static_routes_only=None, tags=None, transit_gateway_id=None, tunnel1_inside_cidr=None, tunnel1_preshared_key=None, tunnel2_inside_cidr=None, tunnel2_preshared_key=None, type=None, vpn_gateway_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an EC2 VPN connection. These objects can be connected to customer gateways, and allow you to establish tunnels between your network and Amazon.
        
        > **Note:** All arguments including `tunnel1_preshared_key` and `tunnel2_preshared_key` will be stored in the raw state as plain-text.
        [Read more about sensitive data in state](https://www.terraform.io/docs/state/sensitive-data.html).
        
        > **Note:** The CIDR blocks in the arguments `tunnel1_inside_cidr` and `tunnel2_inside_cidr` must have a prefix of /30 and be a part of a specific range.
        [Read more about this in the AWS documentation](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_VpnTunnelOptionsSpecification.html).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] customer_gateway_id: The ID of the customer gateway.
        :param pulumi.Input[bool] static_routes_only: Whether the VPN connection uses static routes exclusively. Static routes must be used for devices that don't support BGP.
        :param pulumi.Input[dict] tags: Tags to apply to the connection.
        :param pulumi.Input[str] transit_gateway_id: The ID of the EC2 Transit Gateway.
        :param pulumi.Input[str] tunnel1_inside_cidr: The CIDR block of the inside IP addresses for the first VPN tunnel.
        :param pulumi.Input[str] tunnel1_preshared_key: The preshared key of the first VPN tunnel.
        :param pulumi.Input[str] tunnel2_inside_cidr: The CIDR block of the inside IP addresses for the second VPN tunnel.
        :param pulumi.Input[str] tunnel2_preshared_key: The preshared key of the second VPN tunnel.
        :param pulumi.Input[str] type: The type of VPN connection. The only type AWS supports at this time is "ipsec.1".
        :param pulumi.Input[str] vpn_gateway_id: The ID of the Virtual Private Gateway.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/vpn_connection.html.markdown.
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

            if customer_gateway_id is None:
                raise TypeError("Missing required property 'customer_gateway_id'")
            __props__['customer_gateway_id'] = customer_gateway_id
            __props__['static_routes_only'] = static_routes_only
            __props__['tags'] = tags
            __props__['transit_gateway_id'] = transit_gateway_id
            __props__['tunnel1_inside_cidr'] = tunnel1_inside_cidr
            __props__['tunnel1_preshared_key'] = tunnel1_preshared_key
            __props__['tunnel2_inside_cidr'] = tunnel2_inside_cidr
            __props__['tunnel2_preshared_key'] = tunnel2_preshared_key
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
            __props__['vpn_gateway_id'] = vpn_gateway_id
            __props__['customer_gateway_configuration'] = None
            __props__['routes'] = None
            __props__['transit_gateway_attachment_id'] = None
            __props__['tunnel1_address'] = None
            __props__['tunnel1_bgp_asn'] = None
            __props__['tunnel1_bgp_holdtime'] = None
            __props__['tunnel1_cgw_inside_address'] = None
            __props__['tunnel1_vgw_inside_address'] = None
            __props__['tunnel2_address'] = None
            __props__['tunnel2_bgp_asn'] = None
            __props__['tunnel2_bgp_holdtime'] = None
            __props__['tunnel2_cgw_inside_address'] = None
            __props__['tunnel2_vgw_inside_address'] = None
            __props__['vgw_telemetries'] = None
        super(VpnConnection, __self__).__init__(
            'aws:ec2/vpnConnection:VpnConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, customer_gateway_configuration=None, customer_gateway_id=None, routes=None, static_routes_only=None, tags=None, transit_gateway_attachment_id=None, transit_gateway_id=None, tunnel1_address=None, tunnel1_bgp_asn=None, tunnel1_bgp_holdtime=None, tunnel1_cgw_inside_address=None, tunnel1_inside_cidr=None, tunnel1_preshared_key=None, tunnel1_vgw_inside_address=None, tunnel2_address=None, tunnel2_bgp_asn=None, tunnel2_bgp_holdtime=None, tunnel2_cgw_inside_address=None, tunnel2_inside_cidr=None, tunnel2_preshared_key=None, tunnel2_vgw_inside_address=None, type=None, vgw_telemetries=None, vpn_gateway_id=None):
        """
        Get an existing VpnConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] customer_gateway_configuration: The configuration information for the VPN connection's customer gateway (in the native XML format).
        :param pulumi.Input[str] customer_gateway_id: The ID of the customer gateway.
        :param pulumi.Input[bool] static_routes_only: Whether the VPN connection uses static routes exclusively. Static routes must be used for devices that don't support BGP.
        :param pulumi.Input[dict] tags: Tags to apply to the connection.
        :param pulumi.Input[str] transit_gateway_attachment_id: When associated with an EC2 Transit Gateway (`transit_gateway_id` argument), the attachment ID.
        :param pulumi.Input[str] transit_gateway_id: The ID of the EC2 Transit Gateway.
        :param pulumi.Input[str] tunnel1_address: The public IP address of the first VPN tunnel.
        :param pulumi.Input[str] tunnel1_bgp_asn: The bgp asn number of the first VPN tunnel.
        :param pulumi.Input[float] tunnel1_bgp_holdtime: The bgp holdtime of the first VPN tunnel.
        :param pulumi.Input[str] tunnel1_cgw_inside_address: The RFC 6890 link-local address of the first VPN tunnel (Customer Gateway Side).
        :param pulumi.Input[str] tunnel1_inside_cidr: The CIDR block of the inside IP addresses for the first VPN tunnel.
        :param pulumi.Input[str] tunnel1_preshared_key: The preshared key of the first VPN tunnel.
        :param pulumi.Input[str] tunnel1_vgw_inside_address: The RFC 6890 link-local address of the first VPN tunnel (VPN Gateway Side).
        :param pulumi.Input[str] tunnel2_address: The public IP address of the second VPN tunnel.
        :param pulumi.Input[str] tunnel2_bgp_asn: The bgp asn number of the second VPN tunnel.
        :param pulumi.Input[float] tunnel2_bgp_holdtime: The bgp holdtime of the second VPN tunnel.
        :param pulumi.Input[str] tunnel2_cgw_inside_address: The RFC 6890 link-local address of the second VPN tunnel (Customer Gateway Side).
        :param pulumi.Input[str] tunnel2_inside_cidr: The CIDR block of the inside IP addresses for the second VPN tunnel.
        :param pulumi.Input[str] tunnel2_preshared_key: The preshared key of the second VPN tunnel.
        :param pulumi.Input[str] tunnel2_vgw_inside_address: The RFC 6890 link-local address of the second VPN tunnel (VPN Gateway Side).
        :param pulumi.Input[str] type: The type of VPN connection. The only type AWS supports at this time is "ipsec.1".
        :param pulumi.Input[str] vpn_gateway_id: The ID of the Virtual Private Gateway.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/vpn_connection.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["customer_gateway_configuration"] = customer_gateway_configuration
        __props__["customer_gateway_id"] = customer_gateway_id
        __props__["routes"] = routes
        __props__["static_routes_only"] = static_routes_only
        __props__["tags"] = tags
        __props__["transit_gateway_attachment_id"] = transit_gateway_attachment_id
        __props__["transit_gateway_id"] = transit_gateway_id
        __props__["tunnel1_address"] = tunnel1_address
        __props__["tunnel1_bgp_asn"] = tunnel1_bgp_asn
        __props__["tunnel1_bgp_holdtime"] = tunnel1_bgp_holdtime
        __props__["tunnel1_cgw_inside_address"] = tunnel1_cgw_inside_address
        __props__["tunnel1_inside_cidr"] = tunnel1_inside_cidr
        __props__["tunnel1_preshared_key"] = tunnel1_preshared_key
        __props__["tunnel1_vgw_inside_address"] = tunnel1_vgw_inside_address
        __props__["tunnel2_address"] = tunnel2_address
        __props__["tunnel2_bgp_asn"] = tunnel2_bgp_asn
        __props__["tunnel2_bgp_holdtime"] = tunnel2_bgp_holdtime
        __props__["tunnel2_cgw_inside_address"] = tunnel2_cgw_inside_address
        __props__["tunnel2_inside_cidr"] = tunnel2_inside_cidr
        __props__["tunnel2_preshared_key"] = tunnel2_preshared_key
        __props__["tunnel2_vgw_inside_address"] = tunnel2_vgw_inside_address
        __props__["type"] = type
        __props__["vgw_telemetries"] = vgw_telemetries
        __props__["vpn_gateway_id"] = vpn_gateway_id
        return VpnConnection(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

