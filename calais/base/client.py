# coding: utf-8
"""
pycalais -- a Python interface to the OpenCalais REST API.

Cloned and modified from Jordan Dimov's python-calais.

This interface uses OpenCalais' "paramsXML" REST API method.
"""
import re
import string
import random
import urllib
import httplib
import hashlib
import mimetypes
from xml.sax.saxutils import escape

from calais.base.response import CalaisResponse


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
    # Lie shamelessly to every website.
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

    def __init__(self, api_key, submitter=False):
        if not submitter:
            # self. does not work in the function header.
            submitter = self._get_version()

        self.api_key = api_key
        self.user_directives["submitter"] = submitter

    def _get_params_XML(self):
        # This could be further simplified through map(),
        # however I think readability is better this way.
        x = lambda y: " ".join('c:%s="%s"' % (key, escape(value))
                                              for (key, value) in y.items()
                                              if value)
        return PARAMS_XML % (x(self.processing_directives),
                             x(self.user_directives),
                             x(self.external_metadata))

    def _get_version(self):
        # HACK: We need to defer the __init__.py import since we are
        #       importing this and other files in __init__ so imports for
        #       other developers are beautiful. <3
        from calais import __version__
        return __version__

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

        Don't get confused, this method is not directly used here,
        however the user may use it as external_id for ``analyze()``.
        """
        chars = string.letters + string.digits
        return ''.join(random.sample(chars, 10))

    def get_content_id(self, text):
        """
        Creates a SHA1 hash of the text of your submission.

        Don't get confused, this method is not directly used here,
        however the user may use it as external_id for ``analyze()``.
        """
        h = hashlib.sha1()
        h.update(text)
        return h.hexdigest()

    def preprocess_html(self, html):
        html = html.replace('\n', '')
        html = SCRIPT_STYLE_RE.sub('', html)
        return html

    def analyze(self, content, content_type='TEXT/RAW', external_id=None,
                response_cls=CalaisResponse):
        if not (content and len(content.strip())):
            return None

        self.processing_directives['contentType'] = content_type

        if not external_id is None:
            self.user_directives['externalID'] = urllib.quote(external_id)

        return response_cls(self.rest_POST(content))

    def analyze_url(self, url):
        request = urllib.urlopen(url)
        html = self.preprocess_html(request.read())
        return self.analyze(html, content_type='TEXT/HTML', external_id=url)

    def analyze_file(self, filename):
        filetype = mimetypes.guess_type(filename)[0]
        if filetype is None:
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

        return self.analyze(content, content_type=content_type,
                            external_id=filename)
