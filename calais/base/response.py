# coding: utf-8
"""
The CalaisResponse object as should be returned by a default
``Calais.analyze(...)`` call.
"""
try:  # Python <2.6 needs the simplejson module.
    import simplejson as json
except ImportError:
    import json

from calais import exceptions


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
        self._detect_fails(raw_result)

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

    def _detect_fails(self, resp):
        """
        Detect any failures in the given raw response.
        """
        if '{' in resp:
            return

        lowercase = resp.lower()
        if 'qps' in lowercase:
            raise exceptions.MaxQpsExceeded('You reached your queries per '
                                            'second limit.')
        elif 'busy' in lowercase:
            raise exceptions.BusyCalais('OpenCalais is too busy.')
        elif 'supported languages' in lowercase:
            raise exceptions.LanguageUnsupported("The content's language is"
                                                 'not supported by OpenCalais'
                                                 'yet.')
        elif 'text length' in lowercase:
            raise exceptions.MaxLenExceeded('Content too long for OpenCalais.')
        elif 'gateway timeout' in lowercase:
            raise exceptions.GatewayTimeout('Gateway timed out.')
        else:
            raise exceptions.CalaisError('OpenCalais returned the following '
                                         'error: "%s"' % resp)

    def __contains__(self, item):
        if hasattr(self, item):
            return True
        return False
