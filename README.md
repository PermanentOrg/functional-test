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

The first argument to the script should be the environment that the script should run on, the second should be the `apiKey` for that environment, and the third the directory containing files for upload.
