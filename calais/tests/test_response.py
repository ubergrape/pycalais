from nose.tools import eq_, ok_

from calais import CalaisResponse


RAW_RESPONSE = '{"http://d.opencalais.com/pershash-1/6192d572-838c-3be4-8724-93fb0fca25d7": {"_typeReference": "http://s.opencalais.com/1/type/em/e/Person", "_type": "Person", "name": "Winston Churchill", "commonname": "Winston Churchill", "_typeGroup": "entities", "instances": [{"detection": "[]Winston Churchill[ was an optimist, by all]", "length": 17, "exact": "Winston Churchill", "suffix": " was an optimist, by all", "offset": 0}], "relevance": 0.857, "nationality": "N/A", "persontype": "N/A"}, "doc": {"info": {"docId": "http://d.opencalais.com/dochash-1/bf01a89a-8854-3db0-a9e0-17ce98a28016", "docDate": "2011-11-25 06:43:05.146", "allowSearch": "false", "docTitle": "", "submitter": "1.0", "allowDistribution": "false", "document": "", "calaisRequestID": "5b42083c-818b-04f4-133d-ac023fc298cf", "id": "http://id.opencalais.com/UfegThDnEiLVEjxPuKA4WQ", "externalMetadata": " "}, "meta": {"submitterCode": "73a204cb-98e2-2823-14ea-0197eba97bb8", "contentType": "TEXT/RAW", "language": "InputTextTooShort", "emVer": "7.1.1103.5", "messages": [], "processingVer": "CalaisJob01", "submitionDate": "2011-11-25 06:43:05.084", "signature": "digestalg-1|S7tippuJEhLeLFJ2IAm/ah368FA=|RMXX7xaA53pBD/LXRtCS5Rt8fmhn5NwdfJ9Ql8lO0iyvc6MU9YDeaA==", "langIdVer": "DefaultLangId"}}}'

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
