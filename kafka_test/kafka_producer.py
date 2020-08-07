# -*- coding: utf-8 -*-
# @Time : 2020/6/4 10:57
# @Author : Will
# @Software: PyCharm
# kafka 生产端

from kafka import KafkaProducer

server = "192.168.70.80:9092,192.168.70.81:9092,192.168.70.82:9092"
producer = KafkaProducer(bootstrap_servers=server, key_serializer=str.encode, value_serializer=str.encode)
if producer.bootstrap_connected():
    print("kafka connected!!")
    future = producer.send(topic='demo_topic', key='demo', value='hello kafka', partition=0)
    producer.flush()
    result = future.get(30)
    print(result)

    producer.close()
else:
    print("kafka didn't connect!!")
