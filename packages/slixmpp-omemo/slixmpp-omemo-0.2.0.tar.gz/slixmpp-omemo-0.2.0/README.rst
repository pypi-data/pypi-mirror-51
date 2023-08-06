Slixmpp OMEMO plugin
####################

This library provides an interface to `python-omemo <https://github.com/syndace/python-omemo>`_.

License
-------

This plugin is licensed under GPLv3.

The python-omemo library being used is a reimplementation of libsignal
in python and plans to stay away from the GPL license as possible. For
the moment, the OMEMO library has to reuse parts of the original
libsignal implementation, (the wireformat), which makes it GPL. Efforts
are being made in order to not have to reuse these libsignal bits, and
move to a more permissive license.

As long as this is not the case, this plugin will stay GPLv3 as well,
and it will not be possible to merge it without changing Slixmpp's
license itself.

Note on the underlying OMEMO library
------------------------------------

As stated in `python-xeddsa's
README <https://github.com/Syndace/python-xeddsa/blob/136b9f12c8286b9463566308963e70f090b60e50/README.md>`_,
(dependency of python-omemo), this library has not undergone any
security audits. If you have the knowledge, any help is welcome.

Please take this into consideration when using this library.

Installation
------------

- ArchLinux (AUR):
   `python-slixmpp-omemo <https://aur.archlinux.org/packages/python-slixmpp-omemo>`_, or
   `python-slixmpp-omemo-git <https://aur.archlinux.org/packages/python-slixmpp-omemo-git>`_
- PIP: `slixmpp-omemo`
- Manual: `python3 setup.py install`

Credits
-------

For the help on OMEMO:

- Syndace
- Daniel Gultsch (`gultsch.de <https://gultsch.de/>`_)

And on Slixmpp:

- Mathieu Pasquet (`mathieui@mathieui.net <xmpp:mathieui@mathieui.net?message>`_)
- Emmanuel Gil Peyrot (`Link mauve <xmpp:linkmauve@linkmauve.fr?message>`_)
