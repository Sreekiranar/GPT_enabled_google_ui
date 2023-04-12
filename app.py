import openai
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from googlesearch import search

app = Flask(__name__)

# Configure the OpenAI API
openai.api_key = "enter_your_api_key"

def scrape(url):
    """
    Scrape the content of the given URL and return all the text.

    Args:
        url (str): URL to scrape.

    Returns:
        str: The concatenated text from the scraped webpage.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script and style elements
    for script in soup(['script', 'style']):
        script.decompose()

    # Get the text from the entire webpage
    text = soup.get_text()

    # Remove leading and trailing spaces and join the lines
    lines = (line.strip() for line in text.splitlines())
    text = ' '.join(line for line in lines if line)

    return text

def get_mock_response(prompt):
    """
    Generate a mock response for the given prompt.

    Args:
        prompt (str): The text prompt.

    Returns:
        list: A list of dictionaries containing "source" and "generated_text" keys.
    """
    fake_results = []
    for i in range(3):
        fake_result = {
            "source": f"https://example.com/mock-source-{i + 1}",
            "generated_text": f"Mock output for '{prompt}' from source {i + 1}"
        }
        fake_results.append(fake_result)
    return fake_results


@app.route('/send_prompt', methods=['POST'])
def send_prompt():
    """
    Endpoint that receives the prompt from the client and returns a JSON response
    containing generated text and source URLs.
    """
    # Retrieve the prompt from the request
    prompt = request.json['prompt']
    print(prompt)
    # Use this flag to control whether to use the actual API or the mock response
    use_mock_response = False

    if use_mock_response:
        results = get_mock_response(prompt)
    else:
        results = []
        # Perform a Google search using the open-source library
        for i, url in enumerate(search(prompt, num_results=3)):
            try:
                scraped_text = scrape(url)
                with open(f"scraped_text_{i+1}.txt", 'w') as f:
                    f.write(scraped_text)
                generated_prompt = f'Please provide an accurate and concise reponse for the following prompt:{prompt}, use only the information provided in the {scraped_text}. provide any necessary links that might have relevant information if needed'
                print(f"{url=}")
                # Send the new prompt to the OpenAI API
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=generated_prompt,
                    max_tokens=400,
                    n=1,
                    stop=None,
                    temperature=0,
                )
                generated_text = response.choices[0].text.strip()
                print(f"{generated_text=}")
                results.append(
                    {"source": url, "generated_text": generated_text})

            except Exception as e:
                print(f"Error scraping {url}: {e}")
    print(f"result json: \n {results}")
    return jsonify(results)


# Enable CORS (Cross-Origin Resource Sharing) to allow requests from the frontend
@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    header["Access-Control-Allow-Headers"] = "Content-Type"
    header["Access-Control-Allow-Methods"] = "POST"
    return response


if __name__ == '__main__':
    app.run(debug=True)
