"""
Button loader module for sponsor ticket UI components.

This module defines a loader class responsible for registering and
unregistering interactive button components related to sponsor tickets.
"""

from bot.core.sponsor_tickets import (
    on_become_a_sponsor,
    on_claim_sponsor_role,
    on_submit_enquiry,
)
from bot.ui.buttons.buttons_manager import ButtonsManager
from bot.ui.buttons.sponsor_tickets.main_menu import (
    become_a_sponsor_btn,
    claim_sponsor_role_btn,
    submit_enquiry_btn,
)


class SponsorTicketsButtonLoader:
    """
    Loader for sponsor ticket-related button components.

    Registers and unregisters all button views and their associated
    interaction handlers for sponsor-related actions.
    """

    @staticmethod
    def load_buttons():
        """
        Register all button callbacks/views.
        """
        # register callbacks
        ButtonsManager.register_callback(become_a_sponsor_btn["custom_id"], on_become_a_sponsor)
        ButtonsManager.register_callback(submit_enquiry_btn["custom_id"], on_submit_enquiry)
        ButtonsManager.register_callback(claim_sponsor_role_btn["custom_id"], on_claim_sponsor_role)

        # register view
        ButtonsManager.register_view(
            [
                become_a_sponsor_btn,
                submit_enquiry_btn,
                claim_sponsor_role_btn,
            ]
        )

    @staticmethod
    def unload_buttons():
        """
        Unregister all button callbacks/views.
        """
        # unregister callbacks
        ButtonsManager.unregister_callback(become_a_sponsor_btn["custom_id"])
        ButtonsManager.unregister_callback(submit_enquiry_btn["custom_id"])
        ButtonsManager.unregister_callback(claim_sponsor_role_btn["custom_id"])
