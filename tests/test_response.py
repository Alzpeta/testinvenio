from invenio_oaiserver.models import OAISet


def test_response(db, schema, client):
   oaiset = OAISet(spec='higgs', name='Higgs', description='...')
   oaiset.search_pattern = 'title:higgs'
   db.session.add(oaiset)
   db.session.add(oaiset)
   res = client.get('/oai2d?verb=ListSets')
   print(res.data)
