# coding: utf-8
"""
The CalaisResponse object as should be returned by a default
``Calais.analyze(...)`` call.
"""
try:  # Python <2.6 needs the simplejson module.
    import simplejson as json
except ImportError:
    import json


class CalaisResponse(object):
    """
    Encapsulates a parsed Calais response and provides pythonic access
    to the data.
    """
    def __init__(self, raw_result):
        # Usually OpenCalais returns a valid JSON object, therefore
        # it is pretty safe to assume a { should be in the response.
        # I would have put that in a try/except on json.loads, however
        # it is pretty hard to differ between a json exception and an
        # OpenCalais error message?
        if not '{' in raw_result:
            raise ValueError('OpenCalais returned the following error: "%s"'
                                % raw_result)

        self.raw_response = json.loads(raw_result)

        self.info = self.raw_response['doc']['info']
        self.meta = self.raw_response['doc']['meta']

        for key, value in self.raw_response.iteritems():
            try:
                if key.startswith('http://'):
                    attr_name = value['_typeGroup']
                    # pluralise the attribute name
                    if not attr_name.endswith('s'):
                        attr_name += 's'

                    if not hasattr(self, attr_name):
                        setattr(self, attr_name, {})
                    getattr(self, attr_name)[key] = value
            except AttributeError:
                # FIXME: Looks like the key was not an URI, ignore for now.
                continue

    def __contains__(self, item):
        if hasattr(self, item):
            return True
        return False
