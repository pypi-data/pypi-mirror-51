from openhltspirent.base import Base
class Udp(Base):
	"""TBD
	"""
	YANG_NAME = 'udp'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Udp, self).__init__(parent)

	@property
	def SourcePort(self):
		"""Specifies the port on the sending UDP module.

		Get an instance of the SourcePort class.

		Returns:
			obj(openhltspirent.sessions.config.devicetraffic.frames.udp.sourceport.sourceport.SourcePort)
		"""
		from openhltspirent.sessions.config.devicetraffic.frames.udp.sourceport.sourceport import SourcePort
		return SourcePort(self)._read()

	@property
	def DestinationPort(self):
		"""Specifies the port on the receiving UDP module.

		Get an instance of the DestinationPort class.

		Returns:
			obj(openhltspirent.sessions.config.devicetraffic.frames.udp.destinationport.destinationport.DestinationPort)
		"""
		from openhltspirent.sessions.config.devicetraffic.frames.udp.destinationport.destinationport import DestinationPort
		return DestinationPort(self)._read()

	@property
	def Checksum(self):
		"""Specifies the UDP checksum value.

		Get an instance of the Checksum class.

		Returns:
			obj(openhltspirent.sessions.config.devicetraffic.frames.udp.checksum.checksum.Checksum)
		"""
		from openhltspirent.sessions.config.devicetraffic.frames.udp.checksum.checksum import Checksum
		return Checksum(self)._read()

