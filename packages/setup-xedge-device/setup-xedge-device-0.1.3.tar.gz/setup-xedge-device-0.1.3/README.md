## Creating/uploading pypi package

**TL;DR** Run `sh upload-script.sh`

> Note that it is a very env dependent option

Steps:
- Check setup.py's declared package version
- Run
    ```bash
    # create source distribution
    python setup.py sdist
    # upload to test repo
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    # if ok, upload to pypi
    twine upload dist/*
    ```