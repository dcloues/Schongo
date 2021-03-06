# Schongo Modular Bot #
Schongo is an IRC bot designed to be as modular as possible, with no single module being required for core functionality (Such as talking to the IRC Server itself) -- Note that at this time it is not completely meeting this goal (_tracking is hard-loaded by the core, and can not handle being unloaded), However Selig is working hard to make this happen.

Schongo is being written by:

- Selig Arkin
- Ross Delinger (Posiden)
- Wil Hall

# Plans for the future #
Please read the TODO file.

# Setup #
To setup Schongo: copy data/example.cfg to data/config.cfg
Then edit config.cfg with the irc network details

Then type this into terminal or cmdline:  
> python schongo.py

# Development #
Please take a look at the DEV\_README.md for information on development for the Schongo IRC Bot

# Basics #

## Commands ##
By default, Schongo uses the char '@' for commands, so that is the char that this document will use to describe commands
Commands are of the form
`@command arg1 arg2 ... argn` 
some commands may have sub-commands which take the form of 
`@command subcommand arg1 arg2 ... argn`

## Modules ##
You can load and unload modules at runtime with the commands
`@load module module module module` and `@unload module module module module`

# SO ( By Ross Delinger ) #
 Interface with the Stack Exchange API Current only supports stackoverflow others may follow

#### `@so <tag1> <tag2> <etc>` ####
Search through stackoverflow for the given tags

# choose #
Provides some random commands.

#### `@choose one or two or ... or n` ####
Picks from the given options - options are seperated by the string ' or '

#### `@8ball <life questions of great importance>` ####
Shakes the bot's built-in ( Free of charge! ) eight ball, and outputs the result

# cyphertools ( By Wil Hall ) #
Adds the cypher command for applying various cyphers to text.

#### `@cypher addcharset <setname> <set>` ####
Add a character set for future use. <set> should be like abcdefghijklmnopqrstuvwxyz Where each character will be interpreted respectively.

#### `@cypher view <setname>` ####
View a character set

#### `@cypher delcharset <set>` ####
Deletes the given char set

#### `@cypher replace <from> <to> <text>` ####
Replacement cypher

#### `@cypher shift <set> <num> <text>` ####
Shift Cypher

# dynamic ( By Selig Arkin ) #
Provides Dynamic commands to Schongo

Dynamic commands can use special syntax enhancements, such as %%Nick%% to refer to the person's nick, or %%Channel%% The syntax is as follows:

%%Variable%% - Replaced with the value of Variable
%[function name][function args]% - Dynamic function, such as random

== TODO ==
+ Implement the ability for other plugins to define functions and variables



#### `@add` ####
** No docstring given **

#### `@delete` ####
** No docstring given **

#### `@source` ####
** No docstring given **

#### `@say` ####
** No docstring given **

# geoip ( By Wil Hall ) #
Adds the 'geoip' command, which attempts to resolve a location for an IP or hostname.

#### `@geoip` ####
** No docstring given **

# netcmds ( By Ross Delinger ) #

Module that wraps around ping and traceroute. 
The new and improved system uses a new threading technique to handle unix commands


#### `@ping <host>` ####
This command runs the ping command via the command line and outputs the results into irc

#### `@traceroute <host>` ####
Run traceroute or tracrt depending on system. Gets the route and timing to an IP address or domain name

# probability ( By Wil Hall ) #
Adds the 'probability' command, which calculates the number of possible word and sentence permutations, depending on word length.

#### `@probability` ####
** No docstring given **

# quotes ( By Selig Arkin ) #
Allows the bot to store quotes of people

Adds the following commands: remember, quote

#### `@quote` ####
** No docstring given **

#### `@remember` ####
** No docstring given **

# remote #
Provides remote-control functionality to Schongo


#### `@ping` ####
** No docstring given **

#### `@say` ####
** No docstring given **

#### `@hello` ####
** No docstring given **

#### `@eval` ####
** No docstring given **

# secondlife ( By Ross Delinger ) #

Adds a interface with various SL APIs Name2Key and key2name are currently broken due to drama on the providers side
A new service will be developed when I feel like it


#### `@Name2Key <UUID>` ####
looks up the Secondlife UUID and returns a name

#### `@slstatus` ####
Retrieves the current status of the Second Life Grid

# shorten ( By Wil Hall, Selig Arkin ) #
Interfaces with shortening services, and expands shortened urls

Adds the 'shorten' command, currently hard-coded to use bit.ly
Also adds a sniffer to find short urls and expand them

Original Module by Wil Hall - Hacked to death by Selig Arkin

#### `@shorten [service] <long-url>` ####
Condences <long-url> using the given service (currently defaults to bit.ly)

# tachi ( By Ross Delinger ) #

Named for Tachikoma the bot in irc.quickfox.net/#subnova created by _3of9
It spams random blurbs and twitter posts all the time
Its purpose here is to spit out rss feed updates


#### `@feed add <feed name> <feed url>` ####
Add a feed to monitor

#### `@feed force <feed name>` ####
Force the given feed to be updated

#### `@feed remove <feed name>` ####
Remove the given feed

#### `@feed clear` ####
Clear the monitor of all feeds

#### `@feed list` ####
Return a list of all stored feeds

# test ( By Various ) #
Example Module to test various new features as they are added.

Feel free to add to them!


#### `@test timer start` ####
** No docstring given **

#### `@test timer stop` ####
** No docstring given **

#### `@test timer delay` ####
** No docstring given **

#### `@test crash` ####
** No docstring given **

#### `@test userinfo` ####
** No docstring given **

#### `@test chaninfo` ####
** No docstring given **

#### `@test say` ####
** No docstring given **

# translationparty #
Adds the 'translationparty' command, allowing users to connect to google translator to translate a phrase back and forth from English to Japanese, using translationparty.com's phrases after an equilibrium is found.

#### `@translationparty` ####
** No docstring given **

# unicode ( By Selig Arkin ) #
Looks up information using the unicode database of happy! Yayyy!

#### `@unicode <char or search>` ####
Searches for information on the given char or, does an exact-match search for a char named in the args

# weather ( By Ross Delinger ) #

A weather forcast module that works using the weather underground api


#### `@weather <city>` ####
Returns the current forcast for the given area should be able to take area code or city

# wikipedia #
Looks up information from a MediaWiki wiki - Currently only Wikipedia

Please note that this is still in development and needs some kinks to be worked out still

#### `@wikipedia <search>` ####
Searches through wikipedia for the given search string

# youtube #
Implements various commands to interact with YouTube, and a meta information grabber

#### `@youtube <search string>` ####
Searches youtube for the given search string
