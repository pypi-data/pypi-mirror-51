#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Kafka Producer.

mainly apply async mode.
"""

import sys
import time

from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable

from kafka_client import KafkaConnector 


class KafkaProducer():

    def __init__(self, hosts, topic, 
            sync=False, 
            partitioner=None, 
            max_retries=3, 
            required_acks=1, 
            delivery_reports=False
            ):
        client = KafkaConnector(hosts).get_client()
        self.topic = client.topics[topic]
        self.sync = sync
        self.partitioner = partitioner 
        self.max_retries = max_retries 
        self.required_acks = required_acks 
        self.delivery_reports = delivery_reports 
        self.producer = None

    def produce(self, msg, partition_key=None):
        if not self.producer:
            self.get_producer()

        self._produce(msg, partition_key)

    def get_producer(self):
        self.producer = self.topic.get_producer(
                sync=self.sync,
                partitioner=self.partitioner,
                max_retries=self.max_retries,
                required_acks=self.required_acks,
                delivery_reports=self.delivery_reports)

    def _produce(self, msg, partition_key):
        try:
            self.producer.produce(msg, partition_key=partition_key)
        except (SocketDisconnectedError, LeaderNotAvailable) as e:
            self.get_producer()
            self.producer.stop()
            self.producer.start()
            self.producer.produce(msg, partition_key=partition_key)
        
    def close(self):
        self.producer.stop()


