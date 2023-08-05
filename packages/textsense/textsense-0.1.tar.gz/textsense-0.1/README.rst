TextSense
----------

To use, simply do::

    >>> form textsense import SERVICE
    >>> api = SERVICE(userkey)
    >>> text = 'The tea was not good. But it is better than coffee.'
    >>> api.sentiment(text)

