from flask import Flask, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Replace 'YOUR_COHERE_API_KEY' with your Cohere API key

# Initialize the Cohere Client with an API Key
api = os.getenv("GEMINI_API_KEY")
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/', methods=['POST'])
def get_response():
    try:
        course = request.get_json().get('course')
        target = request.get_json().get('target')
        duration = request.get_json().get('duration')
        # module = request.get_json().get('module')
        # submodules = request.get_json().get('submodules')
        
        # submodules = " , ".join(submodules)
            # Define the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": 
                            f'''
        I want to create a {course} course for {target} which has a duration of {duration}.
            Can you create a table of contents for it?
            Give the output in json format as code block:
            {{
                "courseTitle": "string",
                "courseDescription": "string",
                "courseObjective": ["strings"],
                "courseTags": ["strings"],
                "courseStructure": [
                    {{  
                        "moduleName": "string",
                        "subModules": ["strings"],
                        "quiz": "string" // just give the quiz description
                    }},
                    {{
                        "modulename": "string",
                        "submodules": ["strings"],
                        "quiz": "string" // just give the quiz description
                    }}
                ]
            }}
            where quiz should only be generated for each module. The quiz description should cover the concepts of all the submodules present in that module
        '''
                        }
                    ]
                }
            ]
        }

        # Set the headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the API call
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            # Parse and print the response JSON
            response_json = response.json()
            print(response_json["candidates"][0]["content"]["parts"][0]["text"][7:-3])
            return (response_json["candidates"][0]["content"]["parts"][0]["text"][7:-3])
            # print(json.dumps(response_json, indent=2))
            # print(response_json)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return json.dump(
            {
                "msg":"Error Assessing AI"
            }
            ) 

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
