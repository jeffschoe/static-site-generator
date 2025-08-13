# Use python to run the unittest module as a script
# Discover auto finds and runs tests based on certain naming conventions...
# ... all test functions and file names must start with test_ to be discoverable by unittest
# -s src tells us to look for these tests starting in the src directory  
python3 -m unittest discover -s src
