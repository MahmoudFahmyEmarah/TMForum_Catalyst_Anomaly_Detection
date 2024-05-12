Project Title: LLM based Order Anomaly Detection

Description:

This repository contains the source code for a robust Complaint Prediction and Validation System designed to classify and predict potential customer complaints from order details. Utilizing Kafka for real-time data streaming, the system processes order completion messages to predict the likelihood of a complaint, leveraging the open-source llama3 model for inference. The workflow includes consuming Kafka topics, processing data, interacting with external APIs to fetch and verify order details, and producing outcomes to another Kafka topic based on the analysis. The system is structured to facilitate easy maintenance and scalability.

Key Features:

Real-time Data Streaming: Uses Kafka to consume and produce messages pertaining to order completion and complaint predictions.
Data Processing: Includes modules for transforming and preparing data for prediction.
Machine Learning Inference: Utilizes the llama3 model to predict potential complaints based on order characteristics and historical data.
API Integration: Communicates with external APIs to validate order details against catalog items.
Error Handling and Logging: Robust error handling and detailed logging to ensure reliability and ease troubleshooting.
Technologies Used:

Kafka for message streaming.
Python for backend processing.
Llama3 for machine learning inference.
Pandas for data manipulation.
Requests for HTTP requests handling.
