# Google Search and OpenAI Integration Demo

This project demonstrates the power of combining Google Search and OpenAI's GPT engine to generate accurate and up-to-date information from the top search results. By leveraging the extensive search capabilities of Google and the natural language processing of OpenAI, this demo aims to provide users with relevant information that is both current and reliable.

*Key features of this project include*:

- Google Search integration
- OpenAI API integration
- Prompt engineering techniques
- Flask-based REST API for seamless frontend-backend communication

One of the main limitations of the OpenAI GPT is that it is only trained on data till Sept 2021 and so it cannot answer the questions happened after that. Here, we utilise google search API to get updated results and then use openai to generate prompts resulting in updated and concise information with source.

GPT-4 Sample output

![GPT-4 Sample output](gpt4_output.jpg)

Google Integrated Sample Output

![GPT3.5 integrated with Google Sample ouput](new_ui_out.jpg)

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Further Reading](#further-reading)

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python 3.6 or higher
- Flask
- googlesearch-python
- BeautifulSoup
- Node.js (for serving the frontend). You can install from [here](https://nodejs.org/en/download/).
- An OpenAI API key (Sign up for an account at [OpenAI](https://beta.openai.com/signup/) and obtain an API key)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Sreekiranar/GPT_enabled_google_ui
    cd cd GPT_enabled_google_ui
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Install the `http-server` package for serving the frontend:

    ```bash
    npm install -g http-server
    ```

## Configuration

Update the `app.py` file with your OpenAI API key:

```python
import os
import openai

# Configure the OpenAI API
openai.api_key = "enter-your-api-key"
```

Replace `enter-your-api-key` with your actual OpenAI API key.

## Usage

- Start the Flask server:

    ```python
    python app.py
    ```

- In a separate terminal, navigate to the project's directory and start the frontend server:

    ```bash
    http-server -p 8000
    ```

- Open your browser and navigate to <http://localhost:8000>. You should see the UI where you can enter a text prompt, submit it, and view the prompt and the response from the OpenAI API.

## Project Structure

- app.py: The Flask server that communicates with the OpenAI API.
- index.html: The HTML file for the frontend UI.
- styles.css: The CSS file for styling the frontend UI.
- main.js: The JavaScript file for handling user input and interaction with the Flask server.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).

## Further Reading

This project can be used as a foundation for the connectivity and you can modify it to solve multiple problems. In this example, I've just scraped the first three results and tried to find the relevant results for the given prompt in each of them. We can use it to combine mutiple outputs and generate a summary, use it for information extraction systems etc.  

- [OpenAI API documentation](https://beta.openai.com/docs/)
- [Google Search Python Library](https://github.com/Nv7-GitHub/googlesearch-python)
- [Flask documentation](https://flask.palletsprojects.com/en/2.1.x/)
- [Prompt engineering explained](https://platform.openai.com/docs/guides/prompting)
