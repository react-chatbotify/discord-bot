"""
Button loader module for report ticket UI components.

This module defines a loader class responsible for registering and
unregistering interactive button components related to report tickets.
"""

from bot.core.report_tickets import on_report_plugin, on_report_theme
from bot.ui.buttons.buttons_manager import ButtonsManager
from bot.ui.buttons.report_tickets.main_menu import report_plugin_btn, report_theme_btn


class ReportTicketsButtonLoader:
    """
    Loader for report ticket-related button components.

    Registers and unregisters all button views and their associated
    interaction handlers for report-related actions.
    """

    def load_buttons():
        """
        Register all button callbacks/views.
        """
        # register callbacks
        ButtonsManager.register_callback(report_theme_btn["custom_id"], on_report_theme)
        ButtonsManager.register_callback(report_plugin_btn["custom_id"], on_report_plugin)

        # register view
        ButtonsManager.register_view(
            [
                report_theme_btn,
                report_plugin_btn,
            ]
        )

    def unload_buttons():
        """
        Unregister all button callbacks/views.
        """
        # unregister callbacks
        ButtonsManager.unregister_callback(report_theme_btn["custom_id"])
        ButtonsManager.unregister_callback(report_plugin_btn["custom_id"])
