from acquisition.services.acquisition_service import AcquisitionService

def test_analyse():
 assert AcquisitionService().analyse("https://example.com")["url"]
