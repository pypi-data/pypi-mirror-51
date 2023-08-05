import struct
from factom_core.utils import varint


class AdminMessage:
    """
    Base class to inherit from
    """

    def marshal(self):
        raise NotImplementedError("Must be implemented by subclasses")

    @classmethod
    def unmarshal(cls, raw: bytes):
        raise NotImplementedError("Must be implemented by subclasses")


class MinuteNumber(AdminMessage):
    ADMIN_ID = 0x00
    MESSAGE_SIZE = 1

    def __init__(self, minute: int):
        """
        Minute marker (Deprecated in M2).

        :param minute: the preceding data was acknowledged before this minute
        """
        assert 1 <= minute <= 10, 'minute must be in range(1, 11)'
        self.minute = minute

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - single byte encoding the minute number

        :return: bytes representation of the MinuteNumber message
        """
        buf = bytearray()
        buf.append(self.minute)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new MinuteNumber message object
        """
        minute, data = raw[0], raw[1:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return MinuteNumber(minute)


class DirectoryBlockSignature(AdminMessage):
    ADMIN_ID = 0x01
    MESSAGE_SIZE = 128

    def __init__(self, chain_id: bytes, public_key: bytes, signature: bytes):
        """
        A signature of the preceding Directory Block header.

        :param chain_id: the servers 32 byte identity ChainID
        :param public_key: a 32 byte Ed25519 public key in that identity
        :param signature: a 64 byte signature of the previous Directory Block's header
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert len(public_key) == 32, 'public_key must be a bytes object of length 32'
        assert len(signature) == 64, 'signature must be a bytes object of length 64'
        self.chain_id = chain_id
        self.public_key = public_key
        self.signature = signature

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first 32 bytes are the server's identity ChainID
        - next 32 bytes are the Ed25519 public key in that identity
        - next 64 bytes are the signature of the previous Directory Block's header

        :return: bytes representation of the DirectoryBlockSignature message
        """
        buf = bytearray()
        buf.extend(self.chain_id)
        buf.extend(self.public_key)
        buf.extend(self.signature)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new DirectoryBlockSignature message object
        """
        chain_id, data = raw[:32], raw[32:]
        public_key, data = data[:32], data[32:]
        signature, data = data[:64], data[64:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return DirectoryBlockSignature(chain_id, public_key, signature)
    

class MatryoshkaHashReveal(AdminMessage):
    ADMIN_ID = 0x02
    MESSAGE_SIZE = 64

    def __init__(self, chain_id: bytes, matryoshka_hash_reveal: bytes):
        """
        This is the latest M-hash reveal to be considered for determining server priority in subsequent blocks.

        :param chain_id: the servers 32 byte identity ChainID
        :param matryoshka_hash_reveal: 32 bytes for the M-hash reveal itself
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert len(matryoshka_hash_reveal) == 32, 'matryoshka_hash_reveal must be a bytes object of length 32'
        self.chain_id = chain_id
        self.matryoshka_hash_reveal = matryoshka_hash_reveal

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first 32 bytes are the server's identity ChainID
        - next 32 bytes for the new M-hash reveal itself

        :return: bytes representation of the MatryoshkaHashReveal message
        """
        buf = bytearray()
        buf.extend(self.chain_id)
        buf.extend(self.matryoshka_hash_reveal)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new MatryoshkaHashReveal message object
        """
        chain_id, data = raw[:32], raw[32:]
        matryoshka_hash_reveal, data = data[:32], data[32:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return MatryoshkaHashReveal(chain_id, matryoshka_hash_reveal)


class MatryoshkaHashAddOrReplace(AdminMessage):
    ADMIN_ID = 0x03
    MESSAGE_SIZE = 64

    def __init__(self, chain_id: bytes, new_matryoshka_hash: bytes):
        """
        This is a command which adds or replaces the current M-hash for the specified identity with this new M-hash.
        This data is replicated from the server's identity chain.

        :param chain_id: the servers 32 byte identity ChainID
        :param new_matryoshka_hash: 32 bytes for the new M-hash itself
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert len(new_matryoshka_hash) == 32, 'new_matryoshka_hash must be a bytes object of length 32'
        self.chain_id = chain_id
        self.new_matryoshka_hash = new_matryoshka_hash

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first 32 bytes are the server's identity ChainID
        - next 32 bytes for the new M-hash itself

        :return: bytes representation of the MatryoshkaHashAddOrReplace message
        """
        buf = bytearray()
        buf.extend(self.chain_id)
        buf.extend(self.new_matryoshka_hash)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new MatryoshkaHashAddOrReplace message object
        """
        chain_id, data = raw[:32], raw[32:]
        new_matryoshka_hash, data = data[:32], data[32:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return MatryoshkaHashAddOrReplace(chain_id, new_matryoshka_hash)
    

class ServerCountIncrease(AdminMessage):
    ADMIN_ID = 0x04
    MESSAGE_SIZE = 1

    def __init__(self, value):
        """
        This is a command to increase the number of servers.

        :param value: the server count is incremented by this amount
        """
        assert 0 <= value <= 255, 'value must be in range(0, 256)'
        self.value = value

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - single byte encoding the amount to increase the count by

        :return: bytes representation of the ServerCountIncrease message
        """
        buf = bytearray()
        buf.append(self.value)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new ServerCountIncrease message object
        """
        value, data = raw[0], raw[1:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return ServerCountIncrease(value)

    
class AddFederatedServer(AdminMessage):
    ADMIN_ID = 0x05
    MESSAGE_SIZE = 36

    def __init__(self, chain_id: bytes, activation_height: int):
        """
        Add the specified identity to the pool of Federated Servers

        :param chain_id: the servers 32 byte identity ChainID
        :param activation_height: the Directory Block height that it takes effect
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert activation_height >= 0, 'activation_height must not be negative'
        self.chain_id = chain_id
        self.activation_height = activation_height

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first 32 bytes are the ChainID of the Federated server which is added to the pool
        - next 4 bytes are the Directory Block height that it takes effect

        :return: bytes representation of the AddFederatedServer message
        """
        buf = bytearray()
        buf.extend(self.chain_id)
        buf.extend(struct.pack('>I', self.activation_height))
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new AddFederatedServer message object
        """
        chain_id, data = raw[:32], raw[32:]
        activation_height, data = struct.unpack('>I', data[:4])[0], data[4:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return AddAuditServer(chain_id, activation_height)
    
    
class AddAuditServer(AdminMessage):
    ADMIN_ID = 0x06
    MESSAGE_SIZE = 36

    def __init__(self, chain_id: bytes, activation_height: int):
        """
        Add the specified identity to the pool of Audit Servers

        :param chain_id: the servers 32 byte identity ChainID
        :param activation_height: the Directory Block height that it takes effect
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert activation_height >= 0, 'activation_height must not be negative'
        self.chain_id = chain_id
        self.activation_height = activation_height

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first 32 bytes are the ChainID of the Audit server which is added to the pool
        - next 4 bytes are the Directory Block height that it takes effect

        :return: bytes representation of the AddAuditServer message
        """
        buf = bytearray()
        buf.extend(self.chain_id)
        buf.extend(struct.pack('>I', self.activation_height))
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new AddAuditServer message object
        """
        chain_id, data = raw[:32], raw[32:]
        activation_height, data = struct.unpack('>I', data[:4])[0], data[4:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return AddAuditServer(chain_id, activation_height)
    

class RemoveFederatedServer(AdminMessage):
    ADMIN_ID = 0x07
    MESSAGE_SIZE = 36

    def __init__(self, chain_id: bytes, activation_height: int):
        """
        Remove the specified identity from the pool of Federated Servers (also can be used to remove an Audit server)
        All public keys associated with it are removed as well.

        :param chain_id: the servers 32 byte identity ChainID
        :param activation_height: the Directory Block height that it takes effect
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert activation_height >= 0, 'activation_height must not be negative'
        self.chain_id = chain_id
        self.activation_height = activation_height

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first 32 bytes are the ChainID of the Federated server which is removed from the pool
        - next 4 bytes are the Directory Block height that it takes effect

        :return: bytes representation of the RemoveFederatedServer message
        """
        buf = bytearray()
        buf.extend(self.chain_id)
        buf.extend(struct.pack('>I', self.activation_height))
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new RemoveFederatedServer message object
        """
        chain_id, data = raw[:32], raw[32:]
        activation_height, data = struct.unpack('>I', data[:4])[0], data[4:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return RemoveFederatedServer(chain_id, activation_height)
    

class AddFederatedServerSigningKey(AdminMessage):
    ADMIN_ID = 0x08
    MESSAGE_SIZE = 69

    def __init__(self, chain_id: bytes, priority: int, new_public_key: bytes, activation_height: int):
        """
        This adds an Ed25519 public key to the specified identity in the authority set.
        If the specified key for this server already exists, this replaces the old one.

        :param chain_id: the servers 32 byte identity ChainID
        :param priority: the key's priority level
        :param new_public_key: the new 32 byte Ed25519 public key
        :param activation_height: the Directory Block height that it takes effect
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert 0 <= priority <= 255, 'priority must be in range(0, 256)'
        assert len(new_public_key) == 32, 'new_public_key must be a bytes object of length 32'
        assert activation_height >= 0, 'activation_height must not be negative'
        self.chain_id = chain_id
        self.priority = priority
        self.new_public_key = new_public_key
        self.activation_height = activation_height

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first 32 bytes are the server's identity ChainID
        - next byte is the key priority
        - next 32 bytes are the public key itself
        - next 4 bytes are the activation height

        :return: bytes representation of the AddFederatedServerSigningKey message
        """
        buf = bytearray()
        buf.extend(self.chain_id)
        buf.append(self.priority)
        buf.extend(self.new_public_key)
        buf.extend(struct.pack('>I', self.activation_height))
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new AddFederatedServerSigningKey message object
        """
        chain_id, data = raw[:32], raw[32:]
        priority, data = data[0], data[1:]
        new_public_key, data = data[:32], data[32:]
        activation_height, data = struct.unpack('>I', data[:4])[0], data[4:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return AddFederatedServerSigningKey(chain_id, priority, new_public_key, activation_height)


class AddFederatedServerBitcoinAnchorKey(AdminMessage):
    ADMIN_ID = 0x09
    MESSAGE_SIZE = 54  # TODO: IS THIS TRUE MESSAGE SIZE?

    #
    # ChainID. . N. N.
    def __init__(self, chain_id: bytes, priority: int, hash_type: int, public_key_hash: bytes):
        """
        This adds a Bitcoin public key hash to the authority set.
        If the specified priority for the server already exists, this replaces the old one.

        :param chain_id: the server's 32 byte identity ChainID
        :param priority:
        :param hash_type:
        :param public_key_hash:
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert hash_type == 0 or hash_type == 1, 'hash_type must be 0 (p2pkh) or 1 (p2sh)'
        assert 0 <= priority <= 255, 'priority must be in range(0, 256)'
        assert len(public_key_hash) == 20, 'public_key_hash must be a bytes object of length 20'
        self.chain_id = chain_id
        self.priority = priority
        self.hash_type = hash_type
        self.public_key_hash = public_key_hash

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first 32 bytes are the server's identity ChainID
        - next byte is the key priority
        - next byte is 0=P2PKH 1=P2SH
        - next 20 bytes are the HASH160 of the ECDSA public key

        :return: bytes representation of the AddFederatedServerBitcoinAnchorKey message
        """
        buf = bytearray()
        buf.extend(self.chain_id)
        buf.append(self.priority)
        buf.append(self.hash_type)
        buf.extend(self.public_key_hash)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new AddFederatedServerBitcoinAnchorKey message object
        """
        chain_id, data = raw[:32], raw[32:]
        priority, data = data[0], data[1:]
        hash_type, data = data[0], data[1:]
        public_key_hash, data = data[:20], data[20:]
        assert len(data) == 0, 'Extra bytes remaining!'
        return AddFederatedServerBitcoinAnchorKey(chain_id, priority, hash_type, public_key_hash)
    
    
class ServerFaultHandoff(AdminMessage):
    ADMIN_ID = 0x0A
    MESSAGE_SIZE = 0
    """
    This holds a rollup of all the messages which were sent out by the federated servers which authorize
    the removal of one server and the promotion of another server. This is not currently serialized into
    the blockchain.
    """


class CoinbaseDescriptor(AdminMessage):
    ADMIN_ID = 0x0B
    MAX_MESSAGE_SIZE = 10232

    def __init__(self, outputs: list):
        """
        The coinbase descriptor is an entry in the Admin block which specifies a number of factoid output addresses and
        amounts. These outputs are used to deterministically generate a coinbase transaction 1000 blocks (about 7 days)
        later. This delay is to allow 7 days to respond to software bugs, etc. It is included in each block height that
        is divisible by 25. There can only be one per Admin block.

        :param outputs: the outputs to include in the coinbase transactions 1000 blocks in the future
        """
        for output in outputs:
            assert "value" in output and "fct_address" in output, \
                "Invalid output! Must contain a value and a fct_address"
            value, fct_address = output["value"], output["fct_address"]
            assert isinstance(value, int) and value >=0, \
                "Invalid output! `value` must be a positive integer"
            assert isinstance(fct_address, bytes) and len(fct_address) == 32, \
                'Invalid output! fct_address must be a bytes object of length 32'
        self.outputs = outputs

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first byte is a length descriptor varint (10232 at the maximum)
        - next varint bytes is the descriptor height at which the output will not be created
        - next varint bytes is the index into the specified descriptor that will not be created

        The Coinbase Descriptor cannot be larger than 10233 bytes:
        (1 AdminID byte + 2 varint length bytes + (10 KiB max FCT tx - 10 header bytes of coinbase))

        :return: bytes representation of the CoinbaseDescriptor message
        """
        buf = bytearray()
        bodybuf = bytearray()
        for output in self.outputs:
            bodybuf.extend(varint.encode(output.get("value")))
            bodybuf.extend(output.get("fct_address"))
        buf.extend(varint.encode(len(bodybuf)))
        buf.extend(bodybuf)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new CoinbaseDescriptor message object
        """
        msg, data = CoinbaseDescriptor.unmarshal_with_remainder(raw)
        assert len(data) == 0, 'Extra bytes remaining!'
        return msg

    @classmethod
    def unmarshal_with_remainder(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object and return the remaining bytes

        :param raw: marshalled bytes of the message
        :return: a tuple of (new CoinbaseDescriptor message object, remaining bytes)
        """
        message_size, data = varint.decode(raw)
        message_data, data = data[:message_size], data[message_size:]
        outputs = []
        while len(message_data) > 0:
            value, message_data = varint.decode(message_data)
            fct_address, message_data = message_data[:32], message_data[32:]
            outputs.append({
                "value": value,
                "fct_address": fct_address
            })
        assert len(message_data) == 0, 'Extra bytes remaining in message data!'
        return CoinbaseDescriptor(outputs), data
    
    
class CoinbaseDescriptorCancel(AdminMessage):
    ADMIN_ID = 0x0C
    MAX_MESSAGE_SIZE = 8

    def __init__(self, descriptor_height: int, descriptor_index: int):
        """
        This cancels a specific output index in an earlier Coinbase Descriptor.
        It is only effective in a block between when the Coinbase Descriptor is created and when the coinbase is
        included in the Factoid Block (non-inclusive).

        :param descriptor_height: the height at which to target the CoinbaseDescriptor
        :param descriptor_index: this index into the specified descriptor will not be created
        """
        assert descriptor_height >= 0, 'descriptor_height must not be negative'
        assert descriptor_index >= 0, 'descriptor_index must not be negative'
        self.descriptor_height = descriptor_height
        self.descriptor_index = descriptor_index

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first byte is a length descriptor varint (8 at the maximum)
        - next varint bytes is the descriptor height at which the output will not be created
        - next varint bytes is the index into the specified descriptor that will not be created

        :return: bytes representation of the CoinbaseDescriptorCancel message
        """
        buf = bytearray()
        bodybuf = bytearray()
        bodybuf.extend(varint.encode(self.descriptor_height))
        bodybuf.extend(varint.encode(self.descriptor_index))
        buf.extend(varint.encode(len(bodybuf)))
        buf.extend(bodybuf)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new CoinbaseDescriptorCancel message object
        """
        msg, data = CoinbaseDescriptorCancel.unmarshal_with_remainder(raw)
        assert len(data) == 0, 'Extra bytes remaining!'
        return msg

    @classmethod
    def unmarshal_with_remainder(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object and return the remaining bytes

        :param raw: marshalled bytes of the message
        :return: a tuple of (new CoinbaseDescriptorCancel message object, remaining bytes)
        """
        message_size, data = varint.decode(raw)
        message_data, data = data[:message_size], data[message_size:]
        descriptor_height, message_data = varint.decode(message_data)
        descriptor_index, message_data = message_data[:32], message_data[32:]
        assert len(message_data) == 0, 'Extra bytes remaining in message data!'
        return CoinbaseDescriptorCancel(descriptor_height, descriptor_index), data
    
    
class AddAuthorityFactoidAddress(AdminMessage):
    ADMIN_ID = 0x0D
    MESSAGE_SIZE = 65

    def __init__(self, chain_id: bytes, fct_address: bytes):
        """
        This sets a Factoid address to be used in the Coinbase Descriptor.
        If the specified address for this identity already exists, this replaces the old one.

        :param chain_id: the server's 32 byte identity ChainID
        :param fct_address:
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert len(fct_address) == 32, 'fct_address must be a bytes object of length 32'
        self.chain_id = chain_id
        self.fct_address = fct_address

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first byte is a length descriptor varint (always 64)
        - next 32 bytes are the server's identity ChainID
        - next 32 bytes are the Factoid address (RCD Hash)

        :return: bytes representation of the AddAuthorityFactoidAddress message
        """
        buf = bytearray()
        buf.append(64)
        buf.extend(self.chain_id)
        buf.extend(self.fct_address)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new AddAuthorityFactoidAddress message object
        """
        data = raw[1:]  # Skip message length, always 64
        chain_id, data = data[:32], data[32:]
        fct_address, data = data[:32], data[32:]
        return AddAuthorityFactoidAddress(chain_id, fct_address)
    
    
class AddAuthorityEfficiency(AdminMessage):
    ADMIN_ID = 0x0E
    MESSAGE_SIZE = 35

    def __init__(self, chain_id: bytes, efficiency_percentage: int):
        """
        This sets what percentage of the Factoid rewards for the specified server are yeilded to the Grant Pool.
        This command overrides the previous efficiency settings for this identity.

        :param chain_id: the server's 32 byte identity ChainID
        :param efficiency_percentage:
        """
        assert len(chain_id) == 32, 'chain_id must be a bytes object of length 32'
        assert 0 <= efficiency_percentage <= 10000 , 'efficiency_percentage must be in range(0, 10000)'
        # TODO: is this efficiency assertion right?
        self.chain_id = chain_id
        self.efficiency_percentage = efficiency_percentage

    def marshal(self):
        """
        Marshal the object into its byte representation:
        - the first byte is a length descriptor varint (always 34)
        - next 32 bytes are the server's identity ChainID
        - next 2 bytes are a big endian representation of the percentage with 2 fixed decimals

        :return: bytes representation of the AddAuthorityEfficiency message
        """
        buf = bytearray()
        buf.extend(self.chain_id)
        buf.extend(struct.pack('>H', self.efficiency_percentage))
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """
        Unmarshal the byte representation into a new object

        :param raw: marshalled bytes of the message
        :return: new AddAuthorityEfficiency message object
        """
        data = raw[1:]  # Skip message length, always 34
        chain_id, data = data[:32], data[32:]
        efficiency_percentage, data = struct.unpack('>H', data[:4])[0], data[4:]
        return AddAuthorityEfficiency(chain_id, efficiency_percentage)
