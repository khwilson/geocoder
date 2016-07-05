Geocoder
--------

This package provides a simple way of polling Google's geocoding API.
In particular, it's useful when you have a *lot* of queries to make
and you'll need to use multiple API keys to code them.

How to use
==========

Install with

```bash
pip install -U git+ssh://git@github.com/khwilson/geocoder.git
```

Once installed, you'll need to create some Google API keys. Do that by going
[here](https://console.developers.google.com/flows/enableapi?apiid=geocoding_backend&keyType=SERVER_SIDE&reusekey=true).

Put them into a file. We'll call it `keys` for now.

In a separate file (called, say, `input`), create a csv in the format

```
ADDRESS,CITY,STATE,ZIP
```

of the addresses you want to geocode. Then simply call

```bash
geocode geocode keys input --ouput-file output
```

If you don't specify `output-file`, then it will print to standard out.

What do you get?
================

The output is quite raw. In particular, for every row that you have in your `input` file,
you get a row in the `output` file. This is a csv whose first column is somewhat normalized
version of the address in the input and whose second column is just the json that the
Google API returns. Further processing can be added through modifying the `geocoder/cli.py`
module or by postprocessing.

Caching
=======

If you are expecting a *lot* of duplicate addresses in your runs, then you may want to
cache your results from the API. This can be done by specifying a `--cache-file`. The
key to the cache is the semi-normalized address (so nothing fancy).

Warning
=======

This is not meant to be a super smart implementation. In particular, the cache is in memory
and so if you have lots of addresses to geocode, you probably want to change that.

But if you have that many addresses, you probably are paying Google anyway. :)
