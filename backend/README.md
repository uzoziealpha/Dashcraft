DataCraft

DataCraft is an AI-powered platform designed to automate data analysis, content generation, and visualization. The platform leverages multiple AI agents to handle tasks such as data ingestion, query processing, content generation, and visualizations, making it easy for businesses to extract valuable insights from their data. With a dynamic dashboard, users can interact with their data in real time, receiving intelligent responses to their queries and generating useful reports.

Key Features:

	•	Data Ingestion: The system automatically processes and ingests data from various file formats, including Excel, CSV, JSON, XML, and text documents, converting them into structured formats suitable for analysis.
	•	Natural Language Query Processing: Users can ask questions in plain language, and the AI will analyze the data to generate relevant insights and provide answers.
	•	Data Visualization: The platform allows users to create charts and graphs for easy visual representation of the data, making complex information more accessible and understandable.
	•	Content Generation: The AI agents can generate essays, CVs, letters, and other content based on user input, with the ability to export the generated content to PDF or Word formats.


Technologies Used:

	•	Flask: Python web framework used for creating the API endpoints and serving the backend logic.
	•	PostgreSQL: Relational database for storing user data, file metadata, and task-related information.
	•	Machine Learning: The platform utilizes pre-trained models for natural language query processing and content generation tasks.
	•	AWS: (Planned for future use) Cloud services for data storage and processing (S3, EC2, etc.).


Getting Started:

To set up and run DataCraft locally, follow these steps:
	1.	Clone the repository:

	2.	Install dependencies:
Ensure you have Python installed, then install the required dependencies by running:
	3.	Configure PostgreSQL:
	•	Set up a PostgreSQL database (locally or in the cloud).
	•	Update the database connection details in config/settings.py to point to your database instance.
	4.	Run the application:
After configuring your you can start the Flask server by running: python app.py