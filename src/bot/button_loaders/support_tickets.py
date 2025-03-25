"""
Button loader module for support ticket UI components.

This module defines a loader class responsible for registering and
unregistering interactive button components related to support tickets.
"""

from bot.core.support_tickets import on_create_ticket
from bot.ui.buttons.buttons_manager import ButtonsManager
from bot.ui.buttons.support_tickets.main_menu import create_ticket_btn


class SupportTicketsButtonLoader:
    """
    Loader for support ticket-related button components.

    Registers and unregisters all button views and their associated
    interaction handlers for support-related actions.
    """

    @staticmethod
    def load_buttons():
        """
        Register all button callbacks/views.
        """
        # register callbacks
        ButtonsManager.register_callback(create_ticket_btn["custom_id"], on_create_ticket)

        # register view
        ButtonsManager.register_view(
            [
                create_ticket_btn,
            ]
        )

    @staticmethod
    def unload_buttons():
        """
        Unregister all button callbacks/views.
        """
        # unregister callbacks
        ButtonsManager.unregister_callback(create_ticket_btn["custom_id"])
