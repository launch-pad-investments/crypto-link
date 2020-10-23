"""
Cogs to handle commands for licensing with the bot

Owners of the community can pay a one time monthly fee which allows them to make unlimited transfers
from Merchant wallet to their won upon withdrawal.
"""

from discord.ext import commands
from discord import Embed, Colour
from cogs.utils.customCogChecks import has_wallet
from backOffice.stellarOnChainHandler import StellarWallet
from cogs.utils.systemMessaages import CustomMessages

from cogs.utils.securityChecks import check_stellar_address
from utils.tools import Helpers

custom_messages = CustomMessages()
helper = Helpers()
auto_channels = helper.read_json_file(file_name='autoMessagingChannels.json')

CONST_STELLAR_EMOJI = "<:stelaremoji:684676687425961994>"
CONST_ACCOUNT_ERROR = '__Account Not Registered__'
stellar_chain = StellarWallet()


class HorizonAccessCommands(commands.Cog):
    """
    Discord Commands dealing with Merchant Licensing
    """

    def __init__(self, bot):
        self.bot = bot
        self.backoffice = bot.backoffice
        self.command_string = bot.get_command_str()

    @commands.group()
    @commands.check(has_wallet)
    async def horizon(self, ctx):
        """
        Entry point for horizon queries
        """

        title = ':sunrise: __Stellar Horizon Access__ :sunrise: '
        description = 'Available Stellar Laboratory commands over Discord.'
        list_of_commands = [
            {"name": f':office_worker: Accounts :office_worker:',
             "value": f'`{self.command_string}horizon accounts`'},

            {"name": f':money_with_wings: Payments :money_with_wings:',
             "value": f'`{self.command_string}horizon payments`'},

            {"name": f':gem: Assets :gem: ',
             "value": f'`{self.command_string}horizon assets`'},

            {"name": f':fireworks: Effects :fireworks: ',
             "value": f'`{self.command_string}horizon effects`'},

            {"name": f':ledger: Ledger :ledger: ',
             "value": f'`{self.command_string}horizon ledger`'},

            {"name": f':clipboard: Offers :clipboard: ',
             "value": f'`{self.command_string}horizon offers`'},

            {"name": f':wrench: Operations :wrench: ',
             "value": f'`{self.command_string}horizon operations`'},

            {"name": f':book: Order Book :book: ',
             "value": f'`{self.command_string}horizon orderbook`'},

            {"name": f':railway_track: Paths :railway_track: ',
             "value": f'`{self.command_string}horizon paths`'},

            {"name": f':bar_chart: Trade Aggregation :chart_with_upwards_trend: ',
             "value": f'`{self.command_string}horizon aggregations`'},
            {"name": f':currency_exchange: Trades :currency_exchange:',
             "value": f'`{self.command_string}horizon trades`'},

            {"name": f':incoming_envelope: Transactions :incoming_envelope: ',
             "value": f'`{self.command_string}horizon Transactions`'}

        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands, description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group(aliases=['acc'])
    async def accounts(self, ctx):
        title = ':office_worker: __Horizon Account Operations__ :office_worker:'
        description = 'Representation of all available commands available to interact with ***Account*** Endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f':new: Create New Account :new: ',
             "value": f'`{self.command_string}accounts create`'},
            {"name": f':mag_right: Query Account Details :mag:',
             "value": f'`{self.command_string}accounts get <Valid Stellar Address>`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def payments(self, ctx):
        """
        End points for payments
        """
        title = ':money_with_wings:  __Horizon Payments Operations__ :money_with_wings: '
        description = 'Representation of all available commands available to interact with ***Payments*** Endpoint on ' \
                      'Stellar Horizon Server. All commands return last 3 transactions done on account, and explorer' \
                      ' link to access older transactions. All transactions are returned in descending order.'
        list_of_commands = [
            {"name": f':map: Get payments by public address :map: ',
             "value": f'`{self.command_string}payments address <address>`'},
            {"name": f':ledger:  Get payments based on ledger sequence :ledger:',
             "value": f'`{self.command_string}payments ledger <ledger sequence>`'},
            {"name": f':hash:  Get payments based on transaction hash :hash:',
             "value": f'`{self.command_string}payments transaction <hash of transaction>`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands, description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def assets(self, ctx):
        title = ':gem: __Horizon Assets Operations__ :gem:'
        description = 'Representation of all available commands available to interact with ***Assets*** Endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f':regional_indicator_c: Query by code :regional_indicator_c: ',
             "value": f'`{self.command_string}assets code <alphanumeric string>`'},
            {"name": f':map: Query by Issuer Address :map:',
             "value": f'`{self.command_string}assets issuer <Issuer address>`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def effects(self, ctx):
        title = ':fireworks: __Horizon Effects Operations__ :fireworks: '
        description = 'Representation of all available commands available to interact with ***Effects*** Endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f':map: Query effects for account :map:',
             "value": f'`{self.command_string}effects account <public account address>`'},
            {"name": f' :ledger: Query effects for ledger :ledger: ',
             "value": f'`{self.command_string}effects ledger <ledger id>`'},
            {"name": f':wrench: Query effects for operations :wrench: ',
             "value": f'`{self.command_string}effects operations <operation id>`'},
            {"name": f':hash: Query effects for transactions :hash: ',
             "value": f'`{self.command_string}effects transaction <transaction hash>`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def ledger(self, ctx):
        title = ':ledger: __Horizon Ledger Operations__ :ledger:'
        description = 'Representation of all available commands available to interact with ***Ledger*** endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f':information_source:  Get information for ledger number :information_source: ',
             "value": f'`{self.command_string}ledger <ledger number>`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def offers(self, ctx):
        title = ':handshake:  __Horizon Offers Queries__ :handshake:  '
        description = 'Representation of all available commands available to interact with ***Effects*** Endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f':id: Single Offer Query :id:',
             "value": f'`{self.command_string}offers single <offer id>`'},
            {"name": f' :map: Offers by Account :map: ',
             "value": f'`{self.command_string}offers account <Account public address>`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def operations(self, ctx):
        title = ':wrench: __Horizon Operations__ :wrench:'
        description = 'Representation of all available commands available to interact with ***Operations*** Endpoint on ' \
                      'Stellar Horizon Server'

        list_of_commands = [
            {"name": f':tools: Single Operation :tools: ',
             "value": f'`{self.command_string}operations operation <operation id>`'},
            {"name": f' :ledger: Operation by Ledger :ledger: ',
             "value": f'`{self.command_string}operations ledger <ledger id>`'},
            {"name": f' :map: Operation by Account :map: ',
             "value": f'`{self.command_string}operations account <Account public address>`'},
            {"name": f' :hash: Operations for transaction :hash:',
             "value": f'`{self.command_string}operations transaction <transaction hash>`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def orderbook(self, ctx):
        title = ':office_worker: __Horizon Assets Operations__ :office_worker:'
        description = 'Representation of all available commands available to interact with ***Assets*** Endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f'',
             "value": f''},
            {"name": f'',
             "value": f'`{self.command_string}horizon account create`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def paths(self, ctx):
        title = ':office_worker: __Horizon Assets Operations__ :office_worker:'
        description = 'Representation of all available commands available to interact with ***Assets*** Endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f'',
             "value": f''},
            {"name": f'',
             "value": f'`{self.command_string}horizon account create`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def tradeaggregation(self, ctx):
        title = ':office_worker: __Horizon Assets Operations__ :office_worker:'
        description = 'Representation of all available commands available to interact with ***Assets*** Endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f'',
             "value": f''},
            {"name": f'',
             "value": f'`{self.command_string}horizon account create`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def trades(self, ctx):
        title = ':currency_exchange:  __Horizon Trades Queries__ :currency_exchange:   '
        description = 'Representation of all available commands available to interact with ***Trades*** Endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f':map: Trades for Account :map:',
             "value": f'`{self.command_string}trades account <address>`'},
            {"name": f':id: Trades by Offer ID :id:  ',
             "value": f'`{self.command_string}trades offer <offer id>`'}
        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.group()
    async def transactions(self, ctx):
        title = ':incoming_envelope: __Horizon Transactions __ :incoming_envelope:'
        description = 'Representation of all available commands available to interact with ***Transactions*** Endpoint on ' \
                      'Stellar Horizon Server'
        list_of_commands = [
            {"name": f':hash: Query by transaction Hash :hash: ',
             "value": f'`{self.command_string}transactions single <Transaction Hash>`'},
            {"name": f':map:  Query by account address :map:  ',
             "value": f'`{self.command_string}transactions account <Valid Stellar Address>`'},
            {"name": f':ledger:  Query by ledger :ledger:',
             "value": f'`{self.command_string}transactions ledger <Ledger Number>`'},

        ]

        if ctx.invoked_subcommand is None:
            await custom_messages.embed_builder(ctx=ctx, title=title, data=list_of_commands,
                                                description=description,
                                                destination=1, c=Colour.lighter_gray())

    @horizon.error
    async def asset_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            message = f'In order to user Stellar Expert Commands you need to have wallet registered in the system!. Use' \
                      f' `{self.command_string}register`'
            await custom_messages.system_message(ctx=ctx, color_code=1, message=message, destination=0,
                                                 sys_msg_title=CONST_ACCOUNT_ERROR)


def setup(bot):
    bot.add_cog(HorizonAccessCommands(bot))
