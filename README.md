# ehliyet_bot
This script automates the process of logging into the Kanto Motor School's website for making reservations, fetching calendar data, checking for available time slots, and sending notifications via the Line API for any newly available time slots.

## Prerequisites

- Python 3
- Required Python packages: `requests`, `beautifulsoup4`, `linebot`

## Installation

1. Clone the repository or download the script.
2. Install the required packages using pip:

## Configuration

1. Obtain the necessary credentials and access tokens:

- You need to be enrolled in Kanto Motor School to get an student id and your password.
- Line API Access Token: Follow the Line API documentation to create a new channel and obtain an access token.

2. Open the script file and modify the following variables:

- `user_id`: Your login username or ID.
- `user_pass`: Your login password.
- `access_token`: The Line API access token.

## Usage

1. Run the script:
2. The script will log in to the website, fetch calendar data, check for available time slots, and send Line messages for any newly available slots.

## Example

Here's an example usage of the script:

1. Set up the necessary credentials and access tokens in the script.
2. Run the script using the command:
3. The script will periodically check for available time slots and send Line messages for any new slots found.

## Troubleshooting

If you encounter any issues or errors while running the script, consider the following:

- Check your internet connection.
- Ensure that the provided credentials and access tokens are correct.
- Make sure you have the required permissions and access to the website and Line API.
