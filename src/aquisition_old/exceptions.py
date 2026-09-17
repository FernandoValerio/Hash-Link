class AcquisitionError(Exception): pass
class AuthenticationError(AcquisitionError): pass
class DiscoveryError(AcquisitionError): pass
class DownloadError(AcquisitionError): pass
