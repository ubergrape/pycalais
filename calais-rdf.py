
"""
calais-rdf -- RDF extension for Jordan Dimov's Python interface to the OpenCalais API
Author: Mark Soper (mark@likematter.com)
Last-Update: 04/15/2009
"""

from StringIO import StringIO
from rdflib import ConjunctiveGraph as Graph
from rdflib import Namespace
from calais import Calais, CalaisResponse


CATEGORY_QUERY = { 'fields' : ['docId', 'category', 'categoryName', 'score'],
                   'SPARQL' : """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX cp: <http://s.opencalais.com/1/pred/>
    SELECT ?docId ?category ?categoryName ?score
    WHERE { ?doc cp:docId ?docId .
            ?doc cp:category ?category .
            ?doc cp:categoryName ?categoryName .
            ?doc cp:score ?score . }
    """  }


ENTITY_QUERY = { 'fields' : ['entityId', 'name', 'type', 'relevance', 'resolves_to_uri', 'resolves_to_type', 'resolves_to_name', 'resolves_to_score'],
                 'SPARQL' : """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX cp: <http://s.opencalais.com/1/pred/>
    SELECT ?entity ?name ?type ?relevance ?res_uri ?res_type ?res_name ?res_score
    WHERE {?entity cp:name ?name .
           ?entity rdf:type ?type .
           ?rel_uri cp:subject ?entity .
           ?rel_uri cp:relevance ?relevance .
           OPTIONAL { ?res_uri cp:subject ?entity .
                      ?res_uri rdf:type ?res_type .
                      ?res_uri cp:name ?res_name . }
                  }
      """  }

class RDFCalais(Calais):

    processing_directives = {"contentType":"TEXT/RAW",
                             "outputFormat":"xml/rdf",
                             "reltagBaseURL":None,
                             "calculateRelevanceScore":"true",
                             "enableMetadataType":None,
                             "discardMetadata":None,
                             "omitOutputtingOriginalText":"true"}

    def analyze(self, content, content_type="TEXT/RAW", external_id=None):
        if not (content and  len(content.strip())):
            return None
        self.processing_directives["contentType"]=content_type
        if external_id:
            self.user_directives["externalID"] = external_id
        return RDFCalaisResponse(self.rest_POST(content))


class RDFCalaisResponse(CalaisResponse):

    def __init__(self, raw_result):

        rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        c = Namespace("http://s.opencalais.com/1/pred/")
        g = Graph()
        self.graph = g

        g.parse(StringIO(raw_result.decode('utf-8').encode('utf-8')))

        self.categories = [row for row in g.query(CATEGORY_QUERY["SPARQL"])]
        self.entities = [row for row in g.query(ENTITY_QUERY["SPARQL"])]


    def _simplify_json(self, json):
        raise NotImplementedError, "Not available in RDF implementation"

    def print_summary(self):
        raise NotImplementedError, "Not available in RDF implementation"

    def print_entities(self):
        raise NotImplementedError, "Not available in RDF implementation"

    def print_topics(self):
        raise NotImplementedError, "Not available in RDF implementation"

    def print_relations(self):
        raise NotImplementedError, "Not available in RDF implementation"



