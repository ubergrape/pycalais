# coding: utf-8
"""
pycalais -- a Python interface to the OpenCalais API.

Cloned and modified from Jordan Dimov's python-calais.
"""
__version__ = '1.0'

import re
import string
import random
import urllib
import httplib
import hashlib
import mimetypes
from xml.sax.saxutils import escape
from StringIO import StringIO
try:  # Python <2.6 needs the simplejson module.
    import simplejson as json
except ImportError:
    import json


PARAMS_XML = """
<c:params xmlns:c="http://s.opencalais.com/1/pred/"
          xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <c:processingDirectives %s> </c:processingDirectives>
    <c:userDirectives %s> </c:userDirectives>
    <c:externalMetadata %s> </c:externalMetadata>
</c:params>
"""

SCRIPT_STYLE_RE = re.compile(
            '<script.*?</script>|<noscript.*?</noscript>|<style.*?</style>',
            re.IGNORECASE)


class AppURLopener(urllib.FancyURLopener):
    # Lie shamelessly to every website opened.
    version = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:9.0) '
               'Gecko/20100101 Firefox/9.0')
urllib._urlopener = AppURLopener()


class Calais(object):
    """
    Python class that knows how to talk to the OpenCalais API.

    Use the ``analyze()`` and ``analyze_url()`` methods, which return
    ``CalaisResponse`` objects.
    """
    api_key = None
    processing_directives = {"contentType": "TEXT/RAW",
                             "outputFormat": "application/json",
                             "reltagBaseURL": None,
                             "calculateRelevanceScore": "true",
                             "enableMetadataType": "SocialTags",
                             "discardMetadata": None,
                             "omitOutputtingOriginalText": "true", }
    user_directives = {"allowDistribution": "false",
                       "allowSearch": "false",
                       "externalID": None, }
    external_metadata = {}

    def __init__(self, api_key, submitter="pycalais client %s" % __version__):
        self.api_key = api_key
        self.user_directives["submitter"] = submitter

    def _get_params_XML(self):
        props = lambda x: " ".join('c:%s="%s"' % (key, escape(value))
                                                  for (key, value) in x.items()
                                                  if value)
        return PARAMS_XML % map(props, [self.processing_directives,
                                        self.user_directives,
                                        self.external_metadata])

    def rest_POST(self, content):
        params = urllib.urlencode(
                    {'licenseID': self.api_key,
                     'content': (content.decode('utf8')
                                        .encode('ascii', 'xmlcharrefreplace')),
                     'paramsXML': self._get_params_XML(),
                    })
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn = httplib.HTTPConnection('api.opencalais.com:80')
        conn.request('POST', '/enlighten/rest/', params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data

    def get_random_id(self):
        """
        Creates a random 10-character ID for your submission.
        """
        chars = string.letters + string.digits
        return ''.join(random.sample(chars, 10))

    def get_content_id(self, text):
        """
        Creates a SHA1 hash of the text of your submission.
        """
        checksum = hashlib.sha1(text)
        return checksum.hexdigest()

    def preprocess_html(self, html):
        html = html.replace('\n', '')
        html = SCRIPT_STYLE_RE.sub('', html)
        return html

    def analyze(self, content, content_type='TEXT/RAW', external_id=None):
        if not (content and len(content.strip())):
            return None

        self.processing_directives['contentType'] = content_type

        if external_id:
            self.user_directives['externalID'] = urllib.quote(external_id)

        return CalaisResponse(self.rest_POST(content))

    def analyze_url(self, url):
        request = urllib.urlopen(url)
        html = self.preprocess_html(request.read())
        return self.analyze(html, content_type='TEXT/HTML', external_id=url)

    def analyze_file(self, filename):
        try:
            filetype = mimetypes.guess_type(filename)[0]
        except IndexError:
            raise ValueError('Can not determine file type for "%s"' % filename)

        # Let's hope this does not leave file descriptors open.
        content = open(filename).read()
        content_type = ''
        if filetype == 'text/plain':
            content_type = 'TEXT/RAW'
        elif filetype == 'application/xml':
            content_type = 'TEXT/XML'
        elif filetype == 'text/html':
            content_type = filetype.upper()
            content = self.preprocess_html(content)
        else:
            raise ValueError('Only plaintext, HTML or XML files are '
                             'currently supported.')

        return self.analyze(content, content_type=content_type, external_id=fn)


class CalaisResponse(object):
    """
    Encapsulates a parsed Calais response and provides pythonic access
    to the data.
    """
    raw_response = None
    simplified_response = None

    def __init__(self, raw_result):
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
