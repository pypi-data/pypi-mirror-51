#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kdbase.log import * 

from base.timer import time_wrapper
from kafka_client import get_client, get_all_topics


class KafkaConsumer():

    def __init__(self, topic, balanced=True):
        client = get_client()
        self.topic = client.topics[topic]
        self.consumer = None
        self.get_consumer = self._get_balanced_consumer if balanced else self._get_simple_consumer

    def consume(self):
        pass

    @time_wrapper(logger().debug)
    def _get_simple_consumer(self, 
            consumer_group=None,
            partitions=None,
            auto_commit_enable=False,
            auto_commit_interval_ms=60000,
            offsets_commit_max_retries=5): 
        self.consumer = self.topic.get_simple_consumer(consumer_group)

    @time_wrapper(logger().debug)
    def _get_balanced_consumer(self,
            consumer_group=None,
            partitions=None,
            auto_commit_enable=False,
            auto_commit_interval_ms=60000,
            offsets_commit_max_retries=5): 
        self.consumer = self.topic.get_balanced_consumer(consumer_group)

