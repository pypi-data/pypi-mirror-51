from openhltspirent.base import Base
class IcmpInformationRequest(Base):
	"""TBD
	"""
	YANG_NAME = 'icmp-information-request'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(IcmpInformationRequest, self).__init__(parent)

	@property
	def Code(self):
		"""ICMP information request code.

		Get an instance of the Code class.

		Returns:
			obj(openhltspirent.sessions.config.devicetraffic.frames.icmpinformationrequest.code.code.Code)
		"""
		from openhltspirent.sessions.config.devicetraffic.frames.icmpinformationrequest.code.code import Code
		return Code(self)._read()

	@property
	def Identifier(self):
		"""Identifier value.

		Get an instance of the Identifier class.

		Returns:
			obj(openhltspirent.sessions.config.devicetraffic.frames.icmpinformationrequest.identifier.identifier.Identifier)
		"""
		from openhltspirent.sessions.config.devicetraffic.frames.icmpinformationrequest.identifier.identifier import Identifier
		return Identifier(self)._read()

	@property
	def SequenceNumber(self):
		"""Sequence Number.

		Get an instance of the SequenceNumber class.

		Returns:
			obj(openhltspirent.sessions.config.devicetraffic.frames.icmpinformationrequest.sequencenumber.sequencenumber.SequenceNumber)
		"""
		from openhltspirent.sessions.config.devicetraffic.frames.icmpinformationrequest.sequencenumber.sequencenumber import SequenceNumber
		return SequenceNumber(self)._read()

	@property
	def Checksum(self):
		"""Checksum value.

		Get an instance of the Checksum class.

		Returns:
			obj(openhltspirent.sessions.config.devicetraffic.frames.icmpinformationrequest.checksum.checksum.Checksum)
		"""
		from openhltspirent.sessions.config.devicetraffic.frames.icmpinformationrequest.checksum.checksum import Checksum
		return Checksum(self)._read()

