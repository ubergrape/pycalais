# coding: utf-8
"""
RDF Extension for pycalais.

The original RDF extension was written by Mark Soper for Jordan Dimov's
original Python interface to the OpenCalais API.
"""
from calais.base.client import Calais
from calais.rdf.response import RDFCalaisResponse


class RDFCalais(Calais):
    processing_directives = {'contentType': 'TEXT/RAW',
                             'outputFormat': 'xml/rdf',
                             'reltagBaseURL': None,
                             'calculateRelevanceScore': 'true',
                             'enableMetadataType': None,
                             'discardMetadata': None,
                             'omitOutputtingOriginalText': 'true'}

    def analyze(self, content, content_type='TEXT/RAW', external_id=None):
        return super(RDFCalais, self).analyze(content, content_type,
                                              external_id,
                                              response_cls=RDFCalaisResponse)
