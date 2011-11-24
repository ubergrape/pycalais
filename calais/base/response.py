# coding: utf-8
"""
The CalaisResponse object as should be returned by a default
``Calais.analyze(...)`` call.
"""
from StringIO import StringIO
try:  # Python <2.6 needs the simplejson module.
    import simplejson as json
except ImportError:
    import json


class CalaisResponse(object):
    """
    Encapsulates a parsed Calais response and provides pythonic access
    to the data.
    """
    raw_response = None
    simplified_response = None

    def __init__(self, raw_result):
        if not '{' in raw_result:
            raise ValueError('OpenCalais returned the following error: "%s"'
                                % raw_result)

        self.raw_response = json.load(StringIO(raw_result.decode('utf-8')),
                                      encoding="utf-8")
        self.simplified_response = self._simplify_json(self.raw_response)

        self.__dict__['doc'] = self.raw_response['doc']
        for key, value in self.simplified_response.items():
            self.__dict__[key] = value

    def _simplify_json(self, json):
        result = {}
        # First, resolve references
        for element in json.values():
            for key, value in element.items():
                if (isinstance(value, unicode) and value.startswith('http://')
                        and value in json):
                    element[key] = json[value]

        for key, value in json.items():
            if '_typeGroup' in value:
                group = value['_typeGroup']
                # TODO: use setdefault()
                if not group in result:
                    result[group] = []
                del value['_typeGroup']
                value['__reference'] = key
                result[group].append(value)

        return result

    def print_summary(self):
        if not hasattr(self, 'doc'):
            return None

        info = self.doc['info']
        print 'Calais Request ID: %s' % info['calaisRequestID']

        if 'externalID' in info:
            print 'External ID: %s' % info['externalID']

        if 'docTitle' in info:
            print 'Title: %s ' % info['docTitle']

        print 'Language: %s' % self.doc['meta']['language']
        print 'Extractions: '

        simple_response = self.simplified_response.items()
        for key, value in simple_response:
            print '\t%d %s' % (len(value), key)

    def print_entities(self):
        if not hasattr(self, 'entities'):
            return None

        for item in self.entities:
            print '%s: %s (%.2f)' % (item['_type'], item['name'],
                                     item['relevance'])

    def print_topics(self):
        if not hasattr(self, 'topics'):
            return None

        for topic in self.topics:
            print topic['categoryName']

    def print_relations(self):
        if not hasattr(self, 'relations'):
            return None

        for relation in self.relations:
            print relation['_type']
            for k, v in relation.items():
                if not k.startswith('_'):
                    if isinstance(v, unicode):
                        print '\t%s:%s' % (k, v)
                    elif isinstance(v, dict) and 'name' in v:
                        print '\t%s:%s' % (k, v['name'])

    def print_social_tags(self):
        if not hasattr(self, 'socialTag'):
            return None

        for socialTag in self.socialTag:
            print '%s %s' % (socialTag['name'], socialTag['importance'])
