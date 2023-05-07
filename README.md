# Python Django Rest Framework RpgManager API Project

### A fully functional Django RestFramework API for RpgManager, a self management app that combines game and organization.

<p>This project is my attempt to create self managing app that would all of the functions in one place and combine them with gaming like experience. </p>
<p>It is aimed to be as close to real-world large scale application as possible. I used style of test driven development to write this project.</p>

## The goal

<p>The goal of this manager is to be able to organize yourself using 4 main components such as:</p>

-   Tasks
-   Lists
-   Routines
-   Notes

<p>While combining it with gaming like features such as: </p>

-   Character
-   Level
-   Rewards for completion of tasks, ect.
-   Skills
-   Coins
-   Reward items

To create most comfortable and rewarding experience in managing your life.

## Technical details

<p>This project is made using Django 4 and Django Rest Framework 3. It is designed to work with PostgreSQL using psycopg2 but in theory this project is database agnostic.</p>

<p>Docker was used to make this project...</p>

<p>The Django project is divided into 5 apps: </p>

1. Core - which handles things specific to this project.
2. Manager - it has app has everything that has to do with managing, such as: Tasks, Routines, Lists, etc.
3. RPG - this app handles all game-like elements in the system.
4. Social - it handles things like user profile, and interactions between users.
5. User - that handles authentication.

<p>The database schema for this project is: </p>

![alt text](https://i.imgur.com/0Jf1ch7.png)

## How to install this project

1. Clone this project
2. Install docker desktop
3. Run `docker-compose up` and all dependencies will be automatically installed.

## Known issues

-   When trying to add tag with name that already exists for given user database will throw an error because of 'unique_together' constraint. Server will return 500 error instead of 4\*\*. I don't know how to solve this without breaking other things.
