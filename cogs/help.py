"""
COGS: Help commands for the payment services
"""
import discord
from discord.ext import commands
from discord import Colour
from utils.tools import Helpers
from cogs.utils.customCogChecks import is_owner, is_public
from cogs.utils.systemMessaages import CustomMessages

custom_messages = CustomMessages()

CONST_STELLAR_EMOJI = '<:stelaremoji:684676687425961994>'


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.helper = Helpers()
        self.command_string = bot.get_command_str()

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            title = '__Available help categories__'
            description = "All available help sub-categories for you to familiarize yourself with payment " \
                          "and merchant " \
                          "services available."
            list_of_values = [
                {"name": "How to get started", "value": f"{self.command_string}help get_started"},
                {"name": "About the payment solution", "value": f"{self.command_string} about"},
                {"name": "Account commands", "value": f"{self.command_string}help account"},
                {"name": "How to make peer to peer transactions", "value": f"{self.command_string}help transactions"},
                {"name": "List of available currencies", "value": f"{self.command_string}help currencies"},
                {"name": "List of commands if you are community owner", "value": f"{self.command_string}help owner"},
                {"name": "Explanation on the Merchant System", "value": f"{self.command_string}help owner merchant"}
            ]

            await custom_messages.embed_builder(ctx=ctx, title=title, description=description, data=list_of_values,
                                                destination=1, c=Colour.blue())

    @commands.command()
    async def about(self, ctx):
        """
        Command which returns information on About the system
        :param ctx:
        :return:
        """
        title = ':mega: __About the system__ :mega: '
        description = "Description about the system"
        list_of_values = [
            {"name": ":information_source: About :information_source: ",
             "value": 'Crypto Link is a Discord multi functional bot. Built on top of Stellar, utilizing '
                      'its native Stellar Lumen (XLM) crypto currency and tokens issued on Stellar chain,'
                      ' allows for execution of peer-to-peer crypto transactions, token ICOs/project'
                      ' promotions, and Discord community monetization opportunities.'},

            {"name": ":money_with_wings:  Peer to Peer transactions :money_with_wings:  ",
             "value": f"Users are able to execute instant peer-2-peer transactions either with the Stellar"
                      f" native currency or its tokens which have been integrated onto Crypto Link. For full"
                      f" list of supported currencies please use command {self.command_string}currencies"},

            {"name": ":convenience_store: Merchant system :convenience_store: ",
             "value": f"If you are a Discord Guild owner you can monetize your roles with various lengths and "
                      f"values. So far system support only XLM as a currency to be used in merchant system. "
                      f"For more information execute command {self.command_string}help owner "},

            {"name": ":postal_horn: ICO's and Project promotions :postal_horn: ",
             "value": f"Would you like to have another project sourcing stream? Crypto Link supports all"
                      f" tokens issued on Stellar. This as well provides perfect opportunity to run ICO"
                      f" with minimal costs, or as additional channel to get a hold of potential customers. "
                      f"Contact us by sending an email to cryptolinkpayments@gmail.com or one of the members"
                      f" with the role Crypto Link Staff on Discord Community."},

            {"name": ":placard: Further information and links:placard: ",
             "value": f'[Homepage](https://cryptolink.carrd.co/) \n'
                      f'[Github](https://github.com/launch-pad-investments/crypto-link) \n'
                      f'[Twitter](https://twitter.com/CryptoLink8)'},
        ]

        await custom_messages.embed_builder(ctx=ctx, title=title, description=description, data=list_of_values,
                                            destination=1, c=Colour.blue())

    @help.command()
    async def get_started(self, ctx):
        """
        How to get started with the payment system
        :param ctx: Discord Context
        :return: Discord Embed
        """
        start_embed = discord.Embed(title=f':rocket: Launch {self.bot.user.name} Experience :rocket:',
                                    colour=Colour.blue())
        start_embed.add_field(name=':one: Register your account :one:',
                              value=f'In order for you to be able to make peer to peer transactions and use merchant'
                                    f' system, you must be registered in the system.\n'
                                    f'You can do that by executing command on any public Discord channel, where system'
                                    f' is present with command `{self.command_string}register`.\n'
                                    f'Once successful, you will create personal wallets with details which you can use '
                                    f' to move or deposit funds. To further familiarize yourself with other'
                                    f' commands use __{self.command_string}help__ ',
                              inline=False)
        start_embed.add_field(name=':two: Get Deposit Details :two:',
                              value=f'Get deposit details of your Discord wallet with `{self.command_string}wallet'
                                    f' deposit` and deposit XLM.',
                              inline=False)
        start_embed.add_field(name=':three: Make P-2-P Transaction :three:',
                              value=f'`{self.command_string}send <amount> <ticker> <@discord.Member>`\n'
                                    f'Example: `{self.command_string}send 10 xlm @animus`',
                              inline=False)
        start_embed.add_field(name=':sos: Access Help Menu :sos: ',
                              value=f'`{self.command_string}help` or check '
                                    f'[user command list on Github](https://github.com/launch-pad-investments/crypto-link/blob/master/docs/USERCOMMANDS.md)',
                              inline=False)
        await ctx.author.send(embed=start_embed)

    @help.command(aliases=['tokens', 'coins'])
    async def currencies(self, ctx):
        """
        Returns representation of all available currencies available to be utilized int transactions
        :return: Discord Embed
        """

        available = discord.Embed(title=':coin: Integrated coins and tokens :coin: ',
                                  description='Bellow is a list of all available currencies for making peer 2 peer'
                                              ' transactions or to be used with merchant system',
                                  colour=Colour.blue())
        await ctx.author.send(embed=available)

        coins = self.helper.read_json_file(file_name='integratedCoins.json')
        for coin in coins:
            available.add_field(name=f'====================================',
                                value='\u200b')
            available.add_field(
                name=f"{coins[coin]['emoji']} {coins[coin]['name']} {coins[coin]['emoji']}",
                value=f'`Symbol:` ***{coins[coin]["ticker"]}***\n'
                      f'`Issuer:` ***{coins[coin]["assetIssuer"]}***\n'
                      f'`Decimals:` ***{coins[coin]["decimal"]}***\n'
                      f'`Min. Withdrawal:` ***{coins[coin]["minimumWithdrawal"] / 10000000}***\n'
                      f'`Expert Link:` ***{coins[coin]["expert"]}***\n'
                      f'`Homepage:` ***{coins[coin]["homepage"]}***',
                inline=False)
        await ctx.author.send(embed=available)

    @help.command(aliases=['tx', 'pay'])
    async def transactions(self, ctx):
        title = ':money_with_wings: __How to make peer to peer transaction__ :money_with_wings: '
        description = f"Forms of transactions available on {self.bot.user.name}"
        list_of_values = [
            {"name": f":cowboy: Public P-2-P transactions :cowboy:",
             "value": f"{self.command_string}send <amount> <ticker> <Discord User> <message=optional>\n"
                      f"Example:`{self.command_string}send 10 xlm @animus Have a nice day`"},
            {"name": f":detective: Private transactions :detective:  ",
             "value": f"{self.command_string}private <amount> <ticker> <Discord User> <message=optional>\n"
                      f"Example: `{self.command_string}private 10 xlm @animus Dont tell anyone`"}
        ]

        await custom_messages.embed_builder(ctx=ctx, title=title, description=description, data=list_of_values,
                                            destination=1, c=Colour.blue())

    @help.command(aliases=['acc', 'user', 'profile'])
    async def account(self, ctx):
        title = ':office_worker: __Obtain information on personal account__:office_worker: '
        description = "Bellow are presented all currencies available for P2P transactions"
        list_of_values = [
            {"name": ":credit_card: Get balance information :credit_card: ",
             "value": f"{self.command_string}acc"},
            {"name": ":moneybag: Access wallet commands :moneybag: ",
             "value": f"{self.command_string}wallet"},
            {"name": " :woman_technologist: Get full account balance report :woman_technologist:  ",
             "value": f"{self.command_string}wallet balance"},
            {"name": ":bar_chart: Wallet Statistics :bar_chart:",
             "value": f"{self.command_string}wallet stats"},
            {"name": ":inbox_tray: Get instructions on how to deposit :inbox_tray:",
             "value": f"{self.command_string}wallet deposit"},
            {"name": ":outbox_tray: Withdrawal instructions :outbox_tray: ",
             "value": f"{self.command_string}withdraw"}]

        await custom_messages.embed_builder(ctx=ctx, title=title, description=description, data=list_of_values,
                                            destination=1, c=Colour.blue())

    @help.group()
    @commands.check(is_public)
    @commands.check(is_owner)
    async def owner(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':crown: __Available Commands for guild owners__ :crown: '
            description = "All available commands for you to familiarize yourself with payment and merchant " \
                          "services available as owner of the community."

            list_of_values = [
                {"name": f":bank: Guild wallet commands :bank:",
                 "value": f"{self.command_string}help owner corporate"},
                {"name": f":convenience_store: About Merchant and Setup :convenience_store:",
                 "value": f" {self.command_string}help owner merchant"},
                {"name": f":satellite_orbital: About Uplink and Setup :satellite_orbital:  ",
                 "value": f"{self.command_string}help owner uplink"}

            ]

            await custom_messages.embed_builder(ctx=ctx, title=title, description=description, data=list_of_values,
                                                destination=1, c=Colour.blue())

    @owner.command(aliases=['corp', 'business'])
    async def corporate(self, ctx):
        print('guild accessed')

    @owner.command(aliases=['store', 'monetize', 'merch'])
    async def merchant(self, ctx):
        """
        Entry point for merchant system
        """
        merchant_nfo = discord.Embed(title=':convenience_store: __Merchant System Commands__ :convenience_store: ',
                                     description='Basic explanation on what is merchant system.',
                                     colour=discord.Color.blue())
        merchant_nfo.add_field(name=':mega: About Merchant System:mega:',
                               value='Merchant is part of the Crypto Link eco system and provides owners of the '
                                     'community opportunity to, automize'
                                     ' and fully automate role system. Once monetized roles are created, '
                                     'Discord members can use available Crypto Link integrated currencies'
                                     ' to purchase roles in various durations and values (determined by community '
                                     'owner). System will than handle distribution on appropriate role'
                                     ', transfer of funds to corporate account, and as well remove it from the user '
                                     'once duration expires.',
                               inline=False)
        merchant_nfo.add_field(name=':scroll: Fees and licensing :scroll: ',
                               value='Activation and integration of merchant system is free of charge, however once '
                                     'owner wants to withdraw funds from merchant account'
                                     'to his own, a dynamic fee is applied. There is an option as well to obtain '
                                     'monthly license, and with it remove the transfer fees.',
                               inline=False)
        merchant_nfo.add_field(name=':rocket: Get Started with Merchant :rocket: ',
                               value=f":one: Register yourself {self.bot.user.name} account with "
                                     f"`{self.command_string}register`\n"
                                     f":two: Register your guild  into the {self.bot.user.name} system "
                                     f"with`{self.command_string}owner register`\n"
                                     f":three: Initiate the merchant with `{self.command_string}merchant_initiate`\n"
                                     f":four: Familiarize yourself with merchant system through command `{self.command_string}merchant`",
                               inline=False)
        merchant_nfo.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.author.send(embed=merchant_nfo, delete_after=500)

    @owner.command(aliases=['link', 'up_link'])
    async def uplink(self, ctx):
        """
        Entry point for merchant system
        """
        merchant_nfo = discord.Embed(title=':convenience_store: __Merchant System Commands__ :convenience_store: ',
                                     description='Basic explanation on what is merchant system.',
                                     colour=discord.Color.blue())
        merchant_nfo.add_field(name=':mega: About Merchant System:mega:',
                               value='Merchant is part of the Crypto Link eco system and provides owners of the '
                                     'community opportunity to, automize'
                                     ' and fully automate role system. Once monetized roles are created, '
                                     'Discord members can use available Crypto Link integrated currencies'
                                     ' to purchase roles in various durations and values (determined by community '
                                     'owner). System will than handle distribution on appropriate role'
                                     ', transfer of funds to corporate account, and as well remove it from the user '
                                     'once duration expires.',
                               inline=False)
        merchant_nfo.add_field(name=':scroll: Fees and licensing :scroll: ',
                               value='Activation and integration of merchant system is free of charge, however once '
                                     'owner wants to withdraw funds from merchant account'
                                     'to his own, a dynamic fee is applied. There is an option as well to obtain '
                                     'monthly license, and with it remove the transfer fees.',
                               inline=False)
        merchant_nfo.add_field(name=':rocket: Get Started with Merchant :rocket: ',
                               value=f":one: Register yourself {self.bot.user.name} account with "
                                     f"`{self.command_string}register`\n"
                                     f":two: Register your guild  into the {self.bot.user.name} system "
                                     f"with`{self.command_string}owner register`\n"
                                     f":three: Initiate the merchant with `{self.command_string}merchant_initiate`\n"
                                     f":four: Familiarize yourself with merchant system through command `{self.command_string}merchant`",
                               inline=False)
        merchant_nfo.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.author.send(embed=merchant_nfo, delete_after=500)

    @owner.error
    async def owner_error_assistance(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            message = f'You can access this are only if you are the owner of the guild and command is executed on ' \
                      f'public channel'
            await custom_messages.system_message(ctx=ctx, color_code=1, message=message, destination=0)


def setup(bot):
    bot.add_cog(HelpCommands(bot))
