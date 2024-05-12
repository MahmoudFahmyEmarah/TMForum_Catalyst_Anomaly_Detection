# LLM based Order Anomaly Detection

## Project Overview

This repository hosts the Complaint Prediction and Validation System, a sophisticated solution designed to predict potential customer complaints based on order details. The system integrates Kafka for real-time message streaming, employs the open-source llama3 model for predictive analytics, and ensures data accuracy through external API interactions. It's structured for scalability and maintainability, equipped with robust error handling and logging functionalities.

## Key Features

- **Real-Time Data Streaming:** Utilizes Kafka for consuming and producing messages related to order transactions and complaint predictions.
- **Data Processing:** Implements modules for data extraction and transformation to prepare inputs for predictive modeling.
- **Machine Learning Inference:** Uses the llama3 model to assess the likelihood of customer complaints based on current and historical data.
- **API Integration:** Verifies order details against product catalogs through external API calls.
- **Error Handling and Logging:** Incorporates comprehensive error handling and detailed logging to aid in troubleshooting and system monitoring.

## Technologies Used

- **Kafka:** For messaging and real-time data streaming.
- **Python:** For backend logic and data processing.
- **Llama3 Model:** For generating predictive insights.
- **Pandas:** For data manipulation and analysis.
- **Requests:** For handling HTTP requests.

## Installation

To set up the project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/MahmoudFahmyEmarah/TMForum_Catalyst_Anomaly_Detection.git

