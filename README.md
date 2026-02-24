# Real-Time Online Learning with Apache Flink & Kafka

This repository contains a Python-based implementation of online learning algorithms designed for stateful distributed stream processing. The project focuses on high-throughput data ingestion and low-latency model updates.

## ## Tech Stack & Versions

To ensure reproducibility and stability, this project uses the following specific versions:

* **Python:** `3.11.14`
* **Apache Flink:** `2.2.0`
* **Message Broker:** **Apache Kafka**
* **OS Environment:** Linux (Ubuntu recommended)

---

## ## Project Overview

The system implements a stream processing pipeline where data is ingested from Kafka, processed via Flink for online learning (meta-learning or Bayesian optimization tasks), and results are synced back to downstream consumers.

### ### Key Features
* **Stateful Processing:** Leverages Flink's managed state for persistent model parameters.
* **Online Learning:** Incremental model updates without requiring full batch retraining.
* **Scalability:** Distributed architecture capable of handling high-velocity streams.

---

## ## Getting Started

### 1. Prerequisites
Ensure you have a running Kafka cluster and an Apache Flink 2.2.0 cluster environment.

### 2. Environment Setup
We recommend using a virtual environment or Conda to manage the specific Python version:

```bash
# Create environment
conda create -n online-learning python=3.11.14
conda activate online-learning

# Install core dependencies
pip install apache-flink==2.2.0 confluent-kafka
```

### 3. Kafka Configuration
Create the necessary topics before running the script:
```bash
kafka-topics.sh --create --topic input-stream --bootstrap-server localhost:9092
kafka-topics.sh --create --topic model-outputs --bootstrap-server localhost:9092
```

---

## ## Usage

Run the main stream processing script using the following command:

```bash
python main.py --broker localhost:9092 --flink-manager localhost:8081
```

> **Note:** Ensure your Flink configuration (`flink-conf.yaml`) is optimized for stateful processing if you are performing zero-execution tuning or complex Bayesian updates.

---

## ## Contributing

Contributions are welcome. Please ensure that any additions maintain compatibility with Python 3.11.14 and include type hints for better code clarity.

---

**License**
Distributed under the MIT License.
