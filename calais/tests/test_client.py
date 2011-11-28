# coding: utf-8
import os
import unittest

from nose.tools import eq_, ok_, raises

from calais.base import client


# The good monkeypatching
class DummyRequest(object):
    def read(self):
        return 'foobar'

def dummy_urlopen(*args, **kwargs):
    return DummyRequest()
client.urllib.urlopen = dummy_urlopen


class DummyCalaisResponse(object):
    def __init__(self, *args, **kwargs):
        pass

    # I feel dirty when using isinstance()
    def is_dummy(self):
        return True


class BaseCalaisTest(unittest.TestCase):
    def setUp(self):
        self.c = client.Calais('asdf')


class CalaisTest(BaseCalaisTest):
    def testStripper(self):
        stripped = self.c.preprocess_html("""<body><p>TestWinFail</p>
            Opium for the people.
            <script>(function noscript() {})()</script>
            <noscript>Why you noscript?</noscript>
        """)
        eq_(stripped, ('<body><p>TestWinFail</p>            Opium for the '
                       'people.                                '))

    def testRandomID(self):
        """
        Test Random ID Generation.

        Note that this class fails if the sample
        (string.latters + string.chars) has less than 10 items.

        Hereby I warn you: do not tinker with your string module or this
        will fail fataly.
        """
        eq_(len(self.c.get_random_id()), 10)

    def testContentHash(self):
        """
        Let's check that the hash of a string stayed the same.
        """
        eq_(self.c.get_content_id('newsgrape'),
           '10e9a5f599b467d22b86d6fb9c762d0d4df37abe')

    def testLazyResponseClass(self):
        self.c.rest_POST = lambda x: True
        ok_(self.c.analyze('asd', response_cls=DummyCalaisResponse).is_dummy())


class MimeTypeTest(BaseCalaisTest):
    """
    Make sure MimeType and therefore ContentType detection works.
    """
    def setUp(self):
        super(MimeTypeTest, self).setUp()
        self.c.analyze = self.analyze_stub

    def analyze_stub(self, *args, **kwargs):
        """
        Mocking of ``analyze()`` function to check if ``analyze_file()``
        worked as expected.
        """
        external_id = kwargs['external_id']
        content_type = kwargs['content_type']

        if external_id.endswith('.xml'):
            eq_(content_type, 'TEXT/XML')
        elif external_id.endswith(('.html', '.htm',)):
            eq_(content_type, 'TEXT/HTML')
            # make sure stripping worked.
            content = args[0]
            ok_('\n' not in content)
            ok_('<script>' not in content)
            ok_('<noscript>' not in content)
            ok_('<style>' not in content)
        else:
            eq_(content_type, 'TEXT/RAW')

    def get_path(self, filename):
        return os.path.join(os.path.dirname(__file__), 'data', filename)

    def testHTML(self):
        self.c.analyze_file(self.get_path('index.html'))

    def testHTM(self):
        self.c.analyze_file(self.get_path('index.htm'))

    def testXML(self):
        self.c.analyze_file(self.get_path('test.xml'))

    @raises(ValueError)
    def testFOO(self):
        self.c.analyze_file(self.get_path('foobar.baz'))


class URLTest(BaseCalaisTest):
    def setUp(self):
        super(URLTest, self).setUp()
        self.c.analyze = self.analyze_stub

    def analyze_stub(self, html, *args, **kwargs):
        eq_(html, 'foobar')

    def testURLs(self):
        self.c.analyze_url('http://example.com/')
