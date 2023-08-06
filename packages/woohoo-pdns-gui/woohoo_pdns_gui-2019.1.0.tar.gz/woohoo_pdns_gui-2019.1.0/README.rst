Woohoo pDNS GUI
===============

Simple webapplication that can query and display pDNS data delivered from a server that produces
data according to the
`Common Passive DNS Output Format <http://tools.ietf.org/html/draft-dulaunoy-dnsop-passive-dns-cof-01>`_.

To run, I currently use the following command:
::

    $ LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 FLASK_APP=woohoo_pdns_gui FLASK_ENV=production WOOHOO_PDNS_GUI_SETTINGS="pdns_gui_dev_conf.py" flask run

Learn more `on Read the docs <https://woohoo-pdns-gui.readthedocs.io>`_ (do
not try to read the documentation in the ``docs`` folder).

The source code can be found in `woohoo pDNS GUI's home on Gitlab`_ (link
mainly for people reading this on PyPI).

.. _`woohoo pDNS GUI's home on Gitlab`: https://gitlab.com/scherand/woohoo-pdns-gui
