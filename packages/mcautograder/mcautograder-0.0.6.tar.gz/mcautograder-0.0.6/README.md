# Multiple Choice Autograder

 [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/chrispyles/mcautograder/master?filepath=demo/mcautograder-demo.ipynb)

This repository contains a small Python-based multiple-choice question autograder inteded for use in Jupyter Notebooks. It is meant to be packaged with each assignment so that they are easier for use on third-party servers, e.g. MyBinder.

## Installation

You can install `mcautograder` using pip.

```bash
pip install mcautograder
```

## Usage

To use the autograder, import the `mcautograder` package and make sure to your [tests file](#tests) is in the same directory as your notebook. When you load the notebook dependencies, import the file and initialize the grader by creating an instance of the `Notebook` class:

```python
import mcautograder
grader = mcautograder.Notebook()
```

**The autpgrader automatically assumes that the tests file is stored as `"./.tests.py"`.** More details [below](#tests).

If you want the autograder to score the questions, make sure to set `scored=True` in your `Notebook` call. **The default behavior of the autograder is to allow students to submit answers until they get the correct one.** If you want to change this behavior, you must set the `max_attempts` argument to an integer, the maximum number of retakes allowed. If this is the case, when students hit that ceiling, the check cells will throw an `AssertionError` because they've hit the retake ceiling.

An example call for a scored notebook with a retake ceiling of 5 is given below.

```python
grader = Notebook(scored=True, max_attempts=5)
```

To use the autograder to check answers, have students assign their answers to variables in the notebook; these answers can strings of length 1 or single-digit integers. Then call the `Notebook.check()` function; the first argument should be the question identifier in your tests file and the second should be the variable the student created.

```python
my_answer = "A"
grader.check("q1", my_answer)
```

If the student's response matches the test file, then `Correct.` will be printed; otherwise, `Try again.` will be printed. If the student enters an invalid response (e.g. `float`, answer of > 1 character, hit retake ceiling), the grader will throw an `AssertionError` with a descriptive message.

To get the score on a scored autograder, simply call `Notebook.score()`:

```python
grader.score()
```

The output will contain the fraction of earned points out of possible points and the percentage.

For a more descriptive introduction to the autograder, launch our [Binder](https://mybinder.org/v2/gh/chrispyles/mcautograder/master?filepath=demo/mcautograder-demo.ipynb).

<div id="tests"></div>

## Tests

The autograder relies on a tests file to get the answers for the questions. In this repo, the file is `tests.py` and it is public; in practice, I usually distribute the answers as a hidden file, `.tests.py`. It is unhidden here so that you can peruse its structure and contents.

The `Notebook` constructor by default assumes that your tests are in the file `.tests.py`. If you have a different preferred location, you can pass the path to the file by setting the `tests` argument of the constructor:

```python
grader = Notebook(tests=SOME_OTHER_PATH)
```

In the file, we define a variable `answers` which is a list containing dictionaries, each of which represents a single question. Each dictionary should contain 3 keys: `"identifier"`, `"answer"`, and, optionally, `"points"`. If your assignment is unscored, you can leave off the `"points"` key. A description of the keys' values is given below:

| Key | Value Type | Value Description |
|-----|-----|-----|
| `"identifier"` | `str` | a unique question identifier |
| `"answer"` | `str`, `int` | the answer to the question; specifications below |
| `"points"` | `int` | optional; the number of points assigned to that question |

Answers **must** be of length 1 (i.e. a single-character string or a single-digit integer). The autograder is currently set up to throw an `AssertionError` if an answer of length > 1 is submitted, although we do intend to add this functionality later.

An example of a file is given below.

```python
answers = [
	{
		"identifier": "q1",
		"answer": 3,
		"points": 1,
	}, {
		"identifier": "q2",
		"answer": 2,
		"points": 2,
	}, {
		"identifier": "q3",
		"answer": "D",
		"points": 3,
	}
]
```

The identifiers have no set format. This is because the identifier is passed to `Notebook.check()` when you call it in the notebook.

## Branches

The `master` branch contains the current state of `mcautograder` as it is hosted on PyPI. The `dev` branch contains the next version of `mcautograder` in development. _Do not commit directly to the `master` branch._ Make commits in the `dev` branch and then PR to the `master` branch before uploading to PyPI.

## Changelog

**v0.0.6:**

* Added state serialization to prevent dead kernels from resetting notebooks
* Added `".tests.py"` as default argument value for `Notebook` constructor
* Added `AssertionError` for scored notebooks with 0 points
* Added try/except statement for scored notebook identifiers without `"points"` key

**v0.0.5:**

* Changed `mcautograder.py` to `notebook.py` for less confusion
* Changed `max_retakes` param to `max_attempts` for better understanding
* Upadted docstring format for sphinx autodoc
* Added license field for setuptools

**v0.0.4:**

* Moved utils to separate file for documentation

**v0.0.3:**

* Changed structure of tests file to be more intuitive
* Added docstrings and better documentation
