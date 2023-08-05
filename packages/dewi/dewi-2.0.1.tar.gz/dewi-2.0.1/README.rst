DEWI: A set of commands and a framework
=======================================

Name
----
DEWI: Old Welsh form of David

The name is chosen because of the similarity to DWA, which was the project's
original name, which stands for Developer's Work Area.


Purpose
-------

As the name implies the original purpose was to add tools.

It's not split to many different packages:
  * dewi_core_
  * dewi_utils_
  * dewi_module_framework_
  * dewi_logparsers_
  * dewi_realtime_sync_
  * dewi_commands_  - which is the main package a a command-line tool

.. _dewi_core: https://github.com/LA-Toth/dewi_core
.. _dewi_utils: https://github.com/LA-Toth/dewi_utils
.. _dewi_module_framework: https://github.com/LA-Toth/dewi_module_framework
.. _dewi_logparsers: https://github.com/LA-Toth/dewi_logparsers
.. _dewi_realtime_sync: https://github.com/LA-Toth/dewi_realtime_sync
.. _dewi_commands: https://github.com/LA-Toth/dewi_commands


Installation
------------

It can be installed from source::

        python3 setup.py

Or from pip::

        pip install dewi


Usage as a command-line tool
----------------------------

Common usage
~~~~~~~~~~~~

To print its help::

        dewi -h

To print dewi_commands.commands with their descriptions::

        dewi
        dewi list

To print dewi_commands.commands with their aliases and descriptions::

        dewi list-all

An example: I want to open ~/.ssh/known_hosts at line 123, and it's
listed on the console as ~/.ssh/known_hosts:123. After copy-paste::

        dewi edit ~/.ssh/known_hosts:123

And it starts `vim` with arguments `~/.ssh/known_hosts +123`
