conftext - a helper for managing configuration contexts

Motivation
----------
Imagine handling multi-tenant services, that each require certain config contexts to be specified
for using them (think db connection information for instance). The parameters of these config
options are the same, but their values differ. You are creating CLI tools for working with these
services and find yourself doing:

.. code-block:: shell

   $ some_task1(db_host=service_A_ip, db_name=service_A_name, param1, param2)
   $ some_task2(db_host=service_A_ip, db_name=service_A_name)
   $ some_task3(db_host=service_A_ip, db_name=service_A_name, param1)
   
   $ some_task1(db_host=service_B_ip, db_name=service_B_name, param1, param2)
   $ some_task2(db_host=service_B_ip, db_name=service_B_name)
   $ some_task3(db_host=service_B_ip, db_name=service_B_name, param1)

This small library intends to help bring things back to:

.. code-block:: shell

   $ some_task1(param1, param2)
   $ some_task2()
   $ some_task3(param1)

This is just an example. The tool is meant to be generic and is not nescessarily only made for this
particular use case.

Current operation
-----------------
Use `get_config` in code where context-aware config should be loaded. The conftext invoke task can
then be used to switch the context config.

Todo
----
1. could probably drop dependency on invoke
2. the functions and globals in the module could be made into a class
3. add a enter task for the CLI tool that will enter the conf context?
   - when inside conf context, consider modifying the prompt to show vital context config
   - add exit task as well
4. add python prompt with config context as well?
5. include handling of virtualenv àla virtualenvwrapper? otherwise 4 could come in conflict

Future suggested usage pattern
------------------------------
1. prepare a dict with a set of default config options that can be passed to 
   `create_initial_config`.
2. initialize the `Conftext` class with the section that should be looked for and the default
   config dict.
3. call get_config.

Example in code
---------------
.. code-block:: python

   defaults = dict(
       service='beat',
       context='local)
   
   config = Conftext(section='rytm-dbkit', default_config=defaults)

Command-line usage
------------------
.. code-block:: shell

   $ conftext show
   $ conftext set --service <someservice>
   $ conftext set --service <someservice> --context <somecontext>
