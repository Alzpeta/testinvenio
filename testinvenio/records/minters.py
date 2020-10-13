from invenio_pidstore.minters import recid_minter
from invenio_oaiserver.minters import oaiid_minter
def minter(record_uuid, data):
    rminter = recid_minter(record_uuid, data)
    oaiid_minter(record_uuid, data)

    return rminter
