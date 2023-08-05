# -*- coding:utf-8 -*-
# pylint: disable=W0703

""" kafka_utils 

"""


import os
from kdkafka import kafka_api


KAFKA_PRODUCERS = {}


def _get_kafka_producer(hosts, topic):
    key = '%s:%s' % (topic, os.getpid())
    if key not in KAFKA_PRODUCERS:
        KAFKA_PRODUCERS[key] = kafka_api.get_producer(hosts, topic) 
    return KAFKA_PRODUCERS[key]


def kafka_produce(hosts, topic, value):
    producer = _get_kafka_producer(hosts, topic)
    kafka_api.produce(producer, value)
    return True

    

