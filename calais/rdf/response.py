# coding: utf-8
"""
CalaisResponse queryable through SPARQL.

The original RDF extension was written by Mark Soper for Jordan Dimov's
original Python interface to the OpenCalais API.
"""
from StringIO import StringIO

from rdflib import ConjunctiveGraph as Graph
from rdflib import Namespace
from rdflib import plugin
from rdflib import query

from calais.base.response import CalaisResponse


# Register RDFLib SPARQL support.
plugin.register('sparql', query.Processor,
                'rdfextras.sparql.processor', 'Processor')
plugin.register('sparql', query.Result,
                'rdfextras.sparql.query', 'SPARQLQueryResult')

# SPARQL Queries
CATEGORY_QUERY = {'fields': ['docId', 'category', 'categoryName', 'score'],
                   'SPARQL': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX cp: <http://s.opencalais.com/1/pred/>

    SELECT ?docId ?category ?categoryName ?score
    WHERE { ?doc cp:docId ?docId .
            ?doc cp:category ?category .
            ?doc cp:categoryName ?categoryName .
            ?doc cp:score ?score . }
    """, }

ENTITY_QUERY = {'fields': ['entityId', 'name', 'type', 'relevance',
                            'resolves_to_uri', 'resolves_to_type',
                            'resolves_to_name', 'resolves_to_score'],
                 'SPARQL': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX cp: <http://s.opencalais.com/1/pred/>

    SELECT ?entity ?name ?type ?relevance
           ?res_uri ?res_type ?res_name ?res_score
    WHERE {
           ?entity cp:name ?name .
           ?entity rdf:type ?type .
           ?rel_uri cp:subject ?entity .
           ?rel_uri cp:relevance ?relevance .
           OPTIONAL { ?res_uri cp:subject ?entity .
                      ?res_uri rdf:type ?res_type .
                      ?res_uri cp:name ?res_name . }
          }
      """, }



class RDFCalaisResponse(CalaisResponse):
    """
    RDFCalaisResponse creates a graph from the received output from OpenCalais
    and makes it queryable through SPARQL.
    """
    def __init__(self, raw_result):
        self._detect_fails(raw_result)
        rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        c = Namespace('http://s.opencalais.com/1/pred/')
        g = Graph()
        self.graph = g

        g.parse(StringIO(raw_result.decode('utf-8').encode('utf-8')))

        self.categories = [row for row in g.query(CATEGORY_QUERY['SPARQL'])]
        self.entities = [row for row in g.query(ENTITY_QUERY['SPARQL'])]
