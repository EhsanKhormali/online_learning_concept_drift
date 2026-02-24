import os
import json
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common import Configuration
from river import linear_model, metrics, preprocessing, drift
from river import utils 

class OnlineLearner:
    def __init__(self):
        # Initialize the model, metric, and drift detector
        self.init_model()
        self.metric = utils.Rolling(metrics.Accuracy(), window_size=50)
        # ADWIN (Adaptive Windowing) is a standard for drift detection in research
        self.drift_detector = drift.ADWIN(delta=0.01)

    def init_model(self):
        """Helper to (re)initialize the model weights."""
        self.model = preprocessing.StandardScaler() | linear_model.LogisticRegression()

    def process(self, value):
        data = json.loads(value)
        # Extract metadata if provided by producer_drift.py, else default to 'Stream'
        phase = data.pop('phase', 'Stream')
        y = data.pop('label')
        x = data
        
        # 1. Prequential Evaluation (Predict before Learning)
        y_pred = self.model.predict_one(x)
        
        if y_pred is not None:
            # 2. Check for Drift 
            # We monitor the 'error' (0 = correct, 1 = wrong)
            error = 1 if y_pred != y else 0
            self.drift_detector.update(error)
            
            if self.drift_detector.drift_detected:
                print(f"\n[ALERT] Drift Detected in {phase}! Resetting model weights...\n")
                self.init_model()  # Reset the model to adapt faster to the new rule
            
            # 3. Update Performance Metric
            self.metric.update(y, y_pred)
            
        # 4. Incremental Learning update
        self.model.learn_one(x, y)
        
        return f"[{phase}] Pred: {y_pred} | Actual: {y} | Cumulative Acc: {self.metric.get():.4f}"

def run_pipeline():
    # 1. Setup Configuration for Web UI (localhost:8081)
    config = Configuration()
    config.set_string("rest.address", "localhost")
    config.set_string("rest.port", "8081")
    
    env = StreamExecutionEnvironment.get_execution_environment(config)
    env.set_parallelism(1)
    
    # 2. Add your specific JAR location
    jar_path = "file:///home/ehsan/Downloads/flink-sql-connector-kafka-4.0.1-2.0.jar"
    env.add_jars(jar_path)

    

    # 3. Configure Kafka Source
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers("localhost:9092") \
        .set_topics("input_topic") \
        .set_group_id("research_group") \
        .set_starting_offsets(KafkaOffsetsInitializer.latest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    learner = OnlineLearner()
    
    # 4. Define DataStream
    ds = env.from_source(
        source=kafka_source, 
        watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(), 
        source_name="Kafka Source"
    )
    
    # 5. Map logic and Print output
    ds.map(lambda msg: learner.process(msg)).print()
    
    # 6. Start Execution
    env.execute("Online Learning with Drift Detection")

if __name__ == '__main__':
    run_pipeline()