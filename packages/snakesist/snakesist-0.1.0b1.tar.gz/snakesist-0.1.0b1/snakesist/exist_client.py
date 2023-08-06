"""
.. module:: exist_client
    :synopsis: A module containing basic tools for connecting to eXist.
"""

from snakesist.errors import ExistAPIError
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from lxml.etree import XMLSyntaxError
from typing import List
from lxml import etree
import requests
import delb


class Resource:
    """
    A representation of an eXist resource (documents, nodes etc.). 
    Each Resource object must be coupled to an :class:`ExistClient`.

    Resources are identified by IDs: Some resources (documents) just have
    an absolute resource ID, while others (nodes) require an additional node ID.
    """

    def __init__(self, exist_client, query_result: tuple = None):
        """
        :param exist_client: The client to which the resource is coupled.
        :query_result: A tuple containing the absolute resource ID, node ID
                       and the node of the resource.
        """
        if query_result:
            self._abs_resource_id = query_result[0]
            self._node_id = query_result[1]
            self._exist_client = exist_client
            if query_result[2]:
                self.node = query_result[2]
            else:
                self.node = None
        else:
            self._abs_resource_id = None
            self._node_id = None
            self.node = delb.TagNode()

    def __str__(self):
        return str(self.node)

    def update_push(self):
        """
        Write the resource object to the database.
        """
        self._exist_client.update_resource(
            updated_node=str(self.node),
            abs_resource_id=self._abs_resource_id,
            node_id=self._node_id,
        )

    def update_pull(self):
        """
        Retrieve the current node state from the database and update the object.
        """
        self.node = self._exist_client.retrieve_resource(
            abs_resource_id=self._abs_resource_id, node_id=self._node_id
        )

    def delete(self):
        """
        Remove the node from the database.
        """
        self._exist_client.delete_resource(
            abs_resource_id=self._abs_resource_id, node_id=self._node_id
        )
        self._node_id = None
        self._abs_resource_id = None

    @property
    def abs_resource_id(self):
        """
        The absolute resource ID pointing to a document in the database.
        """
        return self._abs_resource_id

    @property
    def node_id(self):
        """
        The node ID locating the node relative to the containing document.
        """
        return self._node_id


class ExistClient:
    """
    An eXist-db client object representing a database instance.
    The client can be used for RUD operations (no C at the moment). 
    Resources can be queried using an XPath expression. 
    Queried resources are identified by the absolute resource ID and, 
    if the resource is part of a document, the node ID.
    """

    HOST = "localhost"
    PORT = 8080
    USR = "admin"
    PARSER = etree.XMLParser(recover=True)

    def __init__(self, host=HOST, port: int = PORT, usr=USR, pw="", prefix="exist"):
        """
        Connect to an eXist-db instance.
        
        :param host: hostname
        :param port: port used to connect to the configured eXist instance
        :param usr: username
        :param pw: password
        :param prefix: configured prefix for the eXist instance
        """
        self._root_collection = "/"
        self.host = host
        self.port = port
        self.usr = usr
        self.pw = pw
        self.prefix = prefix

    @staticmethod
    def _join_paths(*args):
        return "/".join(s.strip("/") for s in args)

    def _get_request(self, url, query=None):
        headers = {"Content-Type": "application/xml"}
        if query:
            params = {"_howmany": 0, "_indent": "no", "_query": query}
            req = requests.get(
                url,
                headers=headers,
                auth=HTTPBasicAuth(self.usr, self.pw),
                params=params,
            )
        else:
            req = requests.get(
                url, headers=headers, auth=HTTPBasicAuth(self.usr, self.pw)
            )
        if req.status_code == requests.codes.ok:
            return req.content
        else:
            req.raise_for_status()

    def _put_request(self, url, data):
        headers = {"Content-Type": "application/xml"}
        req = requests.put(
            url, headers=headers, auth=HTTPBasicAuth(self.usr, self.pw), data=data
        )
        if req.status_code == requests.codes.ok:
            return req.content
        else:
            req.raise_for_status()

    def _parse_item(self, node) -> tuple:
        return (node["absid"], node["nodeid"], node[0])

    @property
    def base_url(self):
        """
        The base URL pointing to the eXist instance.
        """
        return f"http://{self.host}:{self.port}/{self.prefix}/"

    @property
    def root_collection(self):
        """
        The configured root collection for database queries.
        """
        return self._root_collection

    @root_collection.setter
    def root_collection(self, collection):
        """
        Set the path to the root collection for database 
        queries (e. g. '/db/foo/bar/').
        """

        self._root_collection = collection

    @property
    def root_collection_url(self):
        """
        The URL pointing to the configured root collection.
        """

        data_path = self._join_paths("/rest/", self.root_collection)
        url = urljoin(self.base_url, data_path)
        return url

    def query(
        self, query_expression: str, parser=PARSER
    ) -> delb.Document:
        """
        Make a database query using XQuery

        :param query_expression: XQuery expression
        :param parser: Parser used for processing XML
        :return: The query result as a ``delb.Document`` object.
        """
        response_string = self._get_request(
            self.root_collection_url, query=query_expression
        )
        response_node = delb.Document(response_string, parser)
        return response_node

    def retrieve_resources(self, xpath) -> List["Resource"]:
        """
        Retrieve a set of resources from the database using
        an XPath expression.

        :param xpath: XPath expression (whatever version your eXist 
                      instance supports via its RESTful API)
        :return: The query results as a list of :class:`Resource` objects.
        """
        try:
            results_node = self.query(
                query_expression=f"""for $node in {xpath} return 
                    <pyexist-result nodeid="{{util:node-id($node)}}" 
                    absid="{{util:absolute-resource-id($node)}}">
                    {{$node}}</pyexist-result>"""
            )
        except HTTPError:
            raise ExistAPIError(
                f"""The attempt to retrieve resources with the expression {xpath}
                failed. The XPath expression might not be valid."""
            )

        results = results_node.css_select("pyexist-result")

        return [
            Resource(exist_client=self, query_result=self._parse_item(item))
            for item in results
        ]

    def retrieve_resource(
        self, abs_resource_id: str, node_id=None
    ) -> delb.Document:
        """
        Retrieve a single resource by its internal database IDs.

        :param abs_resource_id: The absolute resource ID pointing to the document.
        :param node_id: The node ID locating a node inside a document (optional).
        :return: The queried node as a ``delb.TagNode`` object.
        """
        if node_id:
            result_node = self.query(
                query_expression=f"""util:node-by-id(
                    util:get-resource-by-absolute-id({abs_resource_id}), '{node_id}')"""
            )
        else:
            result_node = self.query(
                query_expression=f"util:get-resource-by-absolute-id({abs_resource_id})"
            )
        return result_node.xpath("./*")[0]

    def update_resource(
        self, updated_node: str, abs_resource_id: str, node_id=None
    ) -> None:
        """
        Replace a database resource with an updated one.

        :param abs_resource_id: The absolute resource ID pointing to the document.
        :param node_id: The node ID locating a node inside a document (optional).
        """
        if node_id:
            response = self.query(
                query_expression=f"""
                let $node := util:node-by-id(
                util:get-resource-by-absolute-id({abs_resource_id}), '{node_id}')
                return update replace $node with {updated_node}"""
            )
        else:
            response = self.query(
                query_expression=f"""
                let $node := util:get-resource-by-absolute-id({abs_resource_id})
                return update replace $node with {updated_node}"""
            )

    def delete_resource(
        self, abs_resource_id: str, node_id=None
    ) -> None:
        """
        Remove a database resource.

        :param abs_resource_id: The absolute resource ID pointing to the document.
        :param node_id: The node ID locating a node inside a document (optional).
        """
        if node_id:
            response = self.query(
                query_expression=f"""
                let $node := util:node-by-id(
                    util:get-resource-by-absolute-id({abs_resource_id}), '{node_id}')
                return update delete $node"""
            )
        else:
            response = self.query(
                query_expression=f"""
                let $node := util:get-resource-by-absolute-id({abs_resource_id})
                return update delete $node"""
            )
