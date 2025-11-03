
## Problem

Often i face an issue when i want to save important commands for my developer and student work. 
The HISTORY gets reduced or the command is being pilled under other similar commands and is really hard to find
Also when i use new computer all that history is lost

Also i cannot set comment or add any note when some command may be actually useful. Currently it is only guessing and hoping i remember what command is doing what

## Application

The application is simple python CLI application dedicated to only bash/linux

Application provides two commands:

1) rem - takes last command from history and (this will need to be a bash command that will be appended to .bashrc during setup) calls `rems store "DATA" --note "SOME NOTE"` python command. This bash command will also take optional argument: "NOTE" that will add a user note. This code will implemented in user .bashrc file and added using `rems install` command. For reference see @his.sh file
2) rems - Python command line application written in click

commands:
a) rems store (IMPLEMENTED) - this command will store the command passed by rem bash command.
The commands are stored under the ~/XDG-PATH..something /rem/commands.csv file. The csv has schema like: COMMAND,NOTE,DATE(without hour),NUMBER_OF_HITS(1 by default),

`store` will:
- access the store file
- check if the command is already saved in csv file, if yes it should just increase number of hits by one and update the Note if it is provided
- if no it should create new row in csv file with command information

b) rems - standalone command (use `@click.group(invoke_without_command=True)`). This should list max 20 last commands (ordering: hits, date). This should be displayed and be able to search through fzf See @quotes.py app.
The selected command should be added to the history at the very top (see @drawer.py)
The selected command hits counter should increase by 1
Then the selected command should be printed with note, number of uses and date. Also some message should be shown like: "Access command using UP arrow" or something better

options:
-c the command will also use `xclip` to save the command on clipboard
-s silent mode (no final message at all)
-n number of displayed commands (20 by default)

b) rems list (IMPLEMENTED)
Lists the remembered commands in ordering: hits, date displays last N commands where n is and option in cli with default: 20
The display should also display the data is some nice to look at format in cli tables

c) rems install (PARTIALLY IMPLEMENTED) - creates .config / .rem directories . Creates empty commands.csv file and shows small guide on how to use the application with some encouragement. Asks the user to add the "rem" command to .bashrc (create the command with echo "function code" >> ~/.bashrc so the user can just execute it by themselves

Abstractions:
Create store_manager that will be an interface between csv file and rest of the application

Example:
> tar -jxvf remote_drugs/populate_data/ready*.tar.bz2
> rem "Dekompresja pliku z baza lekow"

> npm run storybook
> rem

> rems
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Search commands:                                                                                                                                                                                                                            │
│   Number/Number ────────────────────────────────────




commands:
a) rems store - this command will store the command passed by rem bash command.
The commands are stored under the ~/XDG-PATH..something /rem/commands.csv file. The csv has schema like: COMMAND,NOTE,DATE(without hour),NUMBER_OF_HITS(1 by default),

`store` will:
- access the store file
- check if the command is already saved in csv file, if yes it should just increase number of hits by one and update the Note if it is provided
- if no it should create new row in csv file with command information

b) rems list
Lists the remembered commands in ordering: hits, date displays last N commands where n is and option in cli with default: 20
The display should also display the data is some nice to look at format in cli tables

c) rems install 
Creates empty commands.csv command


You have basic click command structure prepared. Create me a click cli command: "rems" that will implement this functionalities:
  commands:
  a) rems store - this command will store the command passed by rem bash command.
  The commands are stored under the ~/XDG-PATH..something /rem/commands.csv file. The csv has schema like: COMMAND,NOTE,DATE(without hour),NUMBER_OF_HITS(1 by default),

  `store` will:
  - access the store file
  - check if the command is already saved in csv file, if yes it should just increase number of hits by one and update the Note if it is provided
  - if no it should create new row in csv file with command information

  b) rems list
  Lists the remembered commands in ordering: hits, date displays last N commands where n is and option in cli with default: 20
  The display should also display the data is some nice to look at format in cli tables

  c) rems install
  Creates empty commands.csv command

Create me a simple test cases that test out happy paths in app. DO NOT WRITE EDGE CASE TEST CASES!! Remember to unittest only the happy path. Remember to create conftest with fictures that create temporary commands.csv file using namedtemporaryfile object. THe pytest is already installed
