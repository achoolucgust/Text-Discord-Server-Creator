# Text Discord Server Creator
Create discord servers out of text files. Purely python

## Plan to add
User limit for VCs.

## Requirements & Depedencies
Only requirement is Python 3, pip, and a Windows system.

Depedencies:
- nextcord
- json
- colorama

Do these commands to download all of them:
- `pip install nextcord`
- `pip install json`
- `pip install colorama`

## How to run
1. `git clone` this project
2. `cd` to the folder
3. `python main.py`

## .dcsrv Format
For an example, check Example.dcsrv in the Servers directory.
```
== DATA
NAME=The server name
DESC=Blah blah blah blah
```

This is just for channel/category decoration.
```
== DECORATION
CATEGORY_START=<- 
CATEGORY_END= ->
CHANNEL_START=∙│
LAST_CHANNEL_START=∙└
```
- CATEGORY_START appears at the start of every category name. (You should know what CATEGORY_END does.)
- CHANNEL_START appears at the start of every channel name.
- LAST_CHANNEL_START appears at the start of __*the last channel of a category*__.

For the example above, if you put **"Info"** as one of the category names, it would turn to **"<- Info ->"** in Discord.

```
== CHANNELS
# Main
- Info
- Welcome
- General
+ [6] + VC 1
```
The `#` means a category, `-` means a text channel, and then the `+` means a voice channel.

In the example above, it makes 4 channels in the category **"Main"**.
- Info (Text channel)
- Welcome (Text channel)
- General (Text channel)
- VC 1 (Voice Channel with 6 member user limit *\[wip\]*)