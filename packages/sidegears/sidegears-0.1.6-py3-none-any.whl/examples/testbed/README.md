# Development testbed

This example is has a short script that runs the kernel indefinitely,
waiting for a client to connect. You can use this to test client code
in a standard browser, where you can open the browser developer tools
for debugging.

The kernel can sometimes handle client reloads, but in some cases, you
might need to restart the runkernel.py script when reloading the html
client.

Also be advised that, after extended use with many client reloads, we
have seen the kernel process (python) consuming 100% CPU load (one
core). Be sure to periodically monitor CPU activity, and restart the
kernel script when it is more than a few percent.

## Initialize the virtual environment
```
    cd examples/testbed
    python3.7 -m venv tb-venv/
    source tb-venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt

    # Install sidegears
    cd ../..
    pip install -e .
    cd examples/testbed
```

## Run the script
```
    cd examples/testbed
    source tb-venv/bin/activate
    python runkernel.py
```
