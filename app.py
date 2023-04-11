from flask import Flask, request, jsonify
import openai
import requests
from bs4 import BeautifulSoup
from googlesearch import search

app = Flask(__name__)

# Configure the OpenAI API
openai.api_key = "enter-your-api-key"


def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

def get_mock_response(prompt):
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
    prompt = request.json['prompt']
    
    # Use this flag to control whether to use the actual API or the mock response
    use_mock_response = True

    if use_mock_response:
        results = get_mock_response(prompt)
    else:
        results = []
        # Perform a Google search using the open-source library
        for url in search(prompt, num_results=3):
            try:
                scraped_text = scrape(url)
                generated_prompt = f'Imagine you are a reliable accurate source of information. See if any relevant information regarding "{prompt}" in the following content: {scraped_text}'
                print(f"{url=}")
                # Send the new prompt to the OpenAI API
                response = openai.Completion.create(
                    engine="text-curie-001",
                    prompt=generated_prompt,
                    max_tokens=100,
                    n=1,
                    stop=None,
                    temperature=0,
                )
                generated_text = response.choices[0].text.strip()
                print(f"{generated_text=}")
                results.append({"source": url, "generated_text": generated_text})

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
