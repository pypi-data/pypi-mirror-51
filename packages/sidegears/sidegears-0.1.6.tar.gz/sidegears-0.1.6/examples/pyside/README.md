# PySide example

A minimal application using PySide/QWebEngine for the browser. The
python and javascript code implement a simple multiplier function
to show request calls invoked from the front end.

Although functionality is minimal, the use of PySide/QWebEngine
would result in a **huge** executable package on the order of 300 MB
uncompressed on linux (the pyside webengine library itself is over
100MB). So this example is provided only to show that an embedded
browser can be used.

Side note: we tried using fbs with PyInstaller to generate an
executable, but there were problems install all of the QtWebEngine
components.

## Initialize the virtual environment
```
    cd examples/pyside
    python3.7 -m venv py-venv/
    source py-venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt

    # Install sidegears
    cd ../..
    pip install -e .
    cd examples/pyside
```

## Run the script
```
    cd examples/pyside
    source py-venv/bin/activate
    python run.py
```
