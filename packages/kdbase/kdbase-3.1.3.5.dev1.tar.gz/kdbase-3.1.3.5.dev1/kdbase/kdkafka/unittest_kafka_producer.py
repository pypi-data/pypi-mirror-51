#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest

import pykafka

sys.path.append('..')

from kdbase.log import *

from kafka_producer import KafkaProducer


class TestKafkaProducer(unittest.TestCase):

    def setUp(self):
        log_init('debug', './unittest.log.txt', quiet=False)

        self.topic = 'kafka-store-dev'
        self.hosts = 'dev-01:9092,dev-02:9092,dev-03:9092'
        self.sync = False
        self.partitioner = None
        self.max_retries = 3
        self.required_acks = 1
        self.delivery_reports = False

    def test_produce_async(self):
        self.kafka_producer = KafkaProducer(
                self.hosts,
                self.topic,
                sync=self.sync,
                partitioner=self.partitioner,
                max_retries=self.max_retries,
                required_acks=self.required_acks,
                delivery_reports=self.delivery_reports
                )
        import  random

        users = ['Tom', 'Vincent', 'Jack']
        for i in range(10000):
            msg = 'user: %s, score: %s' % (
                    random.choice(users), random.random()) 
            res = self.kafka_producer.produce(msg)
            logger().info('produced msg: %s, res: %s', msg, res)

    def tearDown(self):
        self.kafka_producer.close()


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0],])
