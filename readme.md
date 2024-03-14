# Versatile Preloader Script

The Versatile Preloader Script efficiently preloads web pages into cache by fetching URLs from a specified API endpoint and accessing each URL. This script is highly configurable, supports customizable HTTP headers for requests, and is designed for improving site performance by pre-caching content.

## Features

- Dynamic URL Fetching: Fetches URLs from a specified API endpoint.
- Customizable HTTP Headers: Supports sending custom HTTP headers.
- Configurable Preloading Intervals: Allows setting intervals for running preloading tasks.
- Advanced Error Handling: Implements retry mechanisms for reliability.
- Logging Mechanism: Provides detailed logs for monitoring and debugging.
- Optional Progress Bar: Visual feedback through an optional progress bar.
- Docker Support: Facilitates easy deployment across environments.

## Requirements

- Python 3.6+
- Dependencies: `python-dotenv`, `requests`, `schedule`, `tqdm`
- Docker (optional for Docker-based deployment)

## Installation and Setup

### Standard Installation

1. Clone the repository: `git clone https://github.com/amdiakhate/preloader.git`
2. Install required dependencies: `pip install -r requirements.txt`

### Docker Installation

1. Build Docker image: `docker build -t versatile-preloader .`
2. Run Docker container: `docker run versatile-preloader`

## Configuration

Configure the script using environment variables, through a `.env` file, or Docker configurations.

- `API_URL`: API endpoint URL returning URLs to preload.
- `CUSTOM_HEADERS`: Custom headers for requests, formatted as `Header1=Value1,Header2=Value2;...`.
- `PRELOAD_INTERVAL`: Interval in minutes for running the preloading task.
- `DISABLE_TQDM`: Set to `True` to disable the progress bar, useful for non-interactive environments.

Example `.env` file:

```
API_URL=http://localhost:8300/api/categories/listing?per_page=100
API_CUSTOM_HEADERS=X-Channel=front_fr,X-Locale=fr
FRONTEND_CUSTOM_HEADERS=X-Channel=front_fr,X-Locale=fr
PRELOAD_INTERVAL=15
DISABLE_TQDM=False
```

For Docker, specify these variables in your `Dockerfile` or `docker-compose.yml`.

## Usage

### Standard Usage

Run the script: `python preloader.py`

### Docker Usage

Run your container directly or use Docker Compose: `docker-compose up`

 
