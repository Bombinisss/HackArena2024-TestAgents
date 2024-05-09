# HackArena2024-TestAgents

This repository contains scripts that are used to run and test agents.

## Setup

### Requirement

1. Git clone this repo.
2. Make sure to use Python 3.9 with conda, pyenv, etc.
3. Create virtual environment:

   ```ps
   python -m venv venv
   ```

4. Activate venv:

   ```ps
   .\venv\Scripts\activate
   ```

5. Install the game from the local package:

   ```ps
   pip install dungeon-0.1.6.tar.gz
   ```

6. Run the game:

   ```ps
   coderone-dungeon --interactive coderone.dungeon.agent
   ```

### Run main script

You can run it with default options just with:

```
python main.py
```

But, there is a lot of parameters. Here's the output of `python main.py --help`:

```
usage: main.py [-h] [--config-file CONFIG_FILE] [--agent-folder AGENT_FOLDER] [--num-matches NUM_MATCHES]
               [--output-file OUTPUT_FILE]

Run a tournament of agents

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        Path to the config file
  --agent-folder AGENT_FOLDER
                        Path to the folder containing agent Python files
  --num-matches NUM_MATCHES
                        Number of matches to run per pair of agents
  --output-file OUTPUT_FILE
                        Path to the output JSON file
```
