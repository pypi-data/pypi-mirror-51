from openhltspirent.base import Base
class Vlan(Base):
	"""TBD
	"""
	YANG_NAME = 'vlan'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Vlan, self).__init__(parent)

	@property
	def Priority(self):
		"""TBD

		Get an instance of the Priority class.

		Returns:
			obj(openhltspirent.sessions.config.devicetraffic.frames.vlan.priority.priority.Priority)
		"""
		from openhltspirent.sessions.config.devicetraffic.frames.vlan.priority.priority import Priority
		return Priority(self)._read()

	@property
	def Id(self):
		"""A single-tagged VLAN id

		Get an instance of the Id class.

		Returns:
			obj(openhltspirent.sessions.config.devicetraffic.frames.vlan.id.id.Id)
		"""
		from openhltspirent.sessions.config.devicetraffic.frames.vlan.id.id import Id
		return Id(self)._read()

