<p align="center">
  <img width="200px" src="https://raw.githubusercontent.com/react-chatbotify/discord-bot/main/assets/logo.png" />
  <h1 align="center">React ChatBotify Discord Bot Developer Guide</h1>
</p>

## Table of Contents
* [Introduction](#introduction)
* [Navigating this Developer Guide](#navigating-this-developer-guide)
* [Setup](#setup)
* [Project Structure](#project-structure)
* [Design](#design)
* [Code Documentation](#code-documentation)
* [Testing](#testing)
* [Pull Requests](#pull-requests)
* [Final Notes](#final-notes)

<div style="page-break-after: always;"></div>

## Introduction

For an introduction to the discord bot itself, please refer to the project [*README*](https://github.com/react-chatbotify/discord-bot/blob/main/README.md). This developer guide assumes its readers to have at least a **basic understanding** of [discord.py](https://discordpy.readthedocs.io/), [Python](https://www.python.org/) and [Docker](https://www.docker.com/). Otherwise, it is highly recommended for readers to refer to proper tutorial contents for the basics of discordpy and Python prior to working on the project. It is also worth noting that a major aspect of this guide is to cover **important design considerations** for the project. The designs are not perfect and you are encouraged to **think and explore possible improvements**.

This guide **will not** dive into every single project detail because that is not sustainable in the long run. For simpler implementations that are not covered in this guide, you will find the code comments in the files themselves to be useful.

## Navigating this Developer Guide

Before diving into the rest of the contents in our developer guide, the following are a few important syntaxes to take note of to facilitate your reading:

| Syntax              | Description                                    |
| ------------------- | ---------------------------------------------- |
| `Markdown`          | Commands (e.g. `pip install`)                  |
| *Italics*           | Files/Folders (e.g. *core*, *ui*)  |
| **Bold**            | Keywords (e.g. **important consideration**)    |

<div  style="page-break-after: always;"></div>

## Setup

Setting up the project is relatively simple. Before you begin, ensure that you have **at least Python 3.10 and Docker** installed.
1) Fork the [project repository](https://github.com/react-chatbotify/discord-bot).
2) Clone the **forked project** into your desired directory with:
    ```
    git clone the-forked-project.git
    ```
3) Next, `cd` into the project and install dependencies with:
    ```
    pip install -r requirements.txt -r requirements-dev.txt
    ```
4) Once installations are complete, you may launch the project with:
    ```
    hatch run start
    ```

Go ahead and start making code changes to the project (hot module reloading is enabled). You may also find instructions for [**testing**](https://github.com/react-chatbotify/discord-bot/blob/main/docs/DeveloperGuide.md#testing) and [**opening pull requests**](https://github.com/react-chatbotify/discord-bot/blob/main/docs/DeveloperGuide.md#pull-requests) relevant if you're looking to contribute back to the project!

## Project Structure

### Overview

At a high-level overview, the entire project can be (broadly speaking) broken down into **9 different sections**, which are as follows:

- *button_loaders*
- *cogs*
- *config*
- *core*
- *database*
- *models*
- *services*
- *ui*
- *utils*

Each section and its relevant files are seated in its own folder, so it's relatively straightforward when looking at the project structure. Below, we will take a deeper look at the details for individual sections.

### Button Loaders

The *button_loaders* folder contains logic for dynamically registering and managing buttons used in Discord interactions. Each button is defined with its unique `custom_id` and callback function. These buttons are used across various features of the bot, such as ticket management and game interactions.

### Cogs

The *cogs* folder contains the main modules of the bot, organized into modular components. Each cog represents a specific feature or functionality, such as **Auto Voice**, **Games**, or **Support Tickets**. These cogs are loaded dynamically by the bot during initialization, allowing for easy enablement or disablement of features.

### Config

The *config* folder contains configuration files and settings for the bot. These include settings for features like **Auto Voice**, **Games**, and **Tickets**, as well as database connection details. Each configuration file is modularized to keep settings for different features separate and manageable.

### Core

The *core* folder contains the foundational logic for the bot's features. This includes the main implementations for **Auto Voice**, **Games**, **Logging**, and ticket management. These files define the core behavior of the bot and are used by the cogs to execute specific functionalities.

### Database

The *database* folder contains database models and utilities for interacting with the MySQL database. It includes models like `TicketCounter` and database initialization logic. This folder is essential for managing persistent data such as ticket numbers.

### Models

The *models* folder contains data models used throughout the bot. These models define the structure of objects like `BotButton` and `SponsorTier`, which are used to represent buttons and sponsorship tiers, respectively. These models help standardize data handling across the bot.

### Services

The *services* folder contains utility functions and logic for interacting with external systems or performing specific tasks. For example, it includes services for managing Discord roles, exporting channel contents, and checking user information. These services are reusable and abstract away complex logic from the main bot code.

### UI

The *ui* folder contains components for building user interfaces within Discord. This includes embeds, buttons, and views used in interactions. The folder is further organized into subfolders like `buttons` and `embeds`, which group related components together for better maintainability.

### Utils

The *utils* folder contains miscellaneous utility functions that are used across the bot but do not belong to any specific feature. For example, it includes logging utilities and helper functions for formatting data. This folder acts as a shared library for small, reusable pieces of logic.

## Design

### Overview

The bot's design is centered around modularity, scalability, and maintainability. Key design elements include a cog-based architecture, dynamic interaction handling, and a service layer abstraction. These designs ensure the bot is easy to extend, debug, and maintain. Below are a few critical designs elaborated for better understanding.

### Key Designs

#### 1. Cog-Based Modular Architecture

The bot uses a cog-based architecture to organize its features. Each cog encapsulates a specific functionality (e.g., Auto Voice, Games, Support Tickets) and is dynamically loaded at runtime. This design provides:

- **Modularity**: Features are self-contained and can be added or removed independently.
- **Scalability**: New features can be implemented as separate cogs without affecting existing ones.
- **Ease of Maintenance**: Debugging and updates are straightforward due to the separation of concerns.

#### 2. Dynamic Button and Interaction Management

The bot dynamically registers and manages buttons and interactions using unique `custom_id` values. This is implemented in the `button_loaders` and `ui` folders. Key benefits include:

- **Reusability**: Buttons and interactions can be reused across multiple features.
- **Flexibility**: Interaction callbacks are registered at runtime, allowing for dynamic behavior.
- **Consistency**: Centralized management ensures uniform behavior across the bot.

#### 3. Service Layer Abstraction

The `services` folder abstracts complex logic into reusable service functions. For example, the `discord_svc.py` file handles channel creation, permission management, and content export. This abstraction provides:

- **Separation of Concerns**: Core logic is decoupled from feature-specific code.
- **Reusability**: Services can be shared across multiple features, reducing code duplication.
- **Maintainability**: Changes to core logic are centralized, making updates easier.

#### 4. Embed-Driven UI Design

The bot's user interface is built using Discord embeds, defined in the `ui/embeds` folder. Embeds are used to display information and provide interactive elements like buttons. This design ensures:

- **Consistency**: A uniform look and feel across all bot interactions.
- **Customizability**: Embeds are tailored to specific use cases, such as ticket management or game interactions.
- **User Engagement**: Interactive elements like buttons enhance the user experience.

## Code Documentation

Code documentation is **strongly encouraged** to ensure that the codebase is kept easily maintainable. As a rule of thumb, **all files** should have a description of what it does at the top.

Comments should also be written for **all functions** and all its relevant arguments should be documented. In general, the following structure is adopted for writing comments:

```
def is_admin_user(member: discord.Member) -> bool:
    """
    Check if a user has the admin role.

    Args:
        member (discord.Member): The member to check.

    Returns:
        bool: True if the user has the admin role, False otherwise.

    """
    # implementation
```

The above shows an example of a function checking if a user is an admin. Note that it begins with a brief description of what the function does followed by highlighting its parameter and what it is used for.

Finally, any leftover tasks or areas in the code to be revisited should be flagged with a **todo comment** like the one below:

```
# todo: tj to optimize the calculation code here
```

That way, we can identify what are the tasks to finish up here and optionally, state who will be responsible for it.

## Testing

To be updated

## Pull Requests

If you are satisfied with your changes and would like to **contribute back to the project** (which we strongly encourage you to!), feel free to open a pull request to the master branch.

A pull request template has been setup to assist you in the process. Note that if your pull request involves **significant changes** (e.g. new feature), you should [**reach out and discuss with the team**](https://discord.gg/6R4DK4G5Zh) beforehand.

## Final Notes

The designs in this project are not perfect. We encourage experienced developers to help seek out areas for **improvements** in the application! We value your input and welcome contributions to enhance the chatbot. Happy coding!
