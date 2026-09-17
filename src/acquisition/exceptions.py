class AcquisitionError(Exception): pass
class ValidationError(AcquisitionError): pass
class AuthenticationError(AcquisitionError): pass
class DiscoveryError(AcquisitionError): pass
class DownloadError(AcquisitionError): pass
