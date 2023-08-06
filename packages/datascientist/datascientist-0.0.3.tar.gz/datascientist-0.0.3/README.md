# The Cloudframe Data Scientist Simple Enabler

At Cloudframe we employ teams of Data Scientists, Data Engineers, and Software Developers.  Check us out at [http://cloudframe.io](http://cloudframe.io "Cloudframe website")

If you're interested in joining our team as a Data Scientist see here: [Bid Prediction Repo](https://github.com/cloudframe/texas-bid-prediction).  There you'll find a fun problem and more info about our evergreen positions for Data Scientists, Data Engineers, and Software Developers.

This package contains some convenience functions meant help a Data Scientist get data into a format that is useful for training models.  It is a light version of some of our proprietary enablers that we use to deliver data-informed products to our clients.

## Installation

`pip install datascientist`

## Dependencies

In addition to the following packages, `datascientist` requires that you have the credentials (et cetera) to perform the operation required.  For example, when connecting to an Oracle database you must install and configure [Instant Client](https://docs.oracle.com/en/database/oracle/r-enterprise/1.5.1/oread/installing-oracle-database-instant-client.html "Oracle Instant Client Instructions") or something like that.  This package does not do that for you.  

* `pandas`
* `psycopg2`
* `mysql.connector`
* `cx_Oracle`

## Structure

```
data-scientist/
|
|-- datascientist/
|   |-- __init__.py
|   |-- connection_convenience.py
|
|-- Manifest.in
|-- README.md
|-- setup.py
|-- bash_profile_example
```

## Usage

A sample bash profile is provided for reference with values removed.  Some of the functions will look for environment variables named according the conventions there.  If it can't find them it will prompt you for the appropriate strings.  Strings set via prompts are NOT saved for security reasons.  It's up to you to make sure that if you set environment variables in a more permanent way that they remain secure.

This module replicates the functionality of `pandas.read_sql()`, but is a little friendlier; handling the connection object for you while performing the same according to %timeit.

```
from datascientist.connection_convenience import *

sql = '''
select * from my_table
where my_field in ('cloud', 'frame');
'''

df = pg2df(sql)

# input at the prompts if necessary
```