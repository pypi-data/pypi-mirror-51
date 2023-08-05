from openhltspirent.base import Base
class DeviceTraffic(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/statistics/device-traffic resource.
	"""
	YANG_NAME = 'device-traffic'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'name'
	YANG_PROPERTY_MAP = {"RxFrames": "rx-frames", "RxFrameRate": "rx-frame-rate", "TxFrameRate": "tx-frame-rate", "Name": "name", "TxByteRate": "tx-byte-rate", "TxBitRate": "tx-bit-rate", "TxByteCount": "tx-byte-count", "RxByteCount": "rx-byte-count", "TxFrames": "tx-frames", "RxBitRate": "rx-bit-rate", "RxBitCount": "rx-bit-count", "DroppedFrames": "dropped-frames", "TxBitCount": "tx-bit-count", "RxByteRate": "rx-byte-rate"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(DeviceTraffic, self).__init__(parent)

	@property
	def Ports(self):
		"""TBD

		Get an instance of the Ports class.

		Returns:
			obj(openhltspirent.sessions.statistics.devicetraffic.ports.ports.Ports)
		"""
		from openhltspirent.sessions.statistics.devicetraffic.ports.ports import Ports
		return Ports(self)

	@property
	def Name(self):
		"""Device Traffic name

		Getter Returns:
			string
		"""
		return self._get_value('name')

	@property
	def TxFrames(self):
		"""The total number of frames transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-frames')

	@property
	def RxFrames(self):
		"""The total number of frames received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-frames')

	@property
	def TxFrameRate(self):
		"""Total number of frames transmitted over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-frame-rate')

	@property
	def RxFrameRate(self):
		"""Total number of frames received over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-frame-rate')

	@property
	def DroppedFrames(self):
		"""Total Number of dropped frames during transit.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('dropped-frames')

	@property
	def TxBitCount(self):
		"""The total number of bits transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-bit-count')

	@property
	def RxBitCount(self):
		"""The total number of bits received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-bit-count')

	@property
	def TxBitRate(self):
		"""Total number of bits transmitted over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-bit-rate')

	@property
	def RxBitRate(self):
		"""Total number of bits received over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-bit-rate')

	@property
	def TxByteCount(self):
		"""The total number of bytes transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-byte-count')

	@property
	def RxByteCount(self):
		"""The total number of bytes received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-byte-count')

	@property
	def TxByteRate(self):
		"""Total number of bytes transmitted over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-byte-rate')

	@property
	def RxByteRate(self):
		"""Total number of bytes received over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-byte-rate')

	def read(self, Name=None):
		"""Get `device-traffic` resource(s). Returns all `device-traffic` resources from the server if no input parameters are specified.

		"""
		return self._read(Name)

