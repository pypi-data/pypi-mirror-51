usage:
    kafka-cli <bootstrap-server>  -- list topics
    kafka-cli <bootstrap-server> <topic> -- describe topic
    kafka-cli <bootstrap-server> <topic> <partition> <offset> <next-number: default=1> -- query message from offset
    kafka-cli <bootstrap-server> <topic> <partition> <begin-time> <next-number: default=1> -- query message from time

examples:
    $>kafka-cli 192.168.20.211:9092 test01               
    topic: test01, partition: 0, offset: [0, 3)
    
    $>kafka-cli 192.168.20.211:9092 test01 0 1 
    2019-08-27 19:13:12.573000 ConsumerRecord(topic='test01', partition=0, offset=1, timestamp=1566904392573, timestamp_type=0, key=None, value=b'hihi', checksum=-1132288920, serialized_key_size=-1, serialized_value_size=4)
    
    $>kafka-cli 192.168.20.211:9092 test01 0 "2019-08-27 18:00:00" 2
    2019-08-27 19:08:36.798000 ConsumerRecord(topic='test01', partition=0, offset=0, timestamp=1566904116798, timestamp_type=0, key=None, value=b'hello', checksum=-367915336, serialized_key_size=-1, serialized_value_size=5)
    2019-08-27 19:13:12.573000 ConsumerRecord(topic='test01', partition=0, offset=1, timestamp=1566904392573, timestamp_type=0, key=None, value=b'hihi', checksum=-1132288920, serialized_key_size=-1, serialized_value_size=4)
    
