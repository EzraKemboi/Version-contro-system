# Version-control
-system
A simple version control system like git that allows you to perform actions similar to using  github

How to use in your local machine
#Add the Project to the PYTHONPATH
 Example

set PYTHONPATH=%PYTHONPATH%;C:\Users\...path to project
# Install myscm to the current directory
"""
Activate your virtual environment,
navigate to the project's root directory i.e C\:...scm\
 and "pip install ."

#Check for available commands

myscm --help


#Testing core package

python -m unittest tests.test_core

# Testing commit

python -m unittest tests.test_core.TestCore.test_commit

# Initialize the SCM repository
python -m myscm init

# Add a file
echo "Hello, SCM!" > test_file.txt

# Stage the file
python -m myscm add file.txt

# Commit the file
python -m myscm commit -m "Add initial file"

# Create a new branch
specify the first arguments (create,list, switch)
Example
python -m myscm branch create feature-branch

# Switch to the new branch 
e.g.
python -m myscm branch switch feature-branch

# Add a new file in the feature branch
echo "Feature content" > feature.txt
#Stage file
python -m myscm add feature.txt
#Commit changes
python -m myscm commit -m "Add feature file"

# Switch back to main branch
python -m myscm branch switch main

# Merge the feature branch into main
python -m myscm merge feature-branch

#Cloning your repo

python -m myscm clone ...Path to repo


