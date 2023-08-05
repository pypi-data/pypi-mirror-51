from openhltspirent.base import Base
class IcmpEchoRequest(Base):
	"""TBD
	"""
	YANG_NAME = 'icmp-echo-request'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(IcmpEchoRequest, self).__init__(parent)

	@property
	def Code(self):
		"""ICMP Echo request code.

		Get an instance of the Code class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.code.code.Code)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.code.code import Code
		return Code(self)._read()

	@property
	def Identifier(self):
		"""Identifier value.

		Get an instance of the Identifier class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.identifier.identifier.Identifier)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.identifier.identifier import Identifier
		return Identifier(self)._read()

	@property
	def EchoData(self):
		"""Data value.

		Get an instance of the EchoData class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.echodata.echodata.EchoData)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.echodata.echodata import EchoData
		return EchoData(self)._read()

	@property
	def SequenceNumber(self):
		"""Sequence Number.

		Get an instance of the SequenceNumber class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.sequencenumber.sequencenumber.SequenceNumber)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.sequencenumber.sequencenumber import SequenceNumber
		return SequenceNumber(self)._read()

	@property
	def Checksum(self):
		"""Checksum value.

		Get an instance of the Checksum class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.checksum.checksum.Checksum)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.icmpechorequest.checksum.checksum import Checksum
		return Checksum(self)._read()

