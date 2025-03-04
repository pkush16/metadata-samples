# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Configuration, Serializer, Deserializer
from .version import VERSION
from msrest.pipeline import ClientRawResponse
from msrest.exceptions import HttpOperationError
from . import models


class JsonGeneratorClientConfiguration(Configuration):
    """Configuration for JsonGeneratorClient
    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param str base_url: Service URL
    """

    def __init__(
            self, base_url=None):

        if not base_url:
            base_url = 'http://localhost'

        super(JsonGeneratorClientConfiguration, self).__init__(base_url)

        self.add_user_agent('jsongeneratorclient/{}'.format(VERSION))


class JsonGeneratorClient(SDKClient):
    """defaultDescription

    :ivar config: Configuration for client.
    :vartype config: JsonGeneratorClientConfiguration

    :param str base_url: Service URL
    """

    def __init__(
            self, base_url=None):

        self.config = JsonGeneratorClientConfiguration(base_url)
        super(JsonGeneratorClient, self).__init__(None, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = '0.1'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)


    def create_lineage(
            self, body=None, custom_headers=None, raw=False, **operation_config):
        """

        :param body:
        :type body: list[~swagger.models.Array]
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: list or ClientRawResponse if raw=true
        :rtype: list[~swagger.models.Model1Array] or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.create_lineage.metadata['url']

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if body is not None:
            body_content = self._serialize.body(body, '[Array]')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters, header_parameters, body_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('[Model1Array]', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    create_lineage.metadata = {'url': '/api/atlas_relationships_create'}
