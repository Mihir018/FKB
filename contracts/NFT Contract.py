import smartpy as sp

class FA2ErrorMessage:
    PREFIX                  = "FA2 : "
    TOKEN_UNDEFINED         = "{}TOKEN_UNDEFINED".format(PREFIX)
    INSUFFICIENT_BALANCE    = "{}INSUFFICIENT_BALANCE".format(PREFIX)
    NOT_OWNER               = "{}NOT_OWNER".format(PREFIX)
    OPERATORS_UNSUPPORTED   = "{}OPERATORS_UNSUPPORTED".format(PREFIX)

class FKBErrorMessage:
    PREFIX                              = "FKB : "
    CANT_MINT_SAME_TOKEN_TWICE          = "{}CANT_MINT_SAME_TOKEN_TWICE".format(PREFIX)
    CONTRACT_IS_NOT_ACTIVE              = "{}CONTRACT_IS_NOT_ACTIVE".format(PREFIX)
    MIN_VALUE_SHOULD_BE_MORE_THAN_ZERO  = "{}MIN_VALUE_SHOULD_BE_MORE_THAN_ZERO".format(PREFIX)
    INCORRECT_PURCHASE_VALUE            = "{}INCORRECT_PURCHASE_VALUE".format(PREFIX)
    OBJECT_IS_NOT_SHAREABLE             = "{}OBJECT_IS_NOT_SHAREABLE".format(PREFIX)


# Declaring Object Ledger Key-Value types
class ObjectLedgerValue:
    def get_type():
        return sp.TRecord(
            object_id           = sp.TNat,
            object_name         = sp.TString,
            object_type         = sp.TString,
            object_location     = sp.TString,
            object_owner        = sp.TAddress,
            object_is_shareable = sp.TBool,
            object_amount       = sp.TMutez)
            
    def make(object_id, object_name, object_type, object_location, object_owner, object_is_shareable, object_amount):
        return sp.set_type_expr(sp.record(object_id = object_id, object_name = object_name, object_type = object_type, object_location = object_location, object_owner = object_owner, object_is_shareable = object_is_shareable, object_amount = object_amount), ObjectLedgerValue.get_type())

# Declaring Character Ledger Key-Value types
class CharacterLedgerValue:
    def get_type():
        return sp.TRecord(
            character_id        = sp.TNat, 
            character_name      = sp.TString,
            character_dna       = sp.TRecord(
                    head    = sp.TNat,
                    jeans   = sp.TNat,
                    logo    = sp.TNat,
                    shirt   = sp.TNat,
                    shoes   = sp.TNat
                    ),
            character_location  = sp.TString,
            character_owner     = sp.TAddress,
            character_amount    = sp.TMutez
            )
            
    def make(character_id, character_name, character_dna, character_location, character_owner, character_amount):
        return sp.set_type_expr(sp.record(character_id = character_id, character_name = character_name, character_dna = character_dna, character_location = character_location, character_owner = character_owner, character_amount = character_amount), CharacterLedgerValue.get_type())

# Declaring Token metadata Key-Value types
class TokenMetadataValue:
    def get_type():
        return sp.TRecord(
            token_id    = sp.TNat,
            name        = sp.TString,
            ipfs_link   = sp.TString,
            owner       = sp.TAddress)

# Declaring Marketplace Key-Value types
class marketplace:
    def get_value_type():
        return sp.TRecord(
            seller      = sp.TAddress,
            sale_value  = sp.TMutez)
    def get_key_type():
        """ FKB Token ID """
        return sp.TNat

# Smart Contract 
class FKB(sp.Contract):
    def __init__(self, admin, metadata):
        self.init(
            administrator       = admin,                                                                                    # Admin address is stored
            metadata            = metadata,                                                                                 # Contract metadata is stored
            objects_ledger      = sp.big_map(tkey = sp.TNat, tvalue = ObjectLedgerValue.get_type()),                        # All Objects are stored
            characters_ledger   = sp.big_map(tkey = sp.TNat, tvalue = CharacterLedgerValue.get_type()),                     # All Characters are stored
            all_tokens          = sp.set(t = sp.TNat),                                                                      # Set of all tokens available
            token_metadata      = sp.big_map(tkey = sp.TNat, tvalue = TokenMetadataValue.get_type()),                       # Metadata about Tokens is stored
            marketplace         = sp.big_map(tkey = marketplace.get_key_type(), tvalue = marketplace.get_value_type()),     # All the NFT's listed on Market are stored
            active              = True,                                                                                     # Tells if the contract is active
            )

    def is_administrator(self, sender):
        return sender == self.data.administrator

    @sp.entry_point
    def set_administrator(self, params):
        sp.verify(self.is_administrator(sp.sender),
                  message = FA2ErrorMessage.NOT_OWNER)
        self.data.administrator = params

    def is_active(self):
        return self.data.active

    @sp.entry_point
    def toggle_active(self):
        sp.verify(self.is_administrator(sp.sender),
                  message = FA2ErrorMessage.NOT_OWNER)
        self.data.active = ~self.data.active

    @sp.entry_point
    def mint_object(self, params):
        sp.verify(self.is_active(), FKBErrorMessage.CONTRACT_IS_NOT_ACTIVE)
        token_id = sp.len(self.data.all_tokens)
        sp.verify(~ self.data.all_tokens.contains(token_id),
                    message = FKBErrorMessage.CANT_MINT_SAME_TOKEN_TWICE)
        new_obj = ObjectLedgerValue.make(token_id, params.object_name, params.object_type, params.object_location, sp.sender, params.object_is_shareable, params.object_amount)
        self.data.objects_ledger[token_id] = new_obj
        token_metadata_value = sp.record(
                                    token_id    = token_id,
                                    name        = params.object_name,
                                    ipfs_link   = params.object_location,
                                    owner       = sp.sender)
        self.data.all_tokens.add(token_id)

    @sp.entry_point
    def mint_character(self, params):
        sp.verify(self.is_active(), FKBErrorMessage.CONTRACT_IS_NOT_ACTIVE)
        token_id = sp.len(self.data.all_tokens)
        sp.verify(~ self.data.all_tokens.contains(token_id),
                    message = FKBErrorMessage.CANT_MINT_SAME_TOKEN_TWICE)
        new_char = CharacterLedgerValue.make(character_id = token_id, character_name = params.character_name, character_dna = params.character_dna, character_location = params.character_location, character_owner = sp.sender, character_amount = params.character_amount)
        self.data.characters_ledger[token_id] = new_char
        token_metadata_value = sp.record(
                                    token_id    = token_id,
                                    name        = params.character_name,
                                    ipfs_link   = params.character_location,
                                    owner       = sp.sender)
        self.data.all_tokens.add(token_id)

    @sp.entry_point
    def transfer_object(self, params):
        sp.verify(self.is_active(), message = FKBErrorMessage.CONTRACT_IS_NOT_ACTIVE)
        sp.verify(self.data.objects_ledger[params.token_id].object_is_shareable, message = FKBErrorMessage.OBJECT_IS_NOT_SHAREABLE)
        sp.verify_equal(sp.sender, self.data.objects_ledger[params.token_id].object_owner, message = FA2ErrorMessage.NOT_OWNER)
        self.data.objects_ledger[params.token_id].object_owner = params.new_owner

    @sp.entry_point
    def transfer_character(self, params):
        sp.verify(self.is_active(), message = FKBErrorMessage.CONTRACT_IS_NOT_ACTIVE)
        sp.verify_equal(sp.sender, self.data.characters_ledger[params.token_id].character_owner, message = FA2ErrorMessage.NOT_OWNER)
        self.data.characters_ledger[params.token_id].character_owner = params.new_owner
        
    @sp.entry_point
    def add_to_marketplace(self, params):
        sp.verify_equal(sp.sender, self.data.characters_ledger[params.token_id].character_owner, message = FA2ErrorMessage.NOT_OWNER)
        create_sale = sp.record(seller = sp.sender, sale_value = params.sale_value)
        self.data.marketplace[params.token_id] = create_sale
    
    @sp.entry_point
    def remove_from_marketplace(self, params):
        sp.verify_equal(sp.sender, self.data.characters_ledger[params.token_id].character_owner, message = FA2ErrorMessage.NOT_OWNER)
        del self.data.marketplace[params.token_id]

    @sp.entry_point
    def buy_nft(self, params):
        sp.verify_equal(sp.amount, self.data.marketplace[params.token_id].sale_value, message = FKBErrorMessage.INCORRECT_PURCHASE_VALUE)
        self.data.characters_ledger[params.token_id].character_owner = params.new_owner
        self.data.characters_ledger[params.token_id].character_amount = sp.amount
        del self.data.marketplace[params.token_id]

if "templates" not in __name__:
    @sp.add_test(name="FKB NFTs")
    def test():
        sc = sp.test_scenario()
        sc.h1("FKB NFT's and Marketplace")
        sc.h2("Accounts")
        admin = sp.address("tz1LXRS2zgh12gbGix6R9xSLJwfwqM9VdpPW")
        alice = sp.test_account("Alice")
        bob = sp.test_account("Bob")
        dan = sp.test_account("Dan")
        sc.h1("NFT Contract")
        fkb = FKB(admin = admin, metadata = "metadata")
        sc += fkb
        sc.h1("Table of Contents")
        sc.table_of_contents()
        sc.h1("Accounts")
        sc.show([alice, bob, dan])
        sc.h1("FKB NFT Contract")
        sc.h2("Minting Objects")
        obj1 = sp.record(
                object_name          = "Head1",
                object_type          = "head",
                object_location      = "link.com",
                object_is_shareable  = True,
                object_amount        = sp.mutez(823)
            )
        obj2 = sp.record(
                object_name          = "Jeans1",
                object_type          = "jeans",
                object_location      = "link.com",
                object_is_shareable  = True,
                object_amount        = sp.mutez(864)
            )
        obj3 = sp.record(
                object_name          = "Logo1",
                object_type          = "logo",
                object_location      = "link.com",
                object_is_shareable  = True,
                object_amount        = sp.mutez(654)
            )
        obj4 = sp.record(
                object_name          = "Shirt1",
                object_type          = "shirt",
                object_location      = "link.com",
                object_is_shareable  = True,
                object_amount        = sp.mutez(687)
            )
        obj5 = sp.record(
                object_name          = "Shoes1",
                object_type          = "shoes",
                object_location      = "link.com",
                object_is_shareable  = True,
                object_amount        = sp.mutez(867)
            )
        sc += fkb.mint_object(obj1).run(sender = admin, amount = obj1.object_amount)
        sc += fkb.mint_object(obj2).run(sender = admin, amount = obj2.object_amount)
        sc += fkb.mint_object(obj3).run(sender = admin, amount = obj3.object_amount)
        sc += fkb.mint_object(obj4).run(sender = admin, amount = obj4.object_amount)
        sc += fkb.mint_object(obj5).run(sender = admin, amount = obj5.object_amount)
        
        sc.h2("Minting Characters")
        char1 = sp.record(
                character_name      = "Char 1",
                character_dna       = sp.record(
                                head    = 0,
                                jeans   = 1,
                                logo    = 2,
                                shirt   = 3,
                                shoes   = 4
                            ),
                character_location  = "char1.locn",
                character_amount    = sp.mutez(3456)
            )

        char2 = sp.record(
                character_name      = "Char 2",
                character_dna       = sp.record(
                                head    = 80,
                                jeans   = 17,
                                logo    = 62,
                                shirt   = 39,
                                shoes   = 564
                            ),
                character_location  = "char2.locn",
                character_amount    = sp.mutez(8764)
            )

        char3 = sp.record(
                character_name      = "Char 3",
                character_dna       = sp.record(
                                head    = 80,
                                jeans   = 19,
                                logo    = 872,
                                shirt   = 63,
                                shoes   = 894
                            ),
                character_location  = "char3.locn",
                character_amount    = sp.mutez(3283)
            )

        char4 = sp.record(
                character_name      = "Char 4",
                character_dna       = sp.record(
                                head    = 80,
                                jeans   = 19,
                                logo    = 8289,
                                shirt   = 37,
                                shoes   = 684
                            ),
                character_location  = "char4.locn",
                character_amount    = sp.mutez(54895)
            )

        char5 = sp.record(
                character_name      = "Char 5",
                character_dna       = sp.record(
                                head    = 5708,
                                jeans   = 81,
                                logo    = 27,
                                shirt   = 8653,
                                shoes   = 454
                            ),
                character_location  = "char5.locn",
                character_amount    = sp.mutez(23244)
            )

        
        sc += fkb.mint_character(char1).run(sender = admin, amount = char1.character_amount)
        sc += fkb.mint_character(char2).run(sender = admin, amount = char2.character_amount)
        sc += fkb.mint_character(char3).run(sender = admin, amount = char3.character_amount)
        sc += fkb.mint_character(char4).run(sender = admin, amount = char4.character_amount)
        sc += fkb.mint_character(char5).run(sender = admin, amount = char5.character_amount)

