from solarnetwork_python.client import Client

def test_nodes():
    client = Client("token", "secret")
    nodes = client.nodes()
    assert len(nodes) > 1

def test_import():
    client = Client("token", "secret")

    service_properties = {
        "headerRowCount": "1",
        "dateColumnsValue": "3",
        "dateFormat": "MM/dd/yyyy HH:mm:ss",
        "nodeIdColumn": "1",
        "sourceIdColumn": "2"
    }

    inner = {
        "name": "Test Input",
        "timeZoneId": "America/New_York",
        "serviceIdentifier": "net.solarnetwork.central.datum.imp.standard.BasicCsvDatumImportInputFormatService",
        "serviceProperties": service_properties
    }

    outer = {
        "name": "Test Import",
        "stage": True,
        "inputConfiguration": inner
    }

    csv_data = (
        'node,source,date,irradiance,wattHours\r\n'
        '708,/TEST/TEST,2024-01-21 07:25:00,0.000,0.000\r\n'
        '708,/TEST/TEST,2024-01-21 07:30:00,9.000,10.100\r\n'
        '708,/TEST/TEST,2024-01-21 07:35:00,12.336,15.020\r\n'
        '708,/TEST/TEST,2024-01-21 07:40:00,15.660,19.325\r\n'
        '708,/TEST/TEST,2024-01-21 07:45:00,18.996,25.923'
    )

    client.import_data(outer, csv_data)
