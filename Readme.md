Shared Expenses
===============
Manage shared expenses. It uses data from [Expense Manager](https://play.google.com/store/apps/details?id=com.expensemanager).

Requirements:
-------------
* Python
* Flask
* requests

Installation:
-------------
* clone Git repo

        git clone https://github.com/lpolasek/shared-expenses.git

* configure it

        cd shared-expenses
        cp wsgi/config.py.sample wsgi/config.py
        edit wsgi/config.py to set your configuration

* satisfy dependencies

        pip install -r requirements.txt

You can also install the dependencies using *virtualenv*.

* test shared-expenses

        python wsgi/main.py

    - open http://127.0.0.1:5000 with a web browser

