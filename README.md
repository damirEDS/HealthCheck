# healthcheck_bot


## Project Description

This project performs health checks on a remote server and sends the results to a Telegram channel using the Telegram Bot API.

## Prerequisites

- Python 3.6+
- Docker (if running the application in a Docker container)

## Installation

1. Clone the repository:

   ```shell
    https://github.com/damirEDS/HealthCheck.git 
2. Change to the project directory:
   ```
    cd HealthCheck
3. Install the required Python packages:
    ```
    pip install -r requirements.txt

## Usage
1.Set up a Telegram bot and obtain the bot token.You can chat with the BotFather bot using the /token command.
    ```
    https://telegram.me/botfather


2.Edit the Health_check.py file and replace the placeholder values with your own Telegram bot token and chat ID:

    
    API_TOKEN = 'YOUR_BOT_TOKEN'
    CHAT_ID = 'YOUR_CHAT_ID'
3.Run the health check script:

    
    python Health_check.py

4. (Optional) To run the application in a Docker container:

    docker build -t health-check
    docker run -d health-check

## Configuration

You can customize the behavior of the health check script by modifying the following variables in the Health_check.py file:

URL: The URL of the remote server to perform the health check.
API_TOKEN: Your Telegram bot token.
CHAT_ID: Your Telegram chat ID.

## Testing
To run the unit tests, execute the following command:
    
    python test_telegram.py



