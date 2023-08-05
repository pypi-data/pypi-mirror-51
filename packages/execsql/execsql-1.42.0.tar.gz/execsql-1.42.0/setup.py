import setuptools

setuptools.setup(name='execsql',
	version='1.42.0',
	description="Runs a SQL script against a PostgreSQL, MS-Access, SQLite, MS-SQL-Server, MySQL, MariaDB, or Firebird database, or an ODBC DSN.  Provides metacommands to import and export data, copy data between databases, conditionally execute SQL and metacommands, and dynamically alter SQL and metacommands with substitution variables.  Data can be exported in 13 different formats, including CSV, TSV, ODS, HTML, JSON, LaTeX, and Markdown tables, and using custom templates.",
	author='Dreas Nielsen',
	author_email='dreas.nielsen@gmail.com',
    url='https://bitbucket.org/rdnielsen/execsql/',
	scripts=['execsql/execsql.py'],
    license='GPL',
	requires=[],
	python_requires = '>=2.7',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Environment :: X11 Applications',
		'Environment :: Win32 (MS Windows)',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Information Technology',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Operating System :: POSIX',
		'Operating System :: Microsoft :: Windows',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 2.7',
		'Topic :: Database',
		'Topic :: Database :: Front-Ends',
		'Topic :: Office/Business',
		'Topic :: Scientific/Engineering'
		],
	keywords=['SQL', 'Postgres', 'PostgreSQL', 'SQLite', 'Firebird', 
		'Access', 'SQL Server', 'MySQL', 'MariaDb', 'ODBC', 'database', 
		'CSV', 'TSV', 'OpenDocument', 'JSON', 'LaTeX', 'table', 'DBMS',
		'query', 'script', 'template', 'Jinja', 'Airspeed'],
	long_description_content_type="text/markdown",
	long_description="""``execsql.py`` is a Python program that runs 
a SQL script stored in a text file against a PostgreSQL, MS-Access, SQLite, 
MS-SQL-Server, MySQL, MariaDB, or Firebird database, or to an ODBC 
DSN.  execsql.py also supports a set of special commands (metacommands) 
that can import and export data, copy data between databases, and 
conditionally execute SQL statements and metacommands.  These metacommands 
make up a control language that works the same across all supported DBMSs. 
The metacommands are embedded in SQL comments, so they will be ignored 
by other script processors (e.g., psql for Postgres and sqlcmd for SQL 
Server).  The metacommands make up a toolbox that can be used to create 
both automated and interactive data processing applications.

The program's features and requirements are summarized below.
Complete documentation is available at http://execsql.readthedocs.io/en/latest/.


Capabilities
============

You can use the ``execsql`` program to:

* Import data from text files or spreadsheets into 
  a database.
* Copy data between different databases, even databases using 
  different types of DBMSs.
* Export tables and views as formatted text, comma-separated values (CSV),
  tab-separated values (TSV), OpenDocument spreadsheets, HTML tables,
  JSON, LaTeX tables, unformatted (e.g., binary) data, or several other
  formats.
* Export data to non-tabular formats using several different types
  of template processors.
* Display a table or view in a GUI dialog,
  optionally allowing the user to select a data row, enter a data
  value, or respond to a prompt.
* Display a pair of tables or views in a GUI dialog, allowing the user
  to compare data and find rows with matching or non-matching key values.
* Conditionally execute different SQL commands and metacommands based 
  on the DBMS in use, the database in use, data values, user input, 
  and other conditions. Conditional execution can be used with the 
  INCLUDE and SCRIPT metacommands to implement loops.
* Use simple dynamically-created data entry forms to get user input.
* Write status or informational messages to the console or to a file 
  during the processing of a SQL script. Status messages and data exported in 
  text format can be combined in a single text file. Data tables can be 
  exported in a text format that is compatible with Markdown pipe tables,
  so that script output can be converted into a variety of document formats.
* Write more modular and maintainable SQL code by factoring repeated 
  code out into separate scripts, parameterizing the code using 
  substitution variables, and using the INCLUDE or SCRIPT metacommands 
  to merge the modules into a single stream of commands.
* Standardize the SQL scripting language used for different types of 
  database management systems.
* Merge multiple elements of a workflow--e.g., data loading, summarization, 
  and reporting--into a single script for better coupling of related steps 
  and more secure maintenance.

Standard SQL provides no features for interacting with external files or 
with the user, or for controlling the flow of actions to be carried out
based either on data or on user input.  Some DBMSs provide these features,
but capabilities and syntax differ between DBMSs.  ``execsql`` provides 
these features in a way that operates identically across all supported 
DBMSs on both Linux and Windows.

``execsql`` is inherently a command-line program that can operate in a completely 
non-interactive mode (except for password prompts). Therefore, it is suitable 
for incorporation into a toolchain controlled by a shell script (on Linux), 
batch file (on Windows), or other system-level scripting application. When 
used in this mode, the only interactive elements will be password prompts. 
However, several metacommands generate interactive prompts 
and data displays, so execsql scripts can be written to provide some user 
interactivity.

In addition, ``execsql`` automatically maintains a log that documents key 
information about each run of the program, including the databases that are 
used, the scripts that are run, and the user's choices in response to 
interactive prompts. Together, the script and the log provide documentation 
of all actions carried out that may have altered data.

The documentation includes more than 20 examples showing the use of
execsql's metacommands, in both simple and complex scripts.


Requirements
============

The ``execsql`` program uses third-party Python libraries to communicate with 
different database and spreadsheet software. These libraries must be 
installed to use those programs with execsql. Only those libraries that 
are needed, based on the command line arguments and metacommands, must 
be installed. The libraries required for each database or spreadsheet 
application are:

* PosgreSQL: psycopg2.
* SQL Server: pydobc.
* MS-Access: pydobc and pywin32.
* MySQL or MariaDB: pymysql.
* Firebird: fdb.
* DSN connections: pyodbc.
* OpenDocument spreadsheets: odfpy.
* Excel spreadsheets (read only): xlrd.

All of these can be installed from PyPI using pip.

Connections to SQLite databases are made using Python's standard library, 
so no additional software is needed.


Documentation
================

Complete documentation is at http://execsql.readthedocs.io

"""
	)
