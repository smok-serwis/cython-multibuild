# v1.6

* certified for Python 3.11 and 3.12
* CI moved to GitHub Actions

# v1.5

* fixed logging
* `snakehouse` doesn't need cython and satella installed in advance
* added `find_all`
* made available for PyPy users
* deprecated `find_pyx`, `find_c` and `find_pyx_and_c`

# v1.4

* added `find_pyx`, `find_c` and `find_pyx_and_c`
* added documentation

# v1.3.2

* added `read_requirements_txt`

# v1.3.1

* Cython build step ("cythonize") will be parallelized by default

# v1.3

* added an option to build every file as a separate extension, for
  usage in tests

# v1.2.3

* `Multibuild` will pass given kwargs to `Extension` object
* added an option to monkey-patch `distutils` to compile multicore

# v1.2.2

* snakehouse will pass the remaining arguments to Multibuild to Cython's Extension

# v1.2.1

* snakehouse won't complain anymore if installing 
  from a source wheel

# v1.2

* fixed issue #1

# v1.1.2

* bugfix release: fixed behaviour if there was only
  a single file in Multibuild

# v1.1.1

* allowed Linux-style paths on Windows build environments

# v1.1

* added the capability to insert standard `Extension`s
  in the snakehouse build() command

# v1.0.2

* got rid of some C compiler warnings
* module will now use mako to render the files

# v1.0.1

* standard C files will be allowed in the builds
* added support for Pythons 3.5-3.6
