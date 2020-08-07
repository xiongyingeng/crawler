# -*- coding: utf-8 -*-
# @Time : 2020/6/4 10:58
# @Author : Will
# @Software: PyCharm
# kafka 消费端

from kafka import KafkaConsumer
from kafka import TopicPartition

server = "192.168.70.80:9092,192.168.70.81:9092,192.168.70.82:9092"
consumer = KafkaConsumer(group_id='group2', bootstrap_servers=server,
                         key_deserializer=bytes.decode, value_deserializer=bytes.decode,
                         enable_auto_commit=True,  # 每过一段时间自动提交所有已消费的消息（在迭代时提交）
                         auto_commit_interval_ms=5000,  # 自动提交的周期（毫秒）
                         )
if consumer.bootstrap_connected():
    print("kafka connected")
    consumer.assign([TopicPartition(topic='demo_topic', partition=0)])
    print(consumer)
    for msg in consumer:
        print(msg)
        print("topic:", msg.topic, "partition:", msg.partition, "key:", msg.key, "value:", msg.value, "offset:", msg.offset)

        # consumer.close()

    else:
        print("kafka didn't connect!!")
