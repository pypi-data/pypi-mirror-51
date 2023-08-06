# sanelogging

## Sane Defaults for Python Logging

The python stdlib `logging` module is useful, flexible, and configurable.

However, the maintainers have (quite reasonably) determined that python is
an application runtime and not an application.  The default configuration
for the `logging` is thus not very useful, and this commonly results in 
boilerplate in your own programs.

This is an opinionated module for the 90% case where you just want sane
defaults without that boilerplate.  (In effect, moving it into PyPI.)

# It Also Does Some Other Stuff

* There are some convenience methods added, such as `panic` and `die` (c.f.
  golang and perl).

* `notice` is aliased to `info`, for those who forget that python
  doesn't have a notice level (i.e. me).

* If you set the environment variable `LOG_TO_SYSLOG` to something, 
  it will print out your log messages on paper and mail them to you.

* If stdout is a tty, log messages will be color-coded using the `colorlog`
  module.

# Usage

```python

from sanelogging import log

log.info("starting up!")

log.error("something went wrong.")

log.die("bailing out") # exits

print "no soup for you." # never reached

```

![example output](https://raw.githubusercontent.com/sneak/sanelogging/master/example/example.png)

Author
======

Jeffrey Paul &lt;sneak@sneak.berlin&gt;

https://sneak.berlin

[@sneakdotberlin](https://twitter.com/sneakdotberlin)

`5539 AD00 DE4C 42F3 AFE1  1575 0524 43F4 DF2A 55C2`

License
=======

This code is released into the public domain.
