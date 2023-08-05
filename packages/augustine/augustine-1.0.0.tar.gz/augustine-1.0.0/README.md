## Synopsis

This package makes setting up new Python packages easier.
It has support for creating new virtualenvs,
as well as being able to make it easy to run your package via
    `python -m <package>`

## Developer Requirements

#### Python VirtualEnv

You must have `pip` v9.0 or greater in order to install this package into a
virtualenv. This is to avoid having to build `gevent` as a native extension.
If you have `pip` >= 9.0, then a wheel for `gevent` will be installed and you won't have to build.

To setup a new virtualenv and upgrade `pip`:

    python -m virtualenv venv
    venv\scripts\activate
    pip install --upgrade pip

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
