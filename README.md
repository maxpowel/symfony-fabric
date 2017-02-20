# symfony-fabric
I have many symfony installations in severals servers. With this fabric file I can manage the most common taks easily and fast!

Commands
=======

pull
----
git pull the project

install
-------
composer install

assets
------
assets:install

install_composer
----------------
install composer, used by install command automatically when composer does not exist.

db_prepare(database, user, password)
-----------------------------------
create database, user and grant permissions

cc
--
clear cache

su
--
doctrine schema update

permissions
-----------
fix cache and logs permissions

console(command, args)
----------------------
generic symfony console command

create_user(username, email, password, admin)
--------------
create an user
