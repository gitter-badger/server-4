============
Introduction
============

Argux is a monitoring framework that is designed to work slightly
different from most monitoring applications that you'll find on the
web. It is designed with the following aspects in mind.

.. NOTE::
   Argux is still under heavy development, some of the statements below
   might still be a bit 'optimistic'. (eg. they will be true once there
   is a release) - These remarks also count as reminders to what it is
   that is being developed.

**Decentralisation**
   In short, most of the time you are not interested in ping times 
   from your monitoring host to server X.
   You are interested in ping times from the offices in Paris and
   Madrid to the server in Berlin.

**REST API**
   It is impossible to prepare for any scenario of hosts or services that
   require monitoring. Therefor it is important that the interface to
   Argux is clear and easy to use. It will have client API's in several
   programming languages, but if all else fails you could control it
   with ``CURL``.

   The REST API is the center of the application, it is meant for use by
   external scripts but it is also used internally and as backend to the
   Web-interface.

**Encryption**
   Since Argux is using basic HTTP requests, you can simply configure
   your favourite reverse-proxy or SSL terminator to run all traffic via
   HTTPS instead of plain HTTP.

**Authorisation**
   All requests to Argux require authentication. A user is allowed to
   write metrics of one host, or many. Or is only allowed to read
   information.

   Example 1:
      Basically, I only trust the user 'postgres' on the database-server to
      store any posgres related information.

   Example 2:
      An agent running on server X is not able to save metrics about
      server Y, unless is is explicitly allowed.
