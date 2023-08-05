#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Kafka Connector. 

connect kafka using kafka bootstrap hosts.
"""

import sys
from pykafka import KafkaClient


class KafkaConnector():
    
    def __init__(self, hosts):
        self.client = KafkaClient(hosts=hosts) 

    def get_client(self):
        return self.client

    def get_all_topics(self):
        return self.client.topics



