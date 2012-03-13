from nose.tools import eq_, ok_, raises

from calais.base.response import CalaisResponse
from calais import exceptions


RAW_RESPONSE = '{"http://d.opencalais.com/pershash-1/6192d572-838c-3be4-8724-93fb0fca25d7": {"_typeReference": "http://s.opencalais.com/1/type/em/e/Person", "_type": "Person", "name": "Winston Churchill", "commonname": "Winston Churchill", "_typeGroup": "entities", "instances": [{"detection": "[]Winston Churchill[ was an optimist, by all]", "length": 17, "exact": "Winston Churchill", "suffix": " was an optimist, by all", "offset": 0}], "relevance": 0.857, "nationality": "N/A", "persontype": "N/A"}, "doc": {"info": {"docId": "http://d.opencalais.com/dochash-1/bf01a89a-8854-3db0-a9e0-17ce98a28016", "docDate": "2011-11-25 06:43:05.146", "allowSearch": "false", "docTitle": "", "submitter": "1.0", "allowDistribution": "false", "document": "", "calaisRequestID": "5b42083c-818b-04f4-133d-ac023fc298cf", "id": "http://id.opencalais.com/UfegThDnEiLVEjxPuKA4WQ", "externalMetadata": " "}, "meta": {"submitterCode": "73a204cb-98e2-2823-14ea-0197eba97bb8", "contentType": "TEXT/RAW", "language": "InputTextTooShort", "emVer": "7.1.1103.5", "messages": [], "processingVer": "CalaisJob01", "submitionDate": "2011-11-25 06:43:05.084", "signature": "digestalg-1|S7tippuJEhLeLFJ2IAm/ah368FA=|RMXX7xaA53pBD/LXRtCS5Rt8fmhn5NwdfJ9Ql8lO0iyvc6MU9YDeaA==", "langIdVer": "DefaultLangId"}}}'
BUSY_RESPONSE = '<Error Method="ProcessText" calaisRequestID="ed010f41-4ffb-c6fd-1355-de894f86ba51" CreationDate="2012-02-08 11:00:18" CalaisVersion="R4.3_7.1.1103.5"><Exception>Calais Backend-Server is Busy. Please try again later.</Exception></Error>"'
QPS_RESPONSE = '<h1>403 Developer Over Qps</h1>'
LANGUAGE_FAIL_RESPONSE = '<Error Method="ProcessText" calaisRequestID="347c8ee9-689f-f3a8-1356-3f995ceb5bb5" CreationDate="2012-02-09 15:16:35" CalaisVersion="R4.3_7.1.1103.5"><Exception>Calais continues to expand its list of supported languages, but does not yet support your submitted content.</Exception></Error>'
MAX_LENGTH_RESPONSE = '<Error Method="ProcessText" calaisRequestID="9a8e48e6-bfa2-e92b-1356-3efbda98fc2f" CreationDate="2012-02-09 15:05:50" CalaisVersion="R4.3_7.1.1103.5"><Exception>Text length has exceeded the allowed size .</Exception></Error>'
GATEWAY_TIMEOUT_RESPONSE = '<h1>504 Gateway Timeout</h1>'


def test_info():
    r = CalaisResponse(RAW_RESPONSE)
    eq_(r.info['id'], 'http://id.opencalais.com/UfegThDnEiLVEjxPuKA4WQ')


def test_meta():
    r = CalaisResponse(RAW_RESPONSE)
    eq_(r.meta['submitionDate'], '2011-11-25 06:43:05.084')


def test_attrs():
    r = CalaisResponse(RAW_RESPONSE)
    ok_('entities' in r)
    ok_('socialTags' not in r)


@raises(exceptions.MaxQpsExceeded)
def test_maxqps():
    return CalaisResponse(QPS_RESPONSE)


@raises(exceptions.BusyCalais)
def test_busy():
    return CalaisResponse(BUSY_RESPONSE)


@raises(exceptions.LanguageUnsupported)
def test_lang():
    return CalaisResponse(LANGUAGE_FAIL_RESPONSE)


@raises(exceptions.MaxLenExceeded)
def test_len():
    return CalaisResponse(MAX_LENGTH_RESPONSE)


@raises(exceptions.GatewayTimeout)
def test_gateway():
    return CalaisResponse(GATEWAY_TIMEOUT_RESPONSE)


@raises(exceptions.CalaisError)
def test_general_fail():
    return CalaisResponse('oh noe this is missing curly braces!')
