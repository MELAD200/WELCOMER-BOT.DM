#!/usr/bin/env python3
"""
Discord Welcome Bot - Complete standalone version for Railway deployment
"""
import discord
from discord.ext import commands
import os
import logging
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Arabic welcome message template
WELCOME_MESSAGE = """**{member_mention} مرحبًا بك في السيرفر**
{server_name}
**نرحب بك في سيرفرنا ونتمنى لك تجربة مميزة**.

**يرجى التكرم بمراجعة القوانين لضمان التزام الجميع وحفاظًا على بيئة محترمة وآمنة**

▫️ https://discord.com/channels/1296070387209076848/1312824014347178004
▫️ https://discord.com/channels/1296070387209076848/1312824025059430460

**الالتزام بالقوانين يساهم في تعزيز جودة تجربتك داخل السيرفر.**

**السيرفر فيه نقل متاح لكل من يرغب، والفرصة متاحة للجميع**
▫️https://discord.com/channels/1296070387209076848/1377374964579041391
**تعالوا وشرفونا، وخلونا نبني مجتمع راقي وممتع مع بعض**

-# في حال وجود أي استفسار أو احتياج للمساعدة، لا تتردد في التواصل مع طاقم الإدارة، فنحن هنا لخدمتك

`هذا هو الـ IP للدخول المباشر إلى السيرفر`
cfx.re/join/m8mdxq"""

@bot.event
async def on_ready():
    """Called when bot is ready and connected to Discord"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} servers')
    
    # Set bot status
    try:
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for new members 👋"
            )
        )
        logger.info('Bot status set successfully')
    except Exception as e:
        logger.error(f'Error setting bot status: {e}')

@bot.event
async def on_member_join(member):
    """Called when a new member joins a server"""
    logger.info(f'New member joined: {member.name} in {member.guild.name}')
    
    # Don't send DM to bots
    if member.bot:
        logger.info(f'Skipping bot user: {member.name}')
        return
    
    # Format welcome message
    welcome_message = WELCOME_MESSAGE.format(
        member_mention=member.mention,
        server_name=member.guild.name
    )
    
    try:
        # Send DM to new member
        await member.send(welcome_message)
        logger.info(f'Successfully sent welcome DM to {member.name}')
    except discord.Forbidden:
        logger.warning(f'Could not send DM to {member.name} - DMs disabled')
    except Exception as e:
        logger.error(f'Error sending DM to {member.name}: {e}')

@bot.command(name='test_welcome')
@commands.has_permissions(administrator=True)
async def test_welcome(ctx):
    """Test command to preview welcome message (Admin only)"""
    welcome_message = WELCOME_MESSAGE.format(
        member_mention=ctx.author.mention,
        server_name=ctx.guild.name
    )
    
    embed = discord.Embed(
        title="🔍 Welcome Message Preview",
        description=welcome_message,
        color=discord.Color.green()
    )
    embed.set_footer(text="Welcome Bot Test", icon_url=bot.user.avatar.url if bot.user and bot.user.avatar else None)
    
    await ctx.send(embed=embed)
    logger.info(f'Test welcome command used by {ctx.author.name}')

@bot.command(name='bot_info')
async def bot_info(ctx):
    """Display bot information"""
    embed = discord.Embed(
        title="🤖 Welcome Bot Information",
        color=discord.Color.blue()
    )
    embed.add_field(name="Purpose", value="Sends Arabic welcome DMs to new members", inline=False)
    embed.add_field(name="Servers", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="Commands", value="`!test_welcome` - Preview message\n`!bot_info` - Bot information", inline=False)
    embed.set_footer(text="Welcome Bot", icon_url=bot.user.avatar.url if bot.user and bot.user.avatar else None)
    
    await ctx.send(embed=embed)
    logger.info(f'Bot info command used by {ctx.author.name}')

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ تحتاج لصلاحيات إدارية لاستخدام هذا الأمر")
    elif isinstance(error, commands.CommandNotFound):
        # Ignore command not found errors
        pass
    else:
        logger.error(f'Command error: {error}')
        await ctx.send("❌ حدث خطأ أثناء تنفيذ الأمر")

def main():
    """Main function to run the bot"""
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        logger.info('Environment variables loaded from .env file')
    except ImportError:
        logger.info('python-dotenv not available, using system environment variables')
    
    # Get bot token
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not bot_token:
        logger.error('DISCORD_BOT_TOKEN environment variable not set!')
        logger.error('Please set your Discord bot token in the environment variables.')
        return
    
    logger.info(f'Bot token found, length: {len(bot_token)}')
    
    try:
        # Run the bot
        logger.info('Starting Discord bot...')
        bot.run(bot_token)
    except discord.LoginFailure:
        logger.error('Invalid bot token! Please check your DISCORD_BOT_TOKEN.')
    except Exception as e:
        logger.error(f'Bot failed to start: {e}')
        import traceback
        logger.error(f'Traceback: {traceback.format_exc()}')

if __name__ == '__main__':
    main()