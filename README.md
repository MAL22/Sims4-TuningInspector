<h1 align="center">Sims 4 Tuning Inspector</h1>
<p align="center">
<a href="https://github.com/MAL22/Sims4-TuningInspector/commits/master">
<img src="https://img.shields.io/github/last-commit/MAL22/Sims4-TuningInspector.svg?style=flat-square&logo=github&logoColor=white" alt="GitHub last commit">
</a>
</p>

## About

Tuning Inspector is a resource for modders of The Sims 4. As we all know, The Sims 4 employs XML tuning which are interpreted to build Python objects by the game. In almost every case however, the structure of an XML tuning does not correspond to the Python objects and their attributes when they are created by the game. Tuning Inspector enables modders to peruse the Python object (and its attributes) associated with an XML tuning.

This is extremely useful when implementing custom Python injectors to avoid overriding XML tunings (and thus incompatibility issues) and significantly reduces development time when attempting to inject into unknown Python objects.

## Table of Contents

- [Usage](#Usage)
   - [Scripts](#Scripts)
   - [Commands](#Commands)
- [Installation](#Installation)
- [Configuration](#Configuration)

## Usage

### Scripts

#### compile.py

Compiles and packages all the scripts and modules contained within the `src` folder into a **.ts4script** archive.

#### copy.py

Copies all the scripts and modules from the `src` folder to a development sub-folder in the path defined by `mods_folder`.

#### decompile.py

Decompiles all the EA Python files contained within the installation folder of the game and adds them to the project in the `EA` folder.

#### launch_s4s.py

Lists all available package files in the `assets` folder and opens the selected one in Sims 4 Studio.

### Commands

#### tuning.dump

Prints the output of the currently designated attribute path of a Python object to a file:

`tuning.dump <tuning id> [attribute path]`

##### Example

> tuning.dump 107344 outcome._success_actions

#### attribute path

* Each attribute contained within the path is separated with by a dot. 
* An index can be provided by including [x] at the end of a data structure attribute (list, set, dict, etc.) If not index is provided, the script will default to index 0.

##### Example

> tuning.dump 107344 outcome._success_actions.loot_list[1]

#### tuning.clear

Clears the output file of the specified tuning id:

> tuning.clear [tuning id]

##### Example

> tuning.clear 107344

# Installation

Within the project directory, execute `compile.py` and copy the resulting **.ts4script** archive to the Mods folder of The Sims 4.

# Configuration

Prior to packaging the source code, certain parameters within `settings.py` have to be modified in order for some project scripts to function properly.

### game_folder

This variable has to contain the path to the **The Sims 4** installation folder.

### mods_folder

This variable has to contain the path to the **Mods** folder.

### s4s_executable

This variable has to contain the path to the Sims 4 Studio executable.
