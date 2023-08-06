# Example webruntime application
This example displays a simple page with one function to multiply a
couple numbers. It is setup to build an executable using python 3.7,
and uses webruntime to locate and run the default browser installed on
the desktop machine.

A PyInstaller spec file is included to build a binary executable.

## Initialize the virtual environment
```
    cd examples/webruntime
    python3.7 -m venv wr-venv/
    source wr-venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt

    # Install sidegears
    cd ../..
    pip install -e .
    cd examples/webruntime
```

## Run the script
```
    cd examples/webruntime
    source wr-venv/bin/activate
    python run.py
```

## Build the executable
Use the pyinstaller SPEC file to build the executable.
```
    pyinstaller run.spec
```

Remember NOT to pass in the `run.py` file. The spec file is needed
to add a missing data file from jsonrpcserver. On linux, this generates
a folder totaling ~14MB uncompressed.

To run the executable:
```
    ./dist/run/run
```

Note that additional work is needed to bundle an installer package,
primarily to include the client files and set its location in the
file url.
