#!/usr/bin/python

import time
from amqplib import client_0_8 as amqp
import logging
import logging.config
logging.config.fileConfig('logging.conf')
import jsonpickle
from outboundMessage import OutboundMessage

# create logger
log = logging.getLogger('TextResponder')

queueConn = amqp.Connection(host="localhost:5672", userid="guest", password="guest", virtual_host="/", insist=False)
queueChan = queueConn.channel()

#create outbound message queue
queueChan.queue_declare(queue="outbound_message_queue", durable=True, exclusive=False, auto_delete=False)
queueChan.exchange_declare(exchange="glucose_logs", type="direct", durable=True, auto_delete=False,)
queueChan.queue_bind(queue="outbound_message_queue", exchange="glucose_logs", routing_key="outbound_message")

while (1):
    
    message = queueChan.basic_get("outbound_message_queue")
    if message != None:
        log.info("Found Response in response_outbound")
        unpickled = jsonpickle.decode(message.body)
        outboundMessage = OutboundMessage(**unpickled)
        if outboundMessage.messageType == "sms":
            
            