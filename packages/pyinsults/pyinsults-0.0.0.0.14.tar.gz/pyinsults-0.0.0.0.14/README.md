# pyinsults

That's right, harness the power of `Python` to dynamically call your users really inapropriate names.

# Installation

Install using ```pip install pyinsults```

Upgrade *frequently* using ```pip install pyinsults --upgrade```


# Usage

```from pyinsults import insults ```
> Done in [.01s]

``` print(insults.short_insult()) ```
> dickwad

``` print(insults.long_insult()) ```
> stinking dickwad

``` print(insults.insultify("Have a nice day, you {}!")) ```
> Have a nice day, you stinking dickwad!


# Deployment

Build using ```python setup.py sdist bdist_wheel```

Upload using ```twine upload dist/*```
