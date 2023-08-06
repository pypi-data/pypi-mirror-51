Overview
========

Provides functions to store tuple data as JSON documents in Elasticsearch indices.

This package exposes the `com.ibm.streamsx.elasticsearch <https://ibmstreams.github.io/streamsx.elasticsearch/>`_ toolkit as Python methods for use with Streaming Analytics service on
IBM Cloud and IBM Streams including IBM Cloud Pak for Data.

* `Streaming Analytics service <https://console.ng.bluemix.net/catalog/services/streaming-analytics>`_
* `IBM Streams developer community <https://developer.ibm.com/streamsdev/>`_
* `Compose for Elasticsearch <https://www.ibm.com/cloud/compose/elasticsearch>`_


Sample
======

A simple hello world example of a Streams application writing string messages to
an index::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema
    from streamsx.topology.context import submit
    import streamsx.elasticsearch as es

    topo = Topology('ElasticsearchHelloWorld')

    s = topo.source(['Hello', 'World!']).as_string()
    es.bulk_insert(s, 'test-index-cloud')

    submit('STREAMING_ANALYTICS_SERVICE', topo)


A simple example of a Streams application writing JSON messages to an index, with dynamic index name (part of the stream)::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema, StreamSchema
    from streamsx.topology.context import submit
    import streamsx.elasticsearch as es

    schema = StreamSchema('tuple<rstring indexName, rstring document>')
    topo = Topology()
    s = topo.source([('idx1','{"msg":"This is message number 1"}'), ('idx2','{"msg":"This is message number 2"}')])
    s = s.map(lambda x : x, schema=schema)
    es.bulk_insert_dynamic(s, index_name_attribute='indexName', message_attribute='document')

    submit('STREAMING_ANALYTICS_SERVICE', topo)


Documentation
=============

* `streamsx.elasticsearch package documentation <http://streamsxelasticsearch.readthedocs.io/>`_


