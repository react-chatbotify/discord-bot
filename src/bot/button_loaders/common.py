"""
Button loader module for common button components.

This module defines a loader class responsible for registering and
unregistering interactive common button components used across the bot.
"""

from bot.core.common import (
    on_cancel_close_ticket,
    on_close_ticket,
    on_confirm_close_ticket,
    on_export_ticket,
)
from bot.ui.buttons.buttons_manager import ButtonsManager
from bot.ui.buttons.common.cancel_close_ticket import cancel_close_ticket_btn
from bot.ui.buttons.common.close_ticket import close_ticket_btn
from bot.ui.buttons.common.confirm_close_ticket import confirm_close_ticket_btn
from bot.ui.buttons.common.export_ticket import export_ticket_btn


class CommonButtonLoader:
    """
    Loader for common button components.

    Registers and unregisters all common button views and their associated
    interaction handlers.
    """

    @staticmethod
    def load_buttons():
        """
        Register all button callbacks/views.
        """
        # register callbacks
        ButtonsManager.register_callback(confirm_close_ticket_btn["custom_id"], on_confirm_close_ticket)
        ButtonsManager.register_callback(cancel_close_ticket_btn["custom_id"], on_cancel_close_ticket)
        ButtonsManager.register_callback(close_ticket_btn["custom_id"], on_close_ticket)
        ButtonsManager.register_callback(export_ticket_btn["custom_id"], on_export_ticket)

        # register view
        ButtonsManager.register_view([confirm_close_ticket_btn, cancel_close_ticket_btn])

    @staticmethod
    def unload_buttons():
        """
        Unregister all button callbacks/views.
        """
        # unregister callbacks
        ButtonsManager.unregister_callback(confirm_close_ticket_btn["custom_id"])
        ButtonsManager.unregister_callback(cancel_close_ticket_btn["custom_id"])
        ButtonsManager.unregister_callback(close_ticket_btn["custom_id"])
        ButtonsManager.unregister_callback(export_ticket_btn["custom_id"])
