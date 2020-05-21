# BigDataProject
This is the repo from Group #17 (*A student*: **Ivan Martini**, *B student*: **Beatrice Marsili**) about the course project 2019/2020 of **Big Data Technologies @ UniTN**
The core of the project is the python programming language, version 3. The goal will be using Flask and plain python to achieve the result, but also to dig deeper inside the Big Data thing. Everything runs on a python virtual environment (in order to avoid compatilibity issues on different devices).

## Setup
To setup the working environment first create one named `virtual`. You don't have to stick to this name, but if you want to change it, please modify the *.gitignore* accordingly. 

`
$	pyhton3 - m venv virtual
`

Then activate the environment and install all the required packages. They are stored inside teh *environment.txt* file.

`
$ 	. virtual/bin/activate
`
`
$	pip install -r environment
`

If, while working you installed new packages, no changes will be saved on the repo, since the folder *virtual* is excluded by the *.gitignore*. The correct way to save a file is updating the *environment.txt* file, simply issuing

`
$	pip freeze > environment.txt
`

All the private API keys and sensitive data are to be update inside a file *privates.py*. Again, anything won't be saved on the repo thanks to the *.gitignore* settings. All the configuration parameters are to be saved in the file *utilities.py* instead.

## Startup
Before working on anything, start the virtual environment:

`
$ 	. virtual/bin/activate 
` 

While in the virtual environment and module packet downloaded will be stored locally. The changes to any file, however, will persist. To quit the virtual environment just type:

`
$ 	deactivate
` 