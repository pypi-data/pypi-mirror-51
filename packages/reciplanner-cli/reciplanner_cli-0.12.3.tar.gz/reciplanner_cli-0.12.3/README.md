## **Reciplanner - Command Line Interface**


### What is Reciplanner?
---
Reciplanner is a cross-platform open source tool designed to help people manage the items in their kitchen, and the recipes in their cookbooks.

![Demo Picture](https://i.imgur.com/ECPaNxP.png)

### Features
---
* Keep track of what's in your kitchen, where it is, and when it expires
* Sort your kitchen by custom categories
* Automatically convert new recipes from imperial units to their metric counterparts
* Tell you exactly what ingredients you're missing to make a recipe, and how much of each you're missing

### File locations
---
Reciplanner creates 2 small files on first launch, which contain your recipes and the items in your kitchen. Their locations are listed below

##### Linux
~/.config/Reciplanner
##### Windows
%AppData%\\Local\\Reciplanner
##### MacOS
~/Library/Preferences/reciplanner

### Dependencies
---
* pint

### Getting started
---
Install the program via pip

> pip install reciplanner_cli

and run it

> reciplanner_cli
