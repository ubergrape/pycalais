========
pycalais
========

is a nearly identical clone of python-calais_ and therefore an interface to
the `OpenCalais REST API`_.

To be more specific, we are using the `paramsXML Method`_.

Changes from the original include:

- most issues reported on google code are fixed.
- README converted into reST format.
- PEP8 compliance & code cleanup

.. _`OpenCalais REST API`: http://www.opencalais.com/documentation/calais-web-service-api
.. _`paramsXML Method`: http://www.opencalais.com/documentation/calais-web-service-api/api-invocation/rest-using-paramsxml

Requirements
============

This module has been tested with Python 2.5 and Python 2.7.

Python <2.6 need the ``simplejson`` module to be installed.

In case you want to use the ``calais_rdf`` module/extension, you need to
install ``rdflib`` and ``rdfextras``. The latter one is needed for SPARQL query
support, just so you know.

Usage
=====

To use the OpenCalais API, first create a ``Calais()`` object, passing it your
OpenCalais API key and a string identifier of your application::

    >>> from calais import Calais
    >>> calais = Calais("your-opencalais-api-key",
                        submitter="pycalais demo")

You can then use the ``analyze()`` method.  It takes a string, containing the
text to be analyzed by Calais and returns a ``CalaisResponse()`` object::

    >>> result = calais.analyze("""
            George Bush was the President of the United States of America
            until 2009.  Barack Obama is the new President of
            the United States now.""")

Or you can use the ``analyze_url()`` method, which downloads the specified HTML
page and passes it on to OpenCalais::

    >>> result2 = calais.analyze_url("http://www.example.com/")

The ``CalaisResponse`` class provides several helper methods that print
information about the response::

    >>> result.print_summary()
    Calais Request ID: 0bfa1f51-4dec-4a82-aba6-a9f8243a94fd
    Title:
    Language: English
    Extractions:
            4 entities
            1 topics
            2 relations
    >>> result.print_topics()
    Politics
    >>> result.print_entities()
    Person: Barack Obama (0.29)
    Country: United States of America (0.43)
    Person: George Bush (0.43)
    Country: United States (0.29)
    >>> result.print_relations()
    PersonPoliticalPast
            person:George Bush
            position:President
    PersonPolitical
            person:Barack Obama
            position:President of the United States

Or you can access the results directly::

    >>> print result.entities[0]["name"]
    Barack Obama

You can also set processing and user directives before you make an
``analyze()`` call::

    >>> calais.user_directives["allowDistribution"] = "true"
    >>> result3 = calais.analyze("Some non-confidential text",
                                  external_id=calais.get_random_id())

This should get you up and running. For further information, I guess you should
check out the code. It is pretty! :-)

Notes
=====

The original python-calais_ project is sponsored by `A115 Ltd`_.

.. _`A115 LTD`: http://www.a115.bg/en/
.. _python-calais: http://code.google.com/p/python-calais/
