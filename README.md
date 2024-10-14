# Challenge - News Content Collect and Store

In this project, I was challenged to develop a complete application that scrapes articles from The Guardian's website, processes and stores the data in Google BigQuery, and provides an API built with FastAPI for querying the collected data.

## The key concepts and principles applied include:

- **Asynchronous Programming with asyncio and aiohttp** to efficiently handle I/O-bound operations during web scraping.
- Use of the **Factory Pattern** to create instances of scrapers and manage processing and transformations. This ensures better code maintainability and facilitates scalability by allowing easy adaptation to incorporate additional data sources.
- Application of **SOLID Principles** to enhance modularity and separation of concerns, promoting cleaner and more maintainable code.

## Technologies Used

* **Python 3.9**
* **FastAPI** : Framework for building APIs with Python.
* **Uvicorn** : A lightning-fast ASGI server used to run the FastAPI application.
* **Google Cloud BigQuery** : Data Warehouse.
* **aiohttp e asyncio** : Libraries for asynchronous HTTP clients and servers, enabling non-blocking I/O operations.
* **Pandas** : Data analysis and manipulation.
* **Docker** : A platform for developing, shipping, and running applications inside containers.
* **Docker Compose** : A tool for defining and running multi-container Docker applications.
* **YAML** : Used for configuration files.
* **db-dtypes** : A package providing support for BigQuery data types when using Pandas.

## Requirements

* **Docker** and **Docker Compose** installed on the system.
* A **Google Cloud Platform** account with access to **BigQuery**.
* **Google Cloud credentials** saved in `./credentials/your_credentials.json`.

## How to Run the Project

1. Step 1: Build the Docker Image

In the project’s root directory, run:

`docker-compose build`

2. Step 2: Start the Services

`docker-compose up`

3. Step 3: Access the API

`http://localhost:8000/api/articles`

`http://localhost:8000/api/articles?keyword=peacekeeping`

## Contact

For more information or questions, please contact:

Name: Guilherme Carvalho
Email: guilhermerdcarvalho@gmail.com
LinkedIn: [https://www.linkedin.com/in/devguilhermecarvalho/]()
