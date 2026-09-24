beauty-cpp
==========
A simple tool used to generate cross reference of cpp project, implement in python.

# Dependencies
* Python 3.11
* libclang 20 (the Clang Python bindings must match its major version)
* Python packages in `requirements.txt` (`clang==20.1.5` and `ply==3.11`)

Install libclang 20 with your system package manager (for example, `sudo dnf install clang20-libs` on Amazon Linux 2023), then install the Python dependencies:

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

If your system does not provide an unversioned `libclang.so` in the library search path, point the tool to the versioned library before running it, e.g. `export LIBCLANG_LIBRARY_FILE=/usr/lib64/llvm20/lib64/libclang.so.20.1` on Amazon Linux 2023 (adjust for your installation). Do not use libclang 3.4 with the new bindings.

#Demo
* Just email me, if you just want to read some code, and don't want to deep into the compile process of the project.
* http://42.121.145.91:8000/

#Usage
* Find your system include path with command 'cpp -v'
* add the include search path to args in bc.py
* try compile your project and add the arguments provied to gcc/g++ to  args also
* add the source code file name to the srcs array
* run `/path/to/beauty-cpp/.venv/bin/python /path/to/beauty-cpp/bc.py` in your project; create a `data/` output directory first. The indexing block in `main()` is disabled by default; uncomment it to rebuild `usr.db` from the configured sources before rendering.

#Comming Soon
* function list
* link to global variable
* reference to Class and Method
* syntax error report

#Licence

MIT
