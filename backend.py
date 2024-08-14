from ibm_watson import IAMTokenManager
import requests
import PyPDF2
import io
import re

class TokenGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.token_manager = IAMTokenManager(apikey=self.api_key)

    def generate_token(self):
        return self.token_manager.get_token()

class TextGenerator:
    def __init__(self, api_key):
        self.token_generator = TokenGenerator(api_key)
        self.token = self.token_generator.generate_token()
        self.url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def generate_text(self, user_input):
        prompt = (
            "Provide a concise list of practical tips to reduce personal carbon footprint in daily life. "
            "Focus only on individual actions that can be easily incorporated into daily routines. "
            "Format the response as a bullet point list using '•' symbols. "
            "Keep each point brief and actionable. Do not discuss climate change or global temperature. "
            "Strictly answer the following question: " + user_input
        )

        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 250,
                "stop_sequences": ["\"What\"","\"How\"","\"Why\"","\"Would\"","\"Can\"","\"Is\""],
                "repetition_penalty": 1.5
            },
            "model_id": "meta-llama/llama-3-405b-instruct",
            "project_id": "1a28e7b5-592d-4083-9d64-75491cdde1c2",
            "moderations": {
                "hap": {
                    "input": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {
                            "remove_entity_value": True
                        }
                    },
                    "output": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {
                            "remove_entity_value": True
                        }
                    }
                }
            }
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=body
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        return response.json()['results'][0]['generated_text']

    def format_response(self, response):
        # Split the response by double asterisks
        sections = re.split(r'\*{2,}', response)
        
        formatted_sections = []
        for section in sections:
            # Remove any remaining asterisks and extra spaces
            section = re.sub(r'\*', '', section).strip()
            if section:
                # Split the section into lines
                lines = [line.strip() for line in section.split('\n') if line.strip()]
                
                # Format each line
                formatted_lines = []
                for i, line in enumerate(lines):
                    if i == 0 or line.isupper():  # Main category
                        formatted_lines.append(line.upper())
                    elif ':' in line:  # Subcategory
                        formatted_lines.append(f"**{line}**")
                    elif line.startswith('•'):  # Already a bullet point
                        formatted_lines.append(line)
                    else:  # Add bullet point if not present
                        formatted_lines.append(f"• {line}")
                
                formatted_sections.append(formatted_lines)
        
        return formatted_sections

    def generate_and_format_text(self, user_input):
        response = self.generate_text(user_input)
        return self.format_response(response)

class PDFReader:
    def __init__(self, text_generator):
        self.text_generator = text_generator

    def read_pdf(self, file):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text

    def analyze_pdf(self, file):
        pdf_content = self.read_pdf(file)
        query = (
            "Based on the following report, provide specific, actionable recommendations for reducing "
            "the household's environmental impact. Focus on energy consumption, transport, food choices, and waste disposal. "
            "Organize the recommendations into categories. Each recommendation should be a small, gradual step that can be "
            "implemented immediately. Format your response as follows:\n"
            "1. Use '**' to separate main categories.\n"
            "2. Capitalize main category names.\n"
            "3. Use '**' for subcategories followed by a colon.\n"
            "4. Use bullet points for all specific recommendations.\n"
            "5. Include some specific numerical suggestions (e.g., 'once per week', '$5-7 monthly').\n"
            "Here's the report content: " + pdf_content
        )
        response = self.text_generator.generate_text(query)
        return self.text_generator.format_response(response)