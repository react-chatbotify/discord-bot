"""
DatabaseConfig module for managing MySQL connection settings.

This module defines the database configuration used by the bot to
connect to a MySQL server. It uses Pydantic for loading and validating
environment- based or default settings including credentials, host, and
database name.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """
    Database configuration settings for MySQL.

    These settings define the credentials and connection details used by
    the bot to interact with the MySQL database.

    Attributes:
        mysql_host (str): The hostname or IP address of the MySQL server.
        mysql_port (int): The port number to connect to on the MySQL server.
        mysql_user (str): The username used to authenticate with the MySQL server.
        mysql_password (str): The password for the MySQL user.
        mysql_database (str): The name of the database to use.
        autocommit (bool): Whether to enable autocommit on MySQL connections.

    """

    mysql_host: str = Field(
        default="mysql",
        description="The hostname or IP address of the MySQL server.",
    )
    mysql_port: int = Field(
        default=3306,
        description="The port number used for the MySQL connection.",
    )
    mysql_user: str = Field(
        default="discord_bot",
        description="The username for the MySQL connection.",
    )
    mysql_password: str = Field(
        default="password",
        description="The password for the MySQL user.",
    )
    mysql_database: str = Field(
        default="discord_bot",
        description="The name of the MySQL database to use.",
    )
    autocommit: bool = Field(
        default=True,
        description="Whether MySQL connections should autocommit transactions.",
    )


database_config = DatabaseConfig()
