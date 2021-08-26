# Functional Test

This repository contains a simply functional test for Permanent.org. It is designed to test that the application can successfully upload and process file types that is needs to support.

## Run instructions

First, download the canonical file dataset. Save it to a sibling directory named "files".

Then, set up the virtual environment, install the dependencies, and run the script!

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run_test.py dev apiKey ../files/
```

See `python run_test.py -h` for more information about the arguments it accepts.

In Powershell, use .\venv\Scripts\activate instead of source venv/bin/activate

The test can also be run from the ["Actions" tab](https://github.com/PermanentOrg/functional-test/actions).
