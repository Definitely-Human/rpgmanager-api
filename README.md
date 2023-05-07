# Python Django Rest Framework RpgManager API Project

This is a fully functional Django RestFramework API for RpgManager, a self-management app that combines game and organization. The purpose of this project is to create a single application that combines self-management tools with gaming-like features to provide a comfortable and rewarding experience in managing your life.

## Table of Contents

-   [The Goal](#the-goal)
-   [Technical Details](#technical-details)
-   [Installation](#installation)
-   [Known Issues](#known-issues)
-   [Contributing](#contributing)

## The Goal

The goal of this manager is to organize yourself using four main components:

-   Tasks
-   Lists
-   Routines
-   Notes

While combining it with gaming-like features such as:

-   Character
-   Level
-   Rewards for completion of tasks, etc.
-   Skills
-   Coins
-   Reward items

## Technical Details

This project is made using Django 4 and Django Rest Framework 3. It is designed to work with PostgreSQL using psycopg2, but in theory, this project is database agnostic. Docker was used to make this project. The Django project is divided into five apps:

1. Core - which handles things specific to this project.
2. Manager - it is an app that has everything to do with managing, such as: Tasks, Routines, Lists, etc.
3. RPG - this app handles all game-like elements in the system.
4. Social - it handles things like user profile and interactions between users.
5. User - that handles authentication.

The database schema for this project is:

![alt text](https://i.imgur.com/0Jf1ch7.png)

## Installation

1. Clone this project.
2. Install Docker Desktop.
3. Run `docker-compose up`, and all dependencies will be automatically installed.

## Known Issues

-   When trying to add a tag with a name that already exists for a given user, the database will throw an error because of the 'unique_together' constraint. The server will return a 500 error instead of 4\*\*. I don't know how to solve this without breaking other things.

## Contributing

If you know how to fix a bug or have a cool or useful feature to add, feel free to clone this repository and submit a pull request.
