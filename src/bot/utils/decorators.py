"""
Command decorators for access control based on user roles.

Includes decorators to restrict command usage to admin users or
recurring sponsors. Displays appropriate error messages if access is
denied.
"""

from discord.ext import commands

from bot.services.role_checker_svc import is_admin_user, is_recurring_sponsor_user


def admin_only():
    """
    Restrict a command to admin users only.

    This decorator checks if the command invoker has the admin role
    as defined in the bot's common configuration. If not, it sends an
    ephemeral error message.

    Returns:
        Callable: A command check that returns True if the user is an admin.

    """

    async def predicate(ctx: commands.Context) -> bool:
        member = ctx.author
        if is_admin_user(member):
            return True

        await ctx.send("🚫 You must be an admin to use this command.", ephemeral=True)
        return False

    return commands.check(predicate)


def recurring_sponsor_only():
    """
    Restrict a command to recurring sponsor users only.

    This decorator checks if the command invoker has any of the recurring
    sponsor roles as configured in the bot. If not, it sends an
    ephemeral error message.

    Returns:
        Callable: A command check that returns True if the user is a recurring sponsor.

    """

    async def predicate(ctx: commands.Context) -> bool:
        member = ctx.author
        if is_recurring_sponsor_user(member):
            return True

        await ctx.send("🚫 You must be a sponsor to use this command.", ephemeral=True)
        return False

    return commands.check(predicate)


# todo: add a decorator to identify one-time-sponsors only (community sponsor)
