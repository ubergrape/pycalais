========
pycalais
========

is a nearly identical clone of python-calais_ and therefore an interface to
the `OpenCalais REST API`_.

To be more specific, we are using the `paramsXML Method`_.

Changes from the original include:

- Most issues reported on google code are fixed.
- README converted into reST format.
- PEP8 compliance & code cleanup
- Test Coverage
- Changes Response objects

.. _`OpenCalais REST API`: http://www.opencalais.com/documentation/calais-web-service-api
.. _`paramsXML Method`: http://www.opencalais.com/documentation/calais-web-service-api/api-invocation/rest-using-paramsxml

Requirements
============

This module has been tested with Python 2.5 and Python 2.7.

Python <2.6 need the ``simplejson`` module to be installed.

In case you want to use the ``RDFCalais`` module, you need to
install ``rdflib >= 3`` and ``rdfextras >= 0.1``.
The latter one is needed for SPARQL query support, just so you know.

Usage
=====

To use the OpenCalais API, first create a ``Calais()`` object, passing it your
OpenCalais API key and a string identifier of your application::

    >>> from calais import Calais
    >>> calais = Calais("your-opencalais-api-key",
    ...                 submitter="pycalais demo")

You can then use the ``analyze()`` method.  It takes a string, containing the
text to be analyzed by Calais and returns a ``CalaisResponse()`` object::

    >>> result = calais.analyze("""
    ...     George Bush was the President of the United States of America
    ...     until 2009.  Barack Obama is the new President of
    ...     the United States now.""")

Or you can use the ``analyze_url()`` method, which downloads the specified HTML
page and passes it on to OpenCalais::

    >>> result2 = calais.analyze_url("http://www.example.com/")

The response object automagically scans through OpenCalais' output and sets
it's attributes depending on this output. Let's say we've analyzed the previous
string about the two US Presidents. The following two attributes should always
be available to you::

    >>> result.info
    {u'allowDistribution': u'false',
     u'allowSearch': u'false',
     u'calaisRequestID': u'XXX',
     u'docDate': u'2011-11-25 06:08:58.282',
     u'docId': u'XXX',
     u'docTitle': '',
     u'document': '',
     u'externalMetadata': u' ',
     u'id': u'XXX',
     u'submitter': u'1.0'}
    >>> result.meta
    {u'contentType': u'TEXT/RAW',
     u'emVer': u'7.1.1103.5',
     u'langIdVer': u'DefaultLangId',
     u'language': u'English',
     u'messages': [],
     u'processingVer': u'CalaisJob01',
     u'signature': u'XXX',
     u'submitionDate': u'2011-11-25 06:08:51.898',
     u'submitterCode': u'XXX'}

There is more. Depending on the output you will also gain access to
for example::

    >>> result.topics
    {u'http://d.opencalais.com/dochash-1/a5b24be1-5d5c-34c6-a6d4-92b4072d2973/cat/1':
     {u'_typeGroup': u'topics',
      u'category': u'http://d.opencalais.com/cat/Calais/Politics',
      u'categoryName': u'Politics',
      u'classifierName': u'Calais',
      u'score': 1}}

Note that all attributes besides *info* and *meta* will be pluralised.

To check if a response has a specific attribute, for example *socialTags*,
you do not have to use ``hasattr()``. Instead you may use python's magic
``in`` keyword::

    >>> 'entities' in result
    True
    >>> 'events' in result
    False

This should get you up and running. For further information, you should
check out the code (it's pretty :-)) or play around in the interpreter (we
highly recommend iPython because of the nice autocompletion).

RDFCalais
=========

For all you *SPARQL* enthusiasts, there is also a way to use *SPARQL* on the
OpenCalais Response, thanks to the work of Mark Soper.

Just use the ``RDFCalais()`` class instead of the regular one::

    >>> from calais import RDFCalais
    >>> calais = RDFCalais("your-opencalais-api-key",
    ...                    submitter="pycalais rdf/sparql demo")
    >>> result = calais.analyze("""
    ...     George Bush was the President of the United States of America
    ...     until 2009.  Barack Obama is the new President of
    ...     the United States now.""")

Note that the ``result`` is a ``RDFCalaisResponse`` now.
There are new properties available for you. The following two are already
generated through a *SPARQL* query::

    >>> result.categories
    [[rdflib.term.URIRef('http://d.opencalais.com/dochash-1/a6437d7b-9b69-3750-bf43-400bc134df07'),
    rdflib.term.URIRef('http://d.opencalais.com/cat/Calais/Politics'),
    rdflib.term.Literal(u'Politics'),
    rdflib.term.Literal(u'1.000')]]
    >>> result.entities
    [[rdflib.term.URIRef('http://d.opencalais.com/genericHasher-1/e69aa6d0-1c03-34b6-88ed-9af4acb3440e'),
      rdflib.term.Literal(u'United States of America'),
      rdflib.term.URIRef('http://s.opencalais.com/1/type/em/e/Country'),
      rdflib.term.Literal(u'0.464'),
      rdflib.term.URIRef('http://d.opencalais.com/er/geo/country/ralg-geo1/152649df-347e-e289-1a9e-acc883e07d17'),
      rdflib.term.URIRef('http://s.opencalais.com/1/type/er/Geo/Country'),
      rdflib.term.Literal(u'United States'),
      None], ... a lot more objects ... ]

The third property is the ``graph`` object, as generated by the underlying
``rdflib``. This is where you can do your own SPARQL queries::

    >>> result.graph
    <Graph identifier=SOMEID (<class 'rdflib.graph.ConjunctiveGraph'>)>
    >>> qrs = result.graph.query("""
    ... PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    ... PREFIX cp: <http://s.opencalais.com/1/pred/>
    ...
    ... SELECT DISTINCT ?name WHERE {
    ...     ?subject cp:name ?name
    ... }""")
    >>> qrs.result
    [rdflib.term.Literal(u'George Bush'),
     rdflib.term.Literal(u'President of\n        the United States'),
     rdflib.term.Literal(u'United States of America'),
     rdflib.term.Literal(u'President of the United States of America'),
     rdflib.term.Literal(u'United States'),
     rdflib.term.Literal(u'Barack Obama'),
     rdflib.term.Literal(u'President')]

Notes
=====

Thanks to the original python-calais_ project, as sponsored by `A115 Ltd`_.

.. _`A115 LTD`: http://www.a115.bg/en/
.. _python-calais: http://code.google.com/p/python-calais/
