import smartpy as sp

class FA2ErrorMessage:
    PREFIX = "FA2_"
    TOKEN_UNDEFINED = "{}TOKEN_UNDEFINED".format(PREFIX)
    INSUFFICIENT_BALANCE = "{}INSUFFICIENT_BALANCE".format(PREFIX)
    NOT_OWNER = "{}NOT_OWNER".format(PREFIX)
    OPERATORS_UNSUPPORTED = "{}OPERATORS_UNSUPPORTED".format(PREFIX)

class FKBErrorMessage:
    PREFIX = "FKB_"
    CREATION_LIMIT_EXCEEDED = "{}CREATION_LIMIT_EXCEEDED".format(PREFIX)
    CANT_MINT_SAME_TOKEN_TWICE = "{}CANT_MINT_SAME_TOKEN_TWICE".format(PREFIX)
    CONTRACT_IS_PAUSED = "{}CONTRACT_IS_PAUSED".format(PREFIX)
    MIN_VALUE_SHOULD_BE_MORE_THAN_ZERO = "{}MIN_VALUE_SHOULD_BE_MORE_THAN_ZERO".format(
        PREFIX)
    INCORRECT_PURCHASE_VALUE = "{}INCORRECT_PURCHASE_VALUE".format(PREFIX)

# Declaring Ledger Key-Value types
class LedgerKey:
    def get_type():
        return sp.TRecord(owner=sp.TAddress, token_id=sp.TNat).layout(("owner", "token_id"))
    def make(owner, token_id):
        return sp.set_type_expr(sp.record(owner=owner, token_id=token_id), LedgerKey.get_type())

# Declaring Token metadata Key-Value types
class TokenMetadataValue:
    def get_type():
        return sp.TRecord(
            token_id=sp.TNat,
            token_info=sp.TMap(sp.TString, sp.TBytes)
        ).layout(("token_id", "token_info"))

# Declaring Marketplace Key-Value types
class marketplace:
    def get_value_type():
        return sp.TRecord(
            seller=sp.TAddress,
            sale_value=sp.TMutez,
        )
    def get_key_type():
        """ FKB Token ID """
        return sp.TNat

# Declaring Token Key-Value types
class TokenValue:
    def get_type():
        return sp.TRecord(global_card_id=sp.TNat, player_id=sp.TNat, year=sp.TNat, type=sp.TString, edition_no=sp.TNat, ipfs_string=sp.TString).layout(("global_card_id", ("player_id", ("year", ("type", ("edition_no", ("ipfs_string")))))))

# Smart Contract 
class FKB(sp.Contract):
    def __init__(self, admin, metadata):
        self.init(
            administrator = admin,
            metadata = metadata,
            all_tokens=sp.set(t=sp.TNat),
            character_ledger=sp.big_map(tkey=LedgerKey.get_type(), tvalue=sp.TNat),
            objects_ledger=sp.big_map(tkey=LedgerKey.get_type(), tvalue=sp.TNat),
            token_metadata=sp.big_map(tkey=sp.TNat, tvalue=TokenMetadataValue.get_type()),
            marketplace=sp.big_map(tkey=marketplace.get_key_type(), tvalue=marketplace.get_value_type()),
            paused=False,
            tokens=sp.big_map(tkey=sp.TNat, tvalue=TokenValue.get_type()),
        )

    def is_administrator(self, sender):
        return sender == self.data.administrator

    @sp.entry_point
    def set_administrator(self, params):
        sp.verify(self.is_administrator(sp.sender),
                  message=FA2ErrorMessage.NOT_OWNER)
        self.data.administrator = params

    def is_paused(self):
        return self.data.paused

    @sp.entry_point
    def set_pause(self, params):
        sp.verify(self.is_administrator(sp.sender),
                  message=FA2ErrorMessage.NOT_OWNER)
        self.data.paused = params

    @sp.entry_point
    def mint(self, params):
        sp.verify(~self.is_paused(), FKBErrorMessage.CONTRACT_IS_PAUSED)
        sp.verify(self.is_administrator(sp.sender),
                  message=FA2ErrorMessage.NOT_OWNER)
        token_id = sp.len(self.data.all_tokens)
        sp.verify(~ self.data.all_tokens.contains(token_id),
                  message=FKBErrorMessage.CANT_MINT_SAME_TOKEN_TWICE)
        sp.set_type(params.metadata, sp.TMap(sp.TString, sp.TBytes))
        user = LedgerKey.make(sp.sender, token_id)
        self.data.ledger[user] = 1
        self.data.token_metadata[token_id] = sp.record(
            token_id=token_id, token_info=params.metadata)
        self.data.tokens[token_id] = sp.record(global_card_id=token_id, player_id=params.player_id,
                                               year=params.year, type=params.type, edition_no=params.edition_no, ipfs_string=params.ipfs_string)
        self.data.all_tokens.add(token_id)

    @sp.entry_point
    def transfer(self, batch_transfers):
        sp.verify(~self.is_paused(), FKBErrorMessage.CONTRACT_IS_PAUSED)
        sp.set_type(batch_transfers, BatchTransfer.get_type())
        sp.for transfer in batch_transfers:
            sp.for tx in transfer.txs:
                sp.if (tx.amount > sp.nat(0)):
                    from_user = LedgerKey.make(transfer.from_, tx.token_id)
                    to_user = LedgerKey.make(tx.to_, tx.token_id)
                    sp.verify(self.data.all_tokens.contains(
                        tx.token_id), FA2ErrorMessage.TOKEN_UNDEFINED)
                    sp.verify((self.data.ledger[from_user] >= tx.amount),
                              message=FA2ErrorMessage.INSUFFICIENT_BALANCE)
                    sp.verify((sp.sender == transfer.from_) | (
                        sp.source == transfer.from_), message=FA2ErrorMessage.NOT_OWNER)
                    self.data.ledger[from_user] = sp.as_nat(
                        self.data.ledger[from_user] - tx.amount)
                    self.data.ledger[to_user] = self.data.ledger.get(
                        to_user, 0) + tx.amount
                sp.if self.data.marketplace.contains(tx.token_id):
                    del self.data.marketplace[tx.token_id]
