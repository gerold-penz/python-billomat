##################################
Python Billomat API Client Library
##################################

by Gerold Penz 2014


=============
Version 0.2.0
=============

2014-10-28

- Google App Engine enabled


=============
Version 0.1.5
=============

2014-10-28

- *ClientsIterator* is a new class which allows to iterate over all clients. The
  clients will load gradually.

- *__getitem__* implemented: Now it is possible to iterate over slices of clients.

- Examples added


=============
Version 0.1.4
=============

2014-10-28

- Structure of *clients* reassembled


=============
Version 0.1.3
=============

2014-10-27

- Http-module extended with methods for *get*, *post*, *put* and *delete*

- Draft-Invoices can now completed

- Errors-module extended

- Structure of *invoices* reassembled


=============
Version 0.1.2
=============

2014-10-27

- Invoices-module added.

- Errors-module added.

- The new parameter *allow_empty_filter* prevents fetching all records.

- It's now possible to fetch single pages


=============
Version 0.1.1
=============

2014-10-26

- Tests with *urllib3*

- Connection-module added. It uses *urllib3* to connect to Billomat.

- Clients-module added.

- *http.Url* helper-class added

- Clients-search finished

- Now, all clients can requested (really all).


=============
Version 0.0.2
=============

2014-10-26

- Licenses added


=============
Version 0.0.1
=============

2014-10-26

- Initialy imported

