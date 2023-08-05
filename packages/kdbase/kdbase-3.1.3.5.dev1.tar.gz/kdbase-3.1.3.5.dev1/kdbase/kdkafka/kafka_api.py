#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" kafka APIs.

invoked by upper layer.
invoking operations of kafka.
"""

from kafka_producer import KafkaProducer


def get_producer(hosts, topic, 
            sync=False, 
            partitioner=None, 
            max_retries=3, 
            required_acks=1, 
            delivery_reports=False
            ):  
    return KafkaProducer(hosts, topic, 
            sync=sync, 
            partitioner=partitioner,
            max_retries=max_retries,
            required_acks=required_acks,
            delivery_reports=delivery_reports
            )


def produce(kafka_producer, msg):
    assert isinstance(kafka_producer, KafkaProducer)
    return kafka_producer.produce(msg)

