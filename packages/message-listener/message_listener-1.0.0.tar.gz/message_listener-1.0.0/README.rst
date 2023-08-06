What it is
===========
App used at Raspberry Pi as receiver of incoming messages and pass them to registered handlers 
(relay, screen, sensors) 

.. code-block::

    from message_listener.server import Server
    from iot_message.message import Message
    from message_listener.handler_debug import HandlerDebug
    from iot_message.cryptor.base64 import Cryptor as B64

    Message.node_name = "PC"
    Message.add_decoder(B64())
    #Message.drop_unencrypted = True

    svr = Server()
    # svr.ignore_missing_decoders = False
    svr.add_handler('NodeOne', HandlerDebug({}))
    svr.start()

Initialization:

.. code-block::

    __init__(self, port=5053, ip_address='0.0.0.0', buffer_size=65535)
    
Read more: 

[https://koscis.wordpress.com/2017/03/03/raspberry-pi-as-a-node/](https://koscis.wordpress.com/2017/03/03/raspberry-pi-as-a-node/)

[https://koscis.wordpress.com/2019/08/31/upgrades-to-message_listener/](https://koscis.wordpress.com/2019/08/31/upgrades-to-message_listener/)



