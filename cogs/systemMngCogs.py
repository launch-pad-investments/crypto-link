"""
COGS: Management of the whole payment system
"""
import os
import sys
from datetime import datetime

from discord import Embed, Colour
from discord.ext import commands
from git import Repo, InvalidGitRepositoryError

from backOffice.profileRegistrations import AccountManager
from cogs.utils.systemMessaages import CustomMessages
from utils.tools import Helpers

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

helper = Helpers()
account_manager = AccountManager()
customMessages = CustomMessages()
d = helper.read_json_file(file_name='botSetup.json')
auto_channels = helper.read_json_file(file_name='autoMessagingChannels.json')


def is_animus(ctx):
    return ctx.message.author.id == d['creator']


def is_one_of_gods(ctx):
    list_of_gods = [d['ownerId'], d['creator']]
    return [god for god in list_of_gods if god == ctx.message.author.id]


class BotManagementCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.check(is_one_of_gods)
    async def god(self, ctx):
        """
        Category of commands under team category
        :param ctx:
        :return:
        """

        try:
            await ctx.message.delete()
        except Exception:
            pass

        if ctx.invoked_subcommand is None:
            value = [{'name': 'Change properties of bot setup file',
                      'value': f"High level backend administration commands which can be accessed through\n"
                               f" ***{d['command']}god change*** "},
                     {'name': 'Role Management ',
                      'value': f"Commands dedicated to management of the roles. all available sub-commands "
                               f"are described through\n"
                               f" ***{d['command']}god role*** "}
                     ]
            await customMessages.embed_builder(ctx, title='Welcome to the GOD mode',
                                               description=f"Showcase of all commands and sub-commands available for server owner, "
                                                           f" and bot creator. In order to get access to the categories "
                                                           f"***{d['command']}god*** needs to be typed in first followed by relevant sub-commands",
                                               data=value)

    @god.group()
    @commands.check(is_animus)
    async def system(self, ctx):
        if ctx.invoked_subcommand is None:
            value = [{'name': '__Turning bot off__',
                      'value': f"***{d['command']}god system off*** "},
                     {'name': '__Pulling update from Github__',
                      'value': f"***{d['command']}god system update*** "},
                     ]

            await customMessages.embed_builder(ctx, title='Available sub commands for system',
                                               description='Available commands under category ***system***', data=value)

    @system.command()
    async def off(self, ctx):
        await ctx.channel.send(content='Going Offline!')
        await self.bot.close()
        sys.exit(0)

    @system.command()
    async def update(self, ctx):
        extensions = ['cogs.generalCogs', 'cogs.transactionCogs', 'cogs.userAccountCogs',
                      'cogs.systemMngCogs', 'cogs.hotWalletsCogs', 'cogs.botMainCogs', 'cogs.withdrawalCogs',
                      'cogs.merchantCogs', 'cogs.consumerMerchant', 'cogs.autoMessagesCogs',
                      'cogs.merchantLicensingCogs',
                      'cogs.feeManagementCogs']
        notification_str = ''
        channel_id = auto_channels['sys']
        channel = self.bot.get_channel(id=int(channel_id))
        current_time = datetime.utcnow()
        try:
            repo = Repo()  # Initiate repo
            git = repo.git
            git.pull()
            notification_str += 'GIT UPDATE STATUS\n' \
                                ' Latest commits pulled :green_circle: \n' \
                                '=============================================\n'
        except InvalidGitRepositoryError:
            notification_str += f'GIT UPDATE: There has been an error while pulling latest commits :red_circle:  \n' \
                                f'Error: Git Repository could not be found\n' \
                                f'=============================================\n'
            await channel.send(content=notification_str)

        notification_str += 'STATUS OF COGS AFTER RELOAD\n'
        for extension in extensions:
            print(f'Trying to load extension {extension}')
            try:
                self.bot.unload_extension(f'{extension}')
                self.bot.load_extension(f'{extension}')
                notification_str += f'{extension} :green_circle:  \n'
                print('success')
                print('=========')
            except Exception as e:
                notification_str += f'{extension} :red_circle:' \
                                    f'Error: {e} \n'
                print('failed')
                print('=========')
        notification_str += 'GIT UPDATE STATUS\n' \
                            ' Latest commits pulled :green_circle: \n' \
                            '=============================================\n'
        load_status = Embed(title='System update message',
                            description='Status after git update',
                            colour=Colour.green())
        load_status.add_field(name='Time of execution',
                              value=f'{current_time}',
                              inline=False)
        load_status.add_field(name='Status Message',
                              value=notification_str,
                              inline=False)
        await channel.send(embed=load_status)

    # TODO finish COG manipulation commands
    @system.command()
    async def load_cog(self, ctx, cog_name: str):
        pass

    @system.command()
    async def unload_cog(self, ctx, cog_name: str):
        pass

    @system.command()
    async def list_cogs(self, ctx):
        pass

    @system.command()
    async def reload(self, ctx):
        pass


def setup(bot):
    bot.add_cog(BotManagementCommands(bot))
