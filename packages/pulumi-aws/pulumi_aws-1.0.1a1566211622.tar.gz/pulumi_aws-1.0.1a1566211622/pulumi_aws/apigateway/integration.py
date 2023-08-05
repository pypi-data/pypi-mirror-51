# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Integration(pulumi.CustomResource):
    cache_key_parameters: pulumi.Output[list]
    """
    A list of cache key parameters for the integration.
    """
    cache_namespace: pulumi.Output[str]
    """
    The integration's cache namespace.
    """
    connection_id: pulumi.Output[str]
    """
    The id of the VpcLink used for the integration. **Required** if `connection_type` is `VPC_LINK`
    """
    connection_type: pulumi.Output[str]
    """
    The integration input's [connectionType](https://docs.aws.amazon.com/apigateway/api-reference/resource/integration/#connectionType). Valid values are `INTERNET` (default for connections through the public routable internet), and `VPC_LINK` (for private connections between API Gateway and a network load balancer in a VPC).
    """
    content_handling: pulumi.Output[str]
    """
    Specifies how to handle request payload content type conversions. Supported values are `CONVERT_TO_BINARY` and `CONVERT_TO_TEXT`. If this property is not defined, the request payload will be passed through from the method request to integration request without modification, provided that the passthroughBehaviors is configured to support payload pass-through.
    """
    credentials: pulumi.Output[str]
    """
    The credentials required for the integration. For `AWS` integrations, 2 options are available. To specify an IAM Role for Amazon API Gateway to assume, use the role's ARN. To require that the caller's identity be passed through from the request, specify the string `arn:aws:iam::\*:user/\*`.
    """
    http_method: pulumi.Output[str]
    """
    The HTTP method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTION`, `ANY`)
    when calling the associated resource.
    """
    integration_http_method: pulumi.Output[str]
    """
    The integration HTTP method
    (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONs`, `ANY`, `PATCH`) specifying how API Gateway will interact with the back end.
    **Required** if `type` is `AWS`, `AWS_PROXY`, `HTTP` or `HTTP_PROXY`.
    Not all methods are compatible with all `AWS` integrations.
    e.g. Lambda function [can only be invoked](https://github.com/awslabs/aws-apigateway-importer/issues/9#issuecomment-129651005) via `POST`.
    """
    passthrough_behavior: pulumi.Output[str]
    """
    The integration passthrough behavior (`WHEN_NO_MATCH`, `WHEN_NO_TEMPLATES`, `NEVER`).  **Required** if `request_templates` is used.
    """
    request_parameters: pulumi.Output[dict]
    """
    A map of request query string parameters and headers that should be passed to the backend responder.
    For example: `request_parameters = { "integration.request.header.X-Some-Other-Header" = "method.request.header.X-Some-Header" }`
    """
    request_templates: pulumi.Output[dict]
    """
    A map of the integration's request templates.
    """
    resource_id: pulumi.Output[str]
    """
    The API resource ID.
    """
    rest_api: pulumi.Output[str]
    """
    The ID of the associated REST API.
    """
    timeout_milliseconds: pulumi.Output[float]
    """
    Custom timeout between 50 and 29,000 milliseconds. The default value is 29,000 milliseconds.
    """
    type: pulumi.Output[str]
    """
    The integration input's [type](https://docs.aws.amazon.com/apigateway/api-reference/resource/integration/). Valid values are `HTTP` (for HTTP backends), `MOCK` (not calling any real backend), `AWS` (for AWS services), `AWS_PROXY` (for Lambda proxy integration) and `HTTP_PROXY` (for HTTP proxy integration). An `HTTP` or `HTTP_PROXY` integration with a `connection_type` of `VPC_LINK` is referred to as a private integration and uses a VpcLink to connect API Gateway to a network load balancer of a VPC.
    """
    uri: pulumi.Output[str]
    """
    The input's URI. **Required** if `type` is `AWS`, `AWS_PROXY`, `HTTP` or `HTTP_PROXY`.
    For HTTP integrations, the URI must be a fully formed, encoded HTTP(S) URL according to the RFC-3986 specification . For AWS integrations, the URI should be of the form `arn:aws:apigateway:{region}:{subdomain.service|service}:{path|action}/{service_api}`. `region`, `subdomain` and `service` are used to determine the right endpoint.
    e.g. `arn:aws:apigateway:eu-west-1:lambda:path/2015-03-31/functions/arn:aws:lambda:eu-west-1:012345678901:function:my-func/invocations`
    """
    def __init__(__self__, resource_name, opts=None, cache_key_parameters=None, cache_namespace=None, connection_id=None, connection_type=None, content_handling=None, credentials=None, http_method=None, integration_http_method=None, passthrough_behavior=None, request_parameters=None, request_templates=None, resource_id=None, rest_api=None, timeout_milliseconds=None, type=None, uri=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an HTTP Method Integration for an API Gateway Integration.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] cache_key_parameters: A list of cache key parameters for the integration.
        :param pulumi.Input[str] cache_namespace: The integration's cache namespace.
        :param pulumi.Input[str] connection_id: The id of the VpcLink used for the integration. **Required** if `connection_type` is `VPC_LINK`
        :param pulumi.Input[str] connection_type: The integration input's [connectionType](https://docs.aws.amazon.com/apigateway/api-reference/resource/integration/#connectionType). Valid values are `INTERNET` (default for connections through the public routable internet), and `VPC_LINK` (for private connections between API Gateway and a network load balancer in a VPC).
        :param pulumi.Input[str] content_handling: Specifies how to handle request payload content type conversions. Supported values are `CONVERT_TO_BINARY` and `CONVERT_TO_TEXT`. If this property is not defined, the request payload will be passed through from the method request to integration request without modification, provided that the passthroughBehaviors is configured to support payload pass-through.
        :param pulumi.Input[str] credentials: The credentials required for the integration. For `AWS` integrations, 2 options are available. To specify an IAM Role for Amazon API Gateway to assume, use the role's ARN. To require that the caller's identity be passed through from the request, specify the string `arn:aws:iam::\*:user/\*`.
        :param pulumi.Input[str] http_method: The HTTP method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTION`, `ANY`)
               when calling the associated resource.
        :param pulumi.Input[str] integration_http_method: The integration HTTP method
               (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONs`, `ANY`, `PATCH`) specifying how API Gateway will interact with the back end.
               **Required** if `type` is `AWS`, `AWS_PROXY`, `HTTP` or `HTTP_PROXY`.
               Not all methods are compatible with all `AWS` integrations.
               e.g. Lambda function [can only be invoked](https://github.com/awslabs/aws-apigateway-importer/issues/9#issuecomment-129651005) via `POST`.
        :param pulumi.Input[str] passthrough_behavior: The integration passthrough behavior (`WHEN_NO_MATCH`, `WHEN_NO_TEMPLATES`, `NEVER`).  **Required** if `request_templates` is used.
        :param pulumi.Input[dict] request_parameters: A map of request query string parameters and headers that should be passed to the backend responder.
               For example: `request_parameters = { "integration.request.header.X-Some-Other-Header" = "method.request.header.X-Some-Header" }`
        :param pulumi.Input[dict] request_templates: A map of the integration's request templates.
        :param pulumi.Input[str] resource_id: The API resource ID.
        :param pulumi.Input[str] rest_api: The ID of the associated REST API.
        :param pulumi.Input[float] timeout_milliseconds: Custom timeout between 50 and 29,000 milliseconds. The default value is 29,000 milliseconds.
        :param pulumi.Input[str] type: The integration input's [type](https://docs.aws.amazon.com/apigateway/api-reference/resource/integration/). Valid values are `HTTP` (for HTTP backends), `MOCK` (not calling any real backend), `AWS` (for AWS services), `AWS_PROXY` (for Lambda proxy integration) and `HTTP_PROXY` (for HTTP proxy integration). An `HTTP` or `HTTP_PROXY` integration with a `connection_type` of `VPC_LINK` is referred to as a private integration and uses a VpcLink to connect API Gateway to a network load balancer of a VPC.
        :param pulumi.Input[str] uri: The input's URI. **Required** if `type` is `AWS`, `AWS_PROXY`, `HTTP` or `HTTP_PROXY`.
               For HTTP integrations, the URI must be a fully formed, encoded HTTP(S) URL according to the RFC-3986 specification . For AWS integrations, the URI should be of the form `arn:aws:apigateway:{region}:{subdomain.service|service}:{path|action}/{service_api}`. `region`, `subdomain` and `service` are used to determine the right endpoint.
               e.g. `arn:aws:apigateway:eu-west-1:lambda:path/2015-03-31/functions/arn:aws:lambda:eu-west-1:012345678901:function:my-func/invocations`

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/api_gateway_integration.html.markdown.
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

            __props__['cache_key_parameters'] = cache_key_parameters
            __props__['cache_namespace'] = cache_namespace
            __props__['connection_id'] = connection_id
            __props__['connection_type'] = connection_type
            __props__['content_handling'] = content_handling
            __props__['credentials'] = credentials
            if http_method is None:
                raise TypeError("Missing required property 'http_method'")
            __props__['http_method'] = http_method
            __props__['integration_http_method'] = integration_http_method
            __props__['passthrough_behavior'] = passthrough_behavior
            __props__['request_parameters'] = request_parameters
            __props__['request_templates'] = request_templates
            if resource_id is None:
                raise TypeError("Missing required property 'resource_id'")
            __props__['resource_id'] = resource_id
            if rest_api is None:
                raise TypeError("Missing required property 'rest_api'")
            __props__['rest_api'] = rest_api
            __props__['timeout_milliseconds'] = timeout_milliseconds
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
            __props__['uri'] = uri
        super(Integration, __self__).__init__(
            'aws:apigateway/integration:Integration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, cache_key_parameters=None, cache_namespace=None, connection_id=None, connection_type=None, content_handling=None, credentials=None, http_method=None, integration_http_method=None, passthrough_behavior=None, request_parameters=None, request_templates=None, resource_id=None, rest_api=None, timeout_milliseconds=None, type=None, uri=None):
        """
        Get an existing Integration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] cache_key_parameters: A list of cache key parameters for the integration.
        :param pulumi.Input[str] cache_namespace: The integration's cache namespace.
        :param pulumi.Input[str] connection_id: The id of the VpcLink used for the integration. **Required** if `connection_type` is `VPC_LINK`
        :param pulumi.Input[str] connection_type: The integration input's [connectionType](https://docs.aws.amazon.com/apigateway/api-reference/resource/integration/#connectionType). Valid values are `INTERNET` (default for connections through the public routable internet), and `VPC_LINK` (for private connections between API Gateway and a network load balancer in a VPC).
        :param pulumi.Input[str] content_handling: Specifies how to handle request payload content type conversions. Supported values are `CONVERT_TO_BINARY` and `CONVERT_TO_TEXT`. If this property is not defined, the request payload will be passed through from the method request to integration request without modification, provided that the passthroughBehaviors is configured to support payload pass-through.
        :param pulumi.Input[str] credentials: The credentials required for the integration. For `AWS` integrations, 2 options are available. To specify an IAM Role for Amazon API Gateway to assume, use the role's ARN. To require that the caller's identity be passed through from the request, specify the string `arn:aws:iam::\*:user/\*`.
        :param pulumi.Input[str] http_method: The HTTP method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTION`, `ANY`)
               when calling the associated resource.
        :param pulumi.Input[str] integration_http_method: The integration HTTP method
               (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONs`, `ANY`, `PATCH`) specifying how API Gateway will interact with the back end.
               **Required** if `type` is `AWS`, `AWS_PROXY`, `HTTP` or `HTTP_PROXY`.
               Not all methods are compatible with all `AWS` integrations.
               e.g. Lambda function [can only be invoked](https://github.com/awslabs/aws-apigateway-importer/issues/9#issuecomment-129651005) via `POST`.
        :param pulumi.Input[str] passthrough_behavior: The integration passthrough behavior (`WHEN_NO_MATCH`, `WHEN_NO_TEMPLATES`, `NEVER`).  **Required** if `request_templates` is used.
        :param pulumi.Input[dict] request_parameters: A map of request query string parameters and headers that should be passed to the backend responder.
               For example: `request_parameters = { "integration.request.header.X-Some-Other-Header" = "method.request.header.X-Some-Header" }`
        :param pulumi.Input[dict] request_templates: A map of the integration's request templates.
        :param pulumi.Input[str] resource_id: The API resource ID.
        :param pulumi.Input[str] rest_api: The ID of the associated REST API.
        :param pulumi.Input[float] timeout_milliseconds: Custom timeout between 50 and 29,000 milliseconds. The default value is 29,000 milliseconds.
        :param pulumi.Input[str] type: The integration input's [type](https://docs.aws.amazon.com/apigateway/api-reference/resource/integration/). Valid values are `HTTP` (for HTTP backends), `MOCK` (not calling any real backend), `AWS` (for AWS services), `AWS_PROXY` (for Lambda proxy integration) and `HTTP_PROXY` (for HTTP proxy integration). An `HTTP` or `HTTP_PROXY` integration with a `connection_type` of `VPC_LINK` is referred to as a private integration and uses a VpcLink to connect API Gateway to a network load balancer of a VPC.
        :param pulumi.Input[str] uri: The input's URI. **Required** if `type` is `AWS`, `AWS_PROXY`, `HTTP` or `HTTP_PROXY`.
               For HTTP integrations, the URI must be a fully formed, encoded HTTP(S) URL according to the RFC-3986 specification . For AWS integrations, the URI should be of the form `arn:aws:apigateway:{region}:{subdomain.service|service}:{path|action}/{service_api}`. `region`, `subdomain` and `service` are used to determine the right endpoint.
               e.g. `arn:aws:apigateway:eu-west-1:lambda:path/2015-03-31/functions/arn:aws:lambda:eu-west-1:012345678901:function:my-func/invocations`

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/api_gateway_integration.html.markdown.
        """
        opts = pulumi.ResourceOptions(id=id) if opts is None else opts.merge(pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["cache_key_parameters"] = cache_key_parameters
        __props__["cache_namespace"] = cache_namespace
        __props__["connection_id"] = connection_id
        __props__["connection_type"] = connection_type
        __props__["content_handling"] = content_handling
        __props__["credentials"] = credentials
        __props__["http_method"] = http_method
        __props__["integration_http_method"] = integration_http_method
        __props__["passthrough_behavior"] = passthrough_behavior
        __props__["request_parameters"] = request_parameters
        __props__["request_templates"] = request_templates
        __props__["resource_id"] = resource_id
        __props__["rest_api"] = rest_api
        __props__["timeout_milliseconds"] = timeout_milliseconds
        __props__["type"] = type
        __props__["uri"] = uri
        return Integration(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

