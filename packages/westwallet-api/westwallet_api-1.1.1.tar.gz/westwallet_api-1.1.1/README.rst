westwallet-python-api
=====================

westwallet-python-api is a `WestWallet Public API <https://westwallet.info/api_docs>`_ wrapper for Python programming language. Use it for building payment solutions.

Installing
----------

Install from pypi:

.. code-block:: text

    pip install -U westwallet-api


Install from latest source code (*may be unstable*):

.. code-block:: text

    pip install git+git://github.com/WestWallet/westwallet-python-api


A Simple Example
----------------

.. code-block:: python

    # Send 0.1 ETH to 0x57689002367b407f031f1BB5Ef2923F103015A32
    from westwallet_api import WestWalletAPI

    client = WestWalletAPI("your_api_key", "your_api_secret")
    sent_transaction = client.create_withdrawal(
        "ETH", 0.1, "0x57689002367b407f031f1BB5Ef2923F103015A32"
    )
    print(sent_transaction.__dict__)


Documentation
-------------
* API: https://westwallet.info/api_docs


Other languages
---------------
* JavaScript: https://github.com/WestWallet/westwallet-js-api
* Ruby: https://github.com/WestWallet/westwallet-ruby-api
* PHP: https://github.com/WestWallet/westwallet-php-api
