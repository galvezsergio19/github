# Streaming Data From Github
A small library that can ingest unlimited amounts of data from Github.

## How to use?

### 1. Clone Repository
```bash
git clone https://github.com/galvezsergio19/github.git
```

### 2. Setup with virtual environment
```bash
# setup virtualenv
virtualenv -p python3 env

# start using virtualenv
source env/bin/activate

# install the required Python packages for the development environment
pip install -r requirements.txt

# stop using virtualenv
deactivate
```

### 3. Run Program

You can check parameters of the `main.py` script with the use of the following command:
```
python main.py --help
```

you can run the script by specifying parameters using the example command below:
```
python main.py \ 
--owner='moby' \
--repositories='moby,toolkit,tool' \
--resources='issues,commits,pull_requests'
```

### 4. Running Tests
```
python -m unittest tests/test_github.py
```

## Output
Program will generate JSON file(s) which contents are from the API call to `read()`.

File(s) will be stored on **resources/owner-name/repositories-name** folder. 

Structure of JSON file will be similar to below:

```
{
    "repository-1": {
        "<resource-1>": {
            "url": <url-of-api-call>,
            "data": <actual-data-from-api>
        },
        "<resource-2>": {
            "url": <url-of-api-call>,
            "data": <actual-data-from-api>
        },
        ...
    },
    "repository-2": {
        "<resource-1>": {
            "url": <url-of-api-call>,
            "data": <actual-data-from-api>
        },
        "<resource-2>": {
            "url": <url-of-api-call>,
            "data": <actual-data-from-api>
        },
        ...
    },
    ...
}
```


## The Task
Write a small library that can ingest unlimited amounts of data from Github.

## Description
You will build a class that streams batches of data from Github out to the caller (the user of the object). 

The class will operate as a stream, or an iterable - such that every call to get more data, produces only a portion of that data (as the actual data can be arbitrarily large).

The class will enable it's user to get multiple types of data on multiple repositories owned by the same owner/organization using a single API.

## Requirements

Implement a single class called `Github`.

The class **constructor** is initiated using three variables.
The basic input parameters will be:
 1. `owner` - A string representing the **Owner** name.
 2. `repo` - A list of strings representing **Repository** names.
 3. `resources` - A list of desired resource names.
 
Please pick at least 3 **resources** to support ('issues', 'commits', 'users', etc.) - this will be your "Supported Resources" list and this will define what values may be passed in the resources argument.

The class must implement at least one function calls `read()` that takes no arguments.

Each call to `read()` will return a portion of data; a list of data points returned from the API (e.g a list of dictionaries) 
The class must iterate of every repository and resource combination as the user calls `read()` multiple times.

The resources in the input must be a subset of the support resources, meaning you might support N different resources inside the class, but the caller may only be interested in M resources, so M is a subset of N. 

For each resource make sure you iterate on all the pages of the result (it can be more than a single request) - but **don't read all pages** in a single call to `read()`, instead every call should fetch the next page until the resource is depleted, then move to the next resource and/or next repository. 

When there is no more data to return, return None.

## Example 

If the input is:
 - owner='moby'
 - repositories=['moby', 'toolkit', 'tool']
 - resources=['issues', 'commits', 'pull_requests']
 
 As we call `read()` repeatedly it will return all the issues, commits and pull requests for the repositories at `/moby/moby`, `moby/toolkit`, `moby/tool` (no particular order, see notes). 

## Usage 

Your class will be used in a manner similar to the sample below:

```
gh = Github(arguments)

data = gh.read()
while data is not None:
    # do something with the data
    data = gh.read() # fetch next batch
```


## Notes 

- Order of iteration is not important for this assignment.
- No need to perform input validation (you can if you want to, but it's not a requirement for the task).
- Don't use any existing github library/SDK, make direct calls to the API.
- We only care for reading data from github, not writing to it.

## What Are We Looking for?

We are trying to estimate your optimal code quality and have a peek at your thought process. All this without time limitations, or (too many) restrictive conditions, so please follow best practices. Consider **conventions**, **comments**, **documentation** and **tests**. We wish this to be built by the same quality standards you'd like to see in your production code.
