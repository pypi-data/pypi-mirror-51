#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest

import pykafka


sys.path.append('..')

from kafka_client import KafkaConnector 
from kdbase.log import *


class TestKafkaConnector(unittest.TestCase):

    def setUp(self):
        self.hosts = 'dev-01:9092,dev-02:9092,dev-03:9092'
        log_init('info', './unittest.log.txt', quiet=False)

    def test_get_client(self):
        client = KafkaConnector(self.hosts).get_client()
        self.assertIsNotNone(client)
        self.assertIsInstance(client, pykafka.client.KafkaClient)

    def test_get_all_topics(self):
        topics = KafkaConnector(self.hosts).get_all_topics()
        self.assertIsInstance(topics, pykafka.cluster.TopicDict)
        self.assertGreater(len(topics), 0)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0],])
