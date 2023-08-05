from openhltspirent.base import Base
class Gre(Base):
	"""TBD
	"""
	YANG_NAME = 'gre'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Gre, self).__init__(parent)

	@property
	def ChecksumBit(self):
		"""Checksum bit.

		Get an instance of the ChecksumBit class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.checksumbit.checksumbit.ChecksumBit)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.checksumbit.checksumbit import ChecksumBit
		return ChecksumBit(self)._read()

	@property
	def RoutingBit(self):
		"""Routing bit.

		Get an instance of the RoutingBit class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.routingbit.routingbit.RoutingBit)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.routingbit.routingbit import RoutingBit
		return RoutingBit(self)._read()

	@property
	def KeyBit(self):
		"""Key bit.

		Get an instance of the KeyBit class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.keybit.keybit.KeyBit)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.keybit.keybit import KeyBit
		return KeyBit(self)._read()

	@property
	def SequenceNumberBit(self):
		"""Sequence Number bit.

		Get an instance of the SequenceNumberBit class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.sequencenumberbit.sequencenumberbit.SequenceNumberBit)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.sequencenumberbit.sequencenumberbit import SequenceNumberBit
		return SequenceNumberBit(self)._read()

	@property
	def Reserved0(self):
		"""Reserved-0 bits.

		Get an instance of the Reserved0 class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.reserved0.reserved0.Reserved0)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.reserved0.reserved0 import Reserved0
		return Reserved0(self)._read()

	@property
	def Version(self):
		"""GRE Version.

		Get an instance of the Version class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.version.version.Version)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.version.version import Version
		return Version(self)._read()

	@property
	def ProtocolType(self):
		"""Indicates the ether protocol type of the encapsulated payload.

		Get an instance of the ProtocolType class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.protocoltype.protocoltype.ProtocolType)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.protocoltype.protocoltype import ProtocolType
		return ProtocolType(self)._read()

	@property
	def GreChecksum(self):
		"""GRE Version.

		Get an instance of the GreChecksum class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.grechecksum.grechecksum.GreChecksum)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.grechecksum.grechecksum import GreChecksum
		return GreChecksum(self)._read()

	@property
	def Reserved1(self):
		"""Reserved-1 bits.

		Get an instance of the Reserved1 class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.reserved1.reserved1.Reserved1)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.reserved1.reserved1 import Reserved1
		return Reserved1(self)._read()

	@property
	def Key(self):
		"""Key Value.

		Get an instance of the Key class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.key.key.Key)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.key.key import Key
		return Key(self)._read()

	@property
	def SequenceNumber(self):
		"""Sequence Number.

		Get an instance of the SequenceNumber class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.sequencenumber.sequencenumber.SequenceNumber)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.sequencenumber.sequencenumber import SequenceNumber
		return SequenceNumber(self)._read()

	@property
	def KeepAliveBit(self):
		"""Keep Alive bit.

		Get an instance of the KeepAliveBit class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.keepalivebit.keepalivebit.KeepAliveBit)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.keepalivebit.keepalivebit import KeepAliveBit
		return KeepAliveBit(self)._read()

	@property
	def KeepAlivePeriod(self):
		"""Keep alive period.

		Get an instance of the KeepAlivePeriod class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.keepaliveperiod.keepaliveperiod.KeepAlivePeriod)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.keepaliveperiod.keepaliveperiod import KeepAlivePeriod
		return KeepAlivePeriod(self)._read()

	@property
	def KeepAliveRetries(self):
		"""Keep alive retries.

		Get an instance of the KeepAliveRetries class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.gre.keepaliveretries.keepaliveretries.KeepAliveRetries)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.gre.keepaliveretries.keepaliveretries import KeepAliveRetries
		return KeepAliveRetries(self)._read()

