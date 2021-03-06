# Dealer Portal

---

## About

* Project overview
  * This project is designed to keep track of customers, locations, and devices of a company that sells sensor packages for predictive maintenance.
  * The above data can be thought of as a hierarchical structure as follows

```bash
├── Customer
│   ├── Facility
│       ├── Device
```

## Getting started

* View the [documentation](http://dealer-portal.readthedocs.io/en/latest/install.html) for installing.

* Navigating the project
  * The majority of the server codebase is split into `flask blueprints` within the `portal_server` package
  * Most of the frontend code is found within `.vue` files under `./portal_server/directory/home_static/src/components/`

## Viewing the Documentation

* Go to the [docs](http://dealer-portal.readthedocs.io/en/latest/?)

## Development

* Style
  * JS = [StandardJS](https://standardjs.com/)
  * Python = [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Frontend tooling
  * Webpack can be run with `$ npm run` find the commands in ./static/package.json
* Python virtual env
  * Run `$ source env/bin/activate` from ./ to run python commands
  * Type `$ deactivate` at anytime while in the venv
* Viewing the project on the production server
  * Make sure you are in the virtual env and in the project root
  * Start the server with `$ gunicorn -w 4 portal_server:app`

## Debugging

* Tools
  * with pudb (recommended)
    * insert where you want a breakpoint `from pudb import set_trace; set_trace()`
  * with pdb
    * insert `import pdb; pdb.set_trace()`
* Tips for api and auth
  * Make sure you are sending credentials
  * Make sure to disable cache if using a browser during development
  * Make sure you are building using webpack if working on anything in directory static
* Try out new vscode [debugging for flask](https://code.visualstudio.com/docs/python/tutorial-flask)

## Writing documentation

* Notes on using
  * Just run `$ sphinx-autobuild source build/html -p 5000` from the `./docs` folder
* Build it
  1. Activate your env with `source env/bin/activate`
  2. Run `$ sphinx-autobuild docs/source/ docs/build/html/ -p 5000`
  3. Navigate to http://localhost:5000
* Style
  * [Google style docstrings](https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments)
  * Supported [sphinx flavoring](http://www.sphinx-doc.org/en/stable/ext/example_google.html) within above structure
* Learning how it works/format
  * [Tutorial with google styles included](https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example)
  * [Tutorial to understand sphinx](https://media.readthedocs.org/pdf/brandons-sphinx-tutorial/latest/brandons-sphinx-tutorial.pdf) **you need to adapt with Google style docstrings**

## TO READ

* [things which arent magic flask](https://ains.co/blog/things-which-arent-magic-flask-part-1.html)
* [Best Practices for function arguments](http://www.informit.com/articles/article.aspx?p=2314818)
* [decorators documentation](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
* [how does the property decorator work?](https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work)
* [how to make a chain of function decorators?](https://stackoverflow.com/a/1594484/6879253)

## Resources

* Sphinx [tutorial](https://media.readthedocs.org/pdf/brandons-sphinx-tutorial/latest/brandons-sphinx-tutorial.pdf) extremely helpful
* flask [Blueprints](https://books.google.com/books/about/Flask_Blueprints.html?id=SfSoCwAAQBAJ&printsec=frontcover&source=kp_read_button#v=onepage&q&f=true)
* python subprocess [explanation](http://www.codecalamity.com/run-subprocess-run/)
* [REST api](http://www.restapitutorial.com)
* [python import confustion](http://effbot.org/zone/import-confusion.htm)

## Teardown

* Run `$ ./server_management/teardown_script.sh`
* Delete project folder