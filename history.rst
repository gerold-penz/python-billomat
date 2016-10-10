##################################
Python Billomat API Client Library
##################################

by Gerold Penz 2014-2016


=============
Version 0.5.2
=============

2016-10-10

- Credit-Note-Tags added


=============
Version 0.5.1
=============

2016-10-05

- Credit-Notes added

- Credit-Note-Items added


=============
Version 0.5.0
=============

2016-05-19

- Invoice-Items: Now it is possible to fetch the invoice items for more then
  one invoice with one request.

  The parameter *invoice_id* for the search can now contain a list of invoice ids.
  If list with IDs given: The result contains the invoice-items of
  many invoices. Be careful: Too many invoice IDs can produce to
  large responses or to large SQL statements.
  My recommendation: 10-50 invoice IDs at one time.

- Recurring-Items: Now it is possible to fetch the recurring items for more then
  one recurring with one request.

  The parameter *recurring_id* for the search can now contain a list of recurring ids.
  If list with IDs given: The result contains the recurring-items of
  many recurrings. Be careful: To many recurring IDs can produce to
  large responses or to large SQL statements.
  My recommendation: 10-50 recurring IDs at one time.


=============
Version 0.4.5
=============

2016-05-05

- Merged pull request #3 from Femaref/feature/add_locale_to_clients

  Thank you Femaref! Handling for the locale api argument.


=============
Version 0.4.4
=============

2015-08-20

- Added a timeout for HTTP requests. Default timeout is 10 minutes.


=============
Version 0.4.3
=============

2015-07-06

- Own meta data (customfield) for every Billomat-object


=============
Version 0.4.2
=============

2015-06-25

- Suppliers


=============
Version 0.4.1
=============

2015-05-29

- *Contacts*: merged pull request #2 from *flow90*. Thank you! :-)


=============
Version 0.4.0
=============

2015-05-06

- *invoice_tags*: Bug repaired: Next page search with *order_by* parameter.

- *invoice_payments*

- Status changed from "alpha" to "beta".


==============
Version 0.3.11
==============

2015-04-13

- *_items_base.Item* um Properties für "id" erweitert.


==============
Version 0.3.10
==============

2015-04-13

- Reminder-Items

- Reminder-Texts


=============
Version 0.3.9
=============

2015-04-09

- Reminder-Tags


=============
Version 0.3.8
=============

2015-03-25

- Reminders:

  - Get a single reminder

  - Create reminder

  - Edit reminder

  - Delete reminder

  - Complete reminder

  - Send reminder by e-mail


=============
Version 0.3.7
=============

2015-03-12

- Small bug fixed: Double "article_number" in *articles.Articles.search*.

- Mit Mahnungen (reminders) begonnen.


=============
Version 0.3.6
=============

2015-03-02

- Client-Properties: New "value"-parameter added for searching.


=============
Version 0.3.5
=============

2015-02-12

- Articles


=============
Version 0.3.4
=============

2015-01-29

- Catch ZeroDivisionError on calculating *self.pages*.


=============
Version 0.3.3
=============

2015-01-20


- Recurring-Email-Receivers

- Bug repaired: OrderBy-Field error in *Clients.search*

- Email-Templates


=============
Version 0.3.2
=============

2015-01-19

- Recurrings: New field *email_template_id* added


=============
Version 0.3.1
=============

2015-01-11

- Now, items will load automatically if the ID is given on initializing
  the item-object. No more ``<item>.load()`` is necessary.

- Typo


==============
Version 0.2.14
==============

2015-01-08

- Invoice-Tags

- Invoice-Items

- Create invoice

- Edit invoice


==============
Version 0.2.13
==============

2015-01-02

- Unused parameter *recurring_items*, for creation of one recurring, removed.


==============
Version 0.2.12
==============

2015-01-02

- "Row not found"-Error raises *pybillomat.errors.NotFoundError*

- Recurring-Tags

- Internal renamings


==============
Version 0.2.11
==============

2014-12-23

- Item-class bound to Invoice-class

- Item-class bound to Client-class

- Item-class bound to ClientTag-class

- Item-class bound to ClientProperty-class

- Item-class bound to ArticleTag-class

- *RecurringItems* finished


==============
Version 0.2.10
==============

2014-12-23

- New Base-Class for "items" created.

- Item-class bound to RecurringItem-class

- Item-class bound to Recurring-class

- *_tools.py*-module renamed to *_items_base.py*


=============
Version 0.2.9
=============

2014-12-19

- Begun, programming the recurring-module

- *ItemsIterator*-base class

- *RecurringsIterator*-class

- Global use of *ItemsIterator*-base class

- Create recurrings

- Edit recurrings

- Delete recurrings


=============
Version 0.2.8
=============

2014-12-01

- Article-Tags

- Client delete

- Client edit


=============
Version 0.2.7
=============

2014-12-01

- Article-Properties


=============
Version 0.2.6
=============

2014-12-01

- Client-Tags


=============
Version 0.2.5
=============

2014-11-19

- The new class-method *pybillomat.ClientProperty.create()* creates one new
  client-property-value.


=============
Version 0.2.4
=============

2014-11-19

- Client-Property-Values

  - ClientProperty- and ClientProperties-Classes allow
    to get one clients-property or search for clients-properties.

  - If the requested client is not accessable (Unothorized), the
    NotFoundError will raised.

  - ClientPropertiesIterator-Class finished

- All searches: New parameter *order_by*

- Better examples created


=============
Version 0.2.3
=============

2014-11-18

- The new class-method *clients.Client.create()* creates one new client.


=============
Version 0.2.2
=============

2014-11-10

- Invoices: Default value for *per_page* is 100


=============
Version 0.2.1
=============

2014-10-29

- 60 seconds deadline for Google App Engine Requests

- Sending of invoice-e-mails


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

