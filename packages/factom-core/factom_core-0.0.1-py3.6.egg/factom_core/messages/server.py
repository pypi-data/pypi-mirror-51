from factom_core.messages import Message


class AddServer(Message):
    """
    Add the identity as a Federated or Audit server
    """

    TYPE = 22

    def __init__(self, timestamp: bytes, chain_id: bytes, is_federated: bool, public_key: bytes, signature: bytes):
        # TODO: type/value assertions
        self.timestamp = timestamp
        self.chain_id = chain_id
        self.is_federated = is_federated
        self.public_key = public_key
        self.signature = signature
        super().__init__()

    def marshal(self) -> bytes:
        """
        Marshal the message into the following representation:
        - first byte is the message type (always 22)
        - next 6 bytes are a timestamp
        - next 32 bytes are the server's identity chain id
        - next byte is the server type (0 == Federated, 1 == Audit)
        - next 32 bytes are the public key signing this message
        - next 64 bytes are the signature

        :return: byte representation of the message
        """
        buf = bytearray()
        buf.append(self.TYPE)
        buf.extend(self.timestamp)
        buf.extend(self.chain_id)
        buf.append(0 if self.is_federated else 1)
        buf.extend(self.public_key)
        buf.extend(self.signature)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw:  bytes):
        msg_type, data = raw[0], raw[1:]
        if msg_type != cls.TYPE:
            raise ValueError("Invalid message type ({})".format(msg_type))

        timestamp, data = data[:6], data[6:]
        chain_id, data = data[:32], data[32:]
        server_type, data = data[0], data[1:]
        public_key, data = data[:32], data[32:]
        signature, data = data[:64], data[64:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return AddServer(
            timestamp=timestamp,
            chain_id=chain_id,
            is_federated=(server_type == 0),  # 0 == Federated, 1 == Audit
            public_key=public_key,
            signature=signature,
        )


class ChangeServerKey(Message):
    """
    Change the key for the specified server identity
    """

    TYPE = 23

    CHANGE_TYPE_ADD_MATRYOSHKA = 0x03
    CHANGE_TYPE_ADD_FED_SERVER_KEY = 0x08
    CHANGE_TYPE_ADD_BTC_ANCHOR_KEY = 0x09

    def __init__(self, timestamp: bytes, chain_id: bytes, admin_block_change: int, key_type: int, priority: int,
                 new_key: bytes, public_key: bytes, signature: bytes):
        # TODO: type/value assertions
        self.timestamp = timestamp
        self.chain_id = chain_id
        self.admin_block_change = admin_block_change
        self.key_type = key_type
        self.priority = priority
        self.new_key = new_key
        self.public_key = public_key
        self.signature = signature
        super().__init__()

    def marshal(self) -> bytes:
        """
        Marshal the message into the following representation:
        - first byte is the message type (always 23)
        - next 6 bytes are a timestamp
        - next 32 bytes are the server's identity chain id
        - next byte is Admin Block Change
        - next byte is the key type
        - next byte is the key priority
        - next 32 bytes are the new public key for the identity
        - next 32 bytes are the public key signing this message
        - next 64 bytes are the signature

        :return: byte representation of the message
        """
        buf = bytearray()
        buf.append(self.TYPE)
        buf.extend(self.timestamp)
        buf.extend(self.chain_id)
        buf.append(self.admin_block_change)
        buf.append(self.key_type)
        buf.append(self.priority)
        buf.extend(self.new_key)
        buf.extend(self.public_key)
        buf.extend(self.signature)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw:  bytes):
        msg_type, data = raw[0], raw[1:]
        if msg_type != cls.TYPE:
            raise ValueError("Invalid message type ({})".format(msg_type))

        timestamp, data = data[:6], data[6:]
        chain_id, data = data[:32], data[32:]
        admin_block_change, data = data[0], data[1:]
        key_type, data = data[0], data[1:]
        priority, data = data[0], data[1:]
        new_key, data = data[:32], data[32:]
        public_key, data = data[:32], data[32:]
        signature, data = data[:64], data[64:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return ChangeServerKey(
            timestamp=timestamp,
            chain_id=chain_id,
            admin_block_change=admin_block_change,
            key_type=key_type,
            priority=priority,
            new_key=new_key,
            public_key=public_key,
            signature=signature,
        )


class RemoveServer(Message):
    """
    Remove the identity as a Federated or Audit server
    """

    TYPE = 24

    def __init__(self, timestamp: bytes, chain_id: bytes, is_federated: bool, public_key: bytes, signature: bytes):
        # TODO: type/value assertions
        self.timestamp = timestamp
        self.chain_id = chain_id
        self.is_federated = is_federated
        self.public_key = public_key
        self.signature = signature
        super().__init__()

    def marshal(self) -> bytes:
        """
        Marshal the message into the following representation:
        - first byte is the message type (always 24)
        - next 6 bytes are a timestamp
        - next 32 bytes are the server's identity chain id
        - next byte is the server type (0 == Federated, 1 == Audit)
        - next 32 bytes are the public key signing this message
        - next 64 bytes are the signature

        :return: byte representation of the message
        """
        buf = bytearray()
        buf.append(self.TYPE)
        buf.extend(self.timestamp)
        buf.extend(self.chain_id)
        buf.append(0 if self.is_federated else 1)
        buf.extend(self.public_key)
        buf.extend(self.signature)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw:  bytes):
        msg_type, data = raw[0], raw[1:]
        if msg_type != cls.TYPE:
            raise ValueError("Invalid message type ({})".format(msg_type))

        timestamp, data = data[:6], data[6:]
        chain_id, data = data[:32], data[32:]
        server_type, data = data[0], data[1:]
        public_key, data = data[:32], data[32:]
        signature, data = data[:64], data[64:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return RemoveServer(
            timestamp=timestamp,
            chain_id=chain_id,
            is_federated=(server_type == 0),  # 0 == Federated, 1 == Audit
            public_key=public_key,
            signature=signature,
        )
