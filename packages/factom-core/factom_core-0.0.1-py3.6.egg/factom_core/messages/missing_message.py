import struct
from factom_core.messages import Message


class MissingMessageRequest(Message):
    """
    A request for a missing message in a node's process list
    """

    TYPE = 16

    def __init__(self, timestamp: bytes, asking: bytes, vm_index: int, height: int, system_height: int,
                 process_list_heights: list):
        # TODO: type/value assertions
        self.timestamp = timestamp
        self.asking = asking
        self.vm_index = vm_index
        self.height = height
        self.system_height = system_height
        self.process_list_heights = process_list_heights
        self.is_p2p = True
        super().__init__()

    def marshal(self) -> bytes:
        """
        Marshal the message into the following representation:
        - first byte is the message type (always 16)
        - next 6 bytes are the timestamp
        - next 32 bytes are the asker hash (?)
        - next byte is the VM index
        - next 4 bytes are the directory block height
        - next 4 bytes are the system height
        - next 4 bytes are the number of missing message process list heights
        - next X bytes are a series of 4 byte process list heights

        :return: byte representation of the message
        """
        buf = bytearray()
        buf.append(self.TYPE)
        buf.extend(self.timestamp)
        buf.extend(self.asking)
        buf.append(self.vm_index)
        buf.extend(struct.pack('>I', self.height))
        buf.extend(struct.pack('>I', self.system_height))
        buf.extend(struct.pack('>I', len(self.process_list_heights)))
        for h in self.process_list_heights:
            buf.extend(struct.pack('>I', h))
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw:  bytes):
        msg_type, data = raw[0], raw[1:]
        if msg_type != cls.TYPE:
            raise ValueError("Invalid message type ({})".format(msg_type))

        timestamp, data = data[:6], data[6:]
        asking, data = data[:32], data[32:]
        vm_index, data = data[0], data[1:]
        height, data = struct.unpack('>I', data[:4])[0], data[4:]
        system_height, data = struct.unpack('>I', data[:4])[0], data[4:]
        process_list_heights_count, data = struct.unpack('>I', data[:4])[0], data[4:]
        process_list_heights = []
        for _ in range(process_list_heights_count):
            h, data = struct.unpack('>I', data[:4])[0], data[4:]
            process_list_heights.append(h)

        return MissingMessageRequest(
            timestamp=timestamp,
            asking=asking,
            vm_index=vm_index,
            height=height,
            system_height=system_height,
            process_list_heights=process_list_heights,
        )

    def __str__(self):
        return '{}(hash={})'.format(self.__class__.__name__, self.asking)


class MissingMessageResponse(Message):
    """
    A response to a MissingMessageRequest, containing the requested message
    """

    TYPE = 19

    def __init__(self, timestamp: bytes):
        # TODO: type/value assertions
        self.timestamp = timestamp

        self.is_p2p = True
        super().__init__()

    def marshal(self) -> bytes:
        """
        Marshal the message into the following representation:
        - first byte is the message type (always 19)
        - next 6 bytes are the timestamp

        :return: byte representation of the message
        """
        buf = bytearray()
        buf.append(self.TYPE)
        buf.extend(self.timestamp)
        # TODO: figure out the rest of this MissingMessageResponse
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw:  bytes):
        msg_type, data = raw[0], raw[1:]
        if msg_type != cls.TYPE:
            raise ValueError("Invalid message type ({})".format(msg_type))

        timestamp, data = data[:6], data[6:]
        b, data = data[0], data[1:]
        # TODO: figure out the rest of this MissingMessageResponse

        return MissingMessageResponse(
            timestamp=timestamp,
        )
