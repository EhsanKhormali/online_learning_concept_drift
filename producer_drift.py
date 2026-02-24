from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Streaming data with Concept Drift...")
counter = 0

while True:
    x1 = random.uniform(-1, 1)
    x2 = random.uniform(-1, 1)
    
    # Phase 1: Original Logic (Sum > 0)
    if counter < 500:
        label = 1 if (x1 + x2) > 0 else 0
        phase = "NORMAL"
    # Phase 2: Concept Drift (The rule flips! Now x1 must be > 0.5)
    else:
        label = 1 if x1 > 0.5 else 0
        phase = "DRIFT"
    
    data = {"x1": x1, "x2": x2, "label": label, "phase": phase}
    producer.send('input_topic', data)
    
    counter += 1
    if counter == 500:
        print("!!! CONCEPT DRIFT OCCURRING NOW !!!")
        
    time.sleep(0.1)