from openhltspirent.base import Base
class SourceAddressList(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/config/port-traffic/frames/igmpv3-query/source-address-list resource.
	"""
	YANG_NAME = 'source-address-list'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'name'
	YANG_PROPERTY_MAP = {"Name": "name"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(SourceAddressList, self).__init__(parent)

	@property
	def Address(self):
		"""Source IPv4 Address

		Get an instance of the Address class.

		Returns:
			obj(openhltspirent.sessions.config.porttraffic.frames.igmpv3query.sourceaddresslist.address.address.Address)
		"""
		from openhltspirent.sessions.config.porttraffic.frames.igmpv3query.sourceaddresslist.address.address import Address
		return Address(self)._read()

	@property
	def Name(self):
		"""TBD

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('name')

	def read(self, Name=None):
		"""Get `source-address-list` resource(s). Returns all `source-address-list` resources from the server if no input parameters are specified.

		"""
		return self._read(Name)

	def create(self, Name):
		"""Create an instance of the `source-address-list` resource

		Args:
			Name (string): TBD
		"""
		return self._create(locals())

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `source-address-list` resource

		"""
		return self._delete()

