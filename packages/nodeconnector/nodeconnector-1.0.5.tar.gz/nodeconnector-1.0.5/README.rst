nodeconnector 
#############

Python connector module for Node.JS applications. This packages allows Python functions to be called and 
process Node.JS JSON request. This packages complements `PyConnector`_ module for Node.JS.

.. _PyConnector: https://github.com/cristidbr/pyconnector

Installation
============

Install using pip
::

    pip install nodeconnector 

Python version
--------------

Python 3.6+ is required.

Usage
=====

A simple minimal API interface can be created using the following example.
Note that handle/resolver functions are executed in a separate thread. 
Context information can be using ``nodeconnector.Interface.handle( 'query_type', resolve_function, [ ctx ] )``.

This object will be passed to all ``resolve_function`` calls and can be used to store information between queries.

.. code:: python

    # minimal.py
    import sys
    import time
    import argparse
    import nodeconnector

    # argument parsing, PyConnector automatically sends this
    parser = argparse.ArgumentParser( description = 'Python Exposed API' )
    parser.add_argument( '--pynodeport', help = 'PyConnector Node.JS query port', default = 24001 )
    args = parser.parse_args()

    # python version query
    def nodeq_version( args, ctx = {} ):
        return ( '%d.%d.%d' % ( sys.version_info[ 0 ], sys.version_info[ 1 ], sys.version_info[ 2 ] ) )

    # increment value query
    def nodeq_increment( args, ctx = {} ):
        # return value
        ctx[ 'inc' ] += 1
        args[ 'value' ] = ctx[ 'inc' ]

        return args

    # create interface
    nodeq = nodeconnector.Interface( )

    # queries are executed on a separate thread, a context object can be used to pass data
    nodeq.handle( 'pyversion', nodeq_version )
    nodeq.handle( 'increment', nodeq_increment, dict( inc = 0 ) ) 

    # launch API
    nodeq.listen( port = args.pynodeport ) 

    # wait
    while( True ):
        time.sleep( 0.001 )


License (MIT)
=============

Copyright (C) 2019 `Cristian Dobre`_ .

.. _Cristian Dobre: https://github.com/cristidbr
