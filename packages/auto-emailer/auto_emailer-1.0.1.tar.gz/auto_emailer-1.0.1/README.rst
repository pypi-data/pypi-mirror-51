auto-emailer
============

|Build Status| |GitHub| |Maintenance|

A wrapper library around python's SMTP (Simple Mail Transfer Protocol) and email
libraries for making emails easier. Python makes sending email relatively easy
via the smtplib module, but this library makes it even *easier* with
auto-configuration and email templates.

Table of Contents
-----------------

1.  `Background <#background>`__
2.  `Install <#install>`__
3.  `Usage <#usage>`__
4.  `Docs <#docs>`__
5.  `Maintainers <#maintainers>`__
6.  `Contributing <#contributing>`__
7.  `License <#license>`__

Background
----------

Let's say you’re automating a task that takes a couple of hours to do,
and you don’t want to go back to your computer every few minutes to
check on the program’s status. Instead, you can use auto-emailer to send
a friendly email programmatically when it’s done—freeing you to focus on
more important things while you’re away from your computer.

What if you have a spreadsheet of email addresses and you need to send
out an email to each one? Instead of manually writing hundreds, or even
thousands, of emails, you just write a few lines of code to auto-mate
the process and you're done.

Installing
----------

You can install using `pip`_::

    $ pip install auto-emailer

.. _pip: https://pip.pypa.io/en/stable/

For more information on setting up auto-emailer, please refer to `Docs <#docs>`__

Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^

Python >= 3.6

Docs
----

auto-emailer python library has usage and reference documentation at
`auto-emailer.readthedocs.io <https://auto-emailer.readthedocs.io>`_.

Maintainers
-----------

`@adamstueckrath <https://github.com/adamstueckrath>`__

Contributing
------------

Feel free to dive in! `Open an
issue <https://github.com/adamstueckrath/auto-emailer/issues/new>`__ or
submit PRs.

auto-emailer follows the `Contributor
Covenant <https://www.contributor-covenant.org/version/1/4/code-of-conduct.html>`__
Code of Conduct.

License
-------

`MIT <https://github.com/adamstueckrath/auto-emailer/blob/master/LICENSE.txt>`__ © Adam Stueckrath

.. |Build Status| image:: https://travis-ci.org/adamstueckrath/auto-emailer.svg?branch=master
   :target: https://travis-ci.org/adamstueckrath/auto-emailer
.. |GitHub| image:: https://img.shields.io/github/license/adamstueckrath/auto-emailer
   :target: https://github.com/adamstueckrath/auto-emailer/blob/master/LICENSE.txt
.. |Maintenance| image:: https://img.shields.io/maintenance/yes/2019
   :target: https://github.com/adamstueckrath/auto-emailer/graphs/commit-activity
