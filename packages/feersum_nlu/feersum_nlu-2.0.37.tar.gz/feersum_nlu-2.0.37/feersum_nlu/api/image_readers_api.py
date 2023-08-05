# coding: utf-8

"""
    FeersumNLU API

    This is the HTTP API for Feersum NLU. See https://github.com/praekelt/feersum-nlu-api-wrappers for examples of how to use the API.  # noqa: E501

    OpenAPI spec version: 2.0.37
    Contact: nlu@feersum.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from feersum_nlu.api_client import ApiClient


class ImageReadersApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def image_reader_retrieve(self, instance_name, image_input, **kwargs):  # noqa: E501
        """Read text from the image.  # noqa: E501

        Read text from the image. Returns list of strings found.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.image_reader_retrieve(instance_name, image_input, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instance_name: The name of the model instance. (required)
        :param ImageInput image_input: The input image. (required)
        :param str x_caller:
        :param str origin:
        :return: list[Text]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.image_reader_retrieve_with_http_info(instance_name, image_input, **kwargs)  # noqa: E501
        else:
            (data) = self.image_reader_retrieve_with_http_info(instance_name, image_input, **kwargs)  # noqa: E501
            return data

    def image_reader_retrieve_with_http_info(self, instance_name, image_input, **kwargs):  # noqa: E501
        """Read text from the image.  # noqa: E501

        Read text from the image. Returns list of strings found.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.image_reader_retrieve_with_http_info(instance_name, image_input, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str instance_name: The name of the model instance. (required)
        :param ImageInput image_input: The input image. (required)
        :param str x_caller:
        :param str origin:
        :return: list[Text]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['instance_name', 'image_input', 'x_caller', 'origin']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method image_reader_retrieve" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `image_reader_retrieve`")  # noqa: E501
        # verify the required parameter 'image_input' is set
        if ('image_input' not in params or
                params['image_input'] is None):
            raise ValueError("Missing the required parameter `image_input` when calling `image_reader_retrieve`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'instance_name' in params:
            path_params['instance_name'] = params['instance_name']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_caller' in params:
            header_params['X-CALLER'] = params['x_caller']  # noqa: E501
        if 'origin' in params:
            header_params['Origin'] = params['origin']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'image_input' in params:
            body_params = params['image_input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['APIKeyHeader', 'APIKeyHeader_old']  # noqa: E501

        return self.api_client.call_api(
            '/image_readers/{instance_name}/retrieve', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[Text]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
