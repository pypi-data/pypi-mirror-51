# Hooke
Written in python, and based on quite a few requirements
  
It is yet to work properly

## Installation
```
pip install pyHooke # Stable PyPi
pip install git+https://github.com/oekshido/Hooke # Latest
```
Due to the inital installation, it may be required to install nltk datasets manually

## Usage
To run a simple textual check:
```python
from Hooke import Hooke

hk = Hooke() #Inits
hk.Textual(input="test/test.txt") #Runs the fast, textual comparison
hk.Shingled(input="test/test.txt") #Runs the nltk and shingle comparison
```

## Contributing
Just pull request, with a brief explanation of the changes.
