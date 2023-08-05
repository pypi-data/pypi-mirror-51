from openhltspirent.base import Base
class Ospfv3InterAreaPrefixRange(Base):
	"""TBD
	"""
	YANG_NAME = 'ospfv3-inter-area-prefix-range'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Ospfv3InterAreaPrefixRange, self).__init__(parent)

	@property
	def Address(self):
		"""IPv6 address

		Get an instance of the Address class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.address.address.Address)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.address.address import Address
		return Address(self)._read()

	@property
	def PrefixLength(self):
		"""Prefix Length

		Get an instance of the PrefixLength class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.prefixlength.prefixlength.PrefixLength)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.prefixlength.prefixlength import PrefixLength
		return PrefixLength(self)._read()

	@property
	def AdvertiseRouterId(self):
		"""Advertising Router ID.  Specifies the 32-bit router ID of the router that
		advertises a given LSA 

		Get an instance of the AdvertiseRouterId class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.advertiserouterid.advertiserouterid.AdvertiseRouterId)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.advertiserouterid.advertiserouterid import AdvertiseRouterId
		return AdvertiseRouterId(self)._read()

	@property
	def SequenceNumber(self):
		"""Sequence Number. Used to detect old and duplicate LSAs.

		Get an instance of the SequenceNumber class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.sequencenumber.sequencenumber.SequenceNumber)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.sequencenumber.sequencenumber import SequenceNumber
		return SequenceNumber(self)._read()

	@property
	def Age(self):
		"""Age of the LSA, in seconds.

		Get an instance of the Age class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.age.age.Age)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.age.age import Age
		return Age(self)._read()

	@property
	def Checksum(self):
		"""Specifies the LSA will be advertised with a good or a bad checksum.

		Get an instance of the Checksum class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.checksum.checksum.Checksum)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.checksum.checksum import Checksum
		return Checksum(self)._read()

	@property
	def RouteCategory(self):
		"""Route Category can be used to filter routes by type.
		   UNDEFINED The default category assigned to a manually created block.
		   PRIMARY   A preferred route that has duplicates (secondary routes) advertised by other ports.
		   SECONDARY Secondary route.
		   UNIQUE    A less preferred backup route.
		   ANY       Indicates that a single port in the test configuration advertises this route.

		Get an instance of the RouteCategory class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.routecategory.routecategory.RouteCategory)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.routecategory.routecategory import RouteCategory
		return RouteCategory(self)._read()

	@property
	def Metric(self):
		"""Cost of the advertised network prefix.

		Get an instance of the Metric class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.metric.metric.Metric)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.metric.metric import Metric
		return Metric(self)._read()

	@property
	def PrefixOptions(self):
		"""8- bit field of capabilities advertised with each prefix.
		   NUBIT    No Unicast capability bit. If set, the prefix is excluded from IPv6 unicast calculations.
		   LABIT    Local Address capability bit. If set, the prefix becomes an IPv6 interface address of the advertising router.
		   MCBIT    Multicast capability bit. If set, the prefix is included in the IPv6 multicast calculations.
		   PBIT     Propagate bit. Set this on the NSSA area prefixes that should be readvertised at the NSSA border.
		   DNBIT    Downward bit. Controls an inter-area-prefix-LSAs or AS-external-LSAs re-advertisement in a VPN environment
		   NBIT     Set in PrefixOptions for a host address (PrefixLength=128) that identifies the advertising router
		   UNUSED6  Bit not defined.
		   UNUSED7  Bit not defined. 

		Get an instance of the PrefixOptions class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.prefixoptions.prefixoptions.PrefixOptions)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.prefixoptions.prefixoptions import PrefixOptions
		return PrefixOptions(self)._read()

	@property
	def LinkStateId(self):
		"""Link State ID. ID of the interface connected to the transit network

		Get an instance of the LinkStateId class.

		Returns:
			obj(openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.linkstateid.linkstateid.LinkStateId)
		"""
		from openhltspirent.sessions.config.devicegroups.simulatednetworks.networks.ospfv3interareaprefixrange.linkstateid.linkstateid import LinkStateId
		return LinkStateId(self)._read()

