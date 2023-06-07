# mvd 
mvd (an acronym for "multi-value dictionary") is an interactive command-line tool that stores a multivalue dictionary in memory. All keys and members are strings.

## Requirements:
* should be an interactive console application 
* a dictionary (map) of unordered collections class
* keys are strings
* values are an unordered collection of strings  
* should implement the commands in the work_sample_final.pdf
* when deleting key (and/or member), throw error on missing key
* when deleting value, throw error on missing value
* when adding an item (key/value pair), create key if it doesn't exist
* when adding an item (key/value pair), throw error if value exists
* when getting all items for key, throw error on missing key

## Added bonus features
* rich, colorful help prompts
* dynamic, lazy loading of sub-commands 
* interactive cli command auto-completion 
* interactive cli command history
* optionally loads and saves dictionary to a file
* options can get their values from env vars prefixed with "MVD_". This is especially useful for the `--dict-file` option

## Installation 
to install mvd on Python 3.x, you can use pip: 
```
pip3 install git+https://github.com/dontascii/mvd
```
Make sure your pip installation is current, otherwise pip install might fail. 
___
Alternatively, you can clone the repository to a location of your choosing, 
`cd` to that location, and install: 

#### Cloning the repository
there are several ways to clone the repo: 
* using the `gh command-line tool from github: 
```
gh repo clone <url> 
```
* using ``git clone``:`
```
git clone <url>
```
#### Install
make sure you are in the root directory where the repo was cloned and then: 
```
pip3 install . 
```
___
You might want to create a Virtual Environment and install it there. If you do that, 
you will have to activate the virtual env in order for the `mvd` command to be available.  

## Usage
after installing the package, a new command will be available in your terminal. ``mvd``
```
mvd --help
```

#### Interactive CLI
the interactive cli is launched by the sub-command 'cli': 
```
mvd cli
```

#### Commands
all commands in the mvd cli are also available as sub-commands and can be run directly from your terminal. 
```
mvd add foo bar
```

Commands are lazy loaded at run-time and the app can easily be extended with new commands with little effort. The application looks for commands in the ./commands folder. Command filenames must start with "cmd_" and end in ".py". In the file, there must be a function called "cli" which is decorated with @click.command. To have access to the dictionary at run-time, the function also needs to be decorated with @pass_environment. See the existing commands in the "commands" folder for examples.

The commands that are available in the interactive cli are the same commands available as sub-commands directly from the terminal. No code changes are necessary outside of the commands folder to add a command. The help prompt for each command is generated from the docstring of the cli function defined in the cmd_*.py file. In the interactive cli, `HELP <CMD>` contents use the `short_help` parameter,  passed in the @click.command decorator. See the existing commands to see how this works.  

#### --dict-file option (-d)
The `-d` or `--dict-file` option on the mvd command allows the dictionary to be persisted to disk. The dictionary can be loaded from a file and saved to the file using this option. This can be used with the interactive CLI or when running commands directly from your terminal. In fact, if you run a command directly from the terminal without using the `--dict-file` option, a warning is displayed.  

```
mvd add foo bar
Warning: no dict_file set. The dictionary will be destroyed after this command completes.
Use '-d <file>' option to persist dictionary to a file.
Added
```
In the above output, I ran the ADD command, adding key="foo" and value="bar". 
The warning printed indicates that, although my key and value will be added to the dictionary, the dictionary will be gone as soon as the command completes. You can see in the output, "Added" was returned, which indicates the key/value pair was added, but the dictionary lives in memory only for the life of the command.  

Use the `-d` or `--dict-file` option to avoid this. 
```
mvd -d dict.yaml add bar foo
Added

mvd -d dict.yaml members bar
foo
```
Now the key/value added is retained by saving the dictionary to a file. The dictionary is saved as YAML, in order to be human-readable and support the data types used in the dictionary.  If the file does not exist, it will be created when the command completes.  If it does exist and contains valid YAML, the file contents will be deserialized and loaded into the dictionary before the command is executed. The `-d` or `--dict-file` option works with the interactive cli as well. 

#### using environment variables for options 
Command-line options can also be set in environment variables. The app will look for environment variables that start with "MVD_" followed by the option name in all caps, with hyphens changed to underscores.  This is especially useful with the `-d` or `--dict-file` option. The environment variable name would be "MVD_DICT_FILE".  

```
// set the environment variable (macOS) //
export MVD_DICT_FILE="/Users/joel.clegg/Projects/Python/Spreetail/mvd/mvd/dict.yaml"

// now we don't need to use the -d option with commands: //
mvd add this works
Added
mvd members this
works
```
