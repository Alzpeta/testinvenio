from invenio_indexer.api import RecordIndexer
from invenio_records import Record
from invenio_pidstore.minters import recid_minter
import uuid
from invenio_oaiserver.minters import oaiid_minter

def create_record(app, item_dict, mint_oaiid=True):
    """Create test record."""
    indexer = RecordIndexer()
    with app.test_request_context():
        record_id = uuid.uuid4()
        recid_minter(record_id, item_dict)
        if mint_oaiid:
            oaiid_minter(record_id, item_dict)
        record = Record.create(item_dict, id_=record_id)
        indexer.index(record)
        return record
