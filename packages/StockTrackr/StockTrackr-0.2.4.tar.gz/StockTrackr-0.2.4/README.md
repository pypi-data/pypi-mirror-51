# StockTrackr

This is a basic application that uses alpha_vantages API to pull stock data as well as monitor it real-time.

----
### Installation

You can use pip to download the package directly:

> pip install StockTrackr


Setup the venv by first installing/activating it with:

> ./venv.bat


Then, initialize the venv with superset with:

> ./initialize_venv.bat

This creates a new file "run_superset.bat" which can be used to start the server.

----

### Usage

Use the Stox() class to gain access to all methods

>import StockTrackr

>stox = StockTrackr.Stox()

The UI() method provides an easy-to-use, command-line entry point to run the program

>fx.UI()
