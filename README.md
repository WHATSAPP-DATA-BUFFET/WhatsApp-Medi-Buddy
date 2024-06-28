
---

# Patient-Healthcare Communication Assistant

The use case aims to enhance communication and interaction between patients and healthcare providers. By leveraging Mistral AI’s function-calling fine-tuning APIs, we've developed an assistant capable of efficiently and accurately handling various patient queries.

## Table of Contents
- [Installation](#installation)
- [Vonage WhatsApp Connection](vonage-whatsapp-connection)
- [Project Structure](project-structure)
- [Sample Questions](sample-questions)
  
## Installation

To run this project on your local machine, follow these steps:

1. Clone the repository:
   ```bash
    git clone https://github.com/your-username/patient-healthcare-assistant.git
   ```
   
2. Navigate to the project directory:
  ```bash
      cd patient-healthcare-assistant
  ```

3. Install the required dependencies:
   
```bash
    pip install -r requirements.txt
   ```

## Vonage WhatsApp Connection

To set up the Vonage WhatsApp connection:

1. Go to the `app` folder and run the `main.py` file:
```bash
  python app/main.py
 ```

2. Run ngrok parallely to create a secure tunnel:
```bash
  ./ngrok http 5000
 ```

Copy the generated webhook URL.

3. Log in to Vonage using credentials from `.env` using this link:
[Vonage Login](https://dashboard.nexmo.com/sign-in?adobe_mc=MCMID%3D15640697533634033622262375739442374659%7CMCORGID%3DA8833BC75245AF9E0A490D4D%2540AdobeOrg%7CTS%3D1719571570&cjregion=429207)

4. Navigate to 'Send a WhatsApp message' in the Vonage API Dashboard using this link:
[Send a WhatsApp Message](https://dashboard.nexmo.com/messages/sandbox)

5. Paste `<copied_webhook_address/chat>` in the inbound webhook space with 'HTTP POST' to forward inbound messages to this URL and save the webhook.

6. Scan the QR code to chat with the bot.

Note: The generated webhook will be active for 72 hours only. 

## Project Structure

Here’s an overview of the project structure:

```
Whatsapp_Data_Buffet/
└── app/
    ├── function_calling.py
    ├── db_utils.py
    ├── vonage.py
    ├── main.py
    ├── ngrok.exe
    ├── .env
    └── requirements.txt

```

## Description of Each File

- **function_calling.py**: Contains function descriptions with function names, descriptions, parameters, and parameter types for each function. Processes a given question by dynamically selecting and calling the appropriate internal function (copay status, prior authorization status, insurance updates, case reports, lead details) based on the context of the question provided.
- **db_utils.py**: Sets up and manages connections to a PostgreSQL database. Initializes a language model from Hugging Face and generates SQL queries based on user questions to retrieve relevant data from specified database tables. Ensures conversational and accurate responses to user inquiries by leveraging natural language processing techniques.
- **vonage.py**: Sends messages via the Vonage API. The primary function sends a text message to a specified recipient using the WhatsApp channel, handling the API request and authentication process.
- **main.py**: Serves as the core component of the application, responsible for extracting messages received from WhatsApp, processing them, and sending responses back to the user through Vonage. Sets up a Flask server with routes to handle incoming messages, ensures messages are processed uniquely using threading locks, and generates appropriate responses.
- **ngrok.exe**: Ngrok is used to create secure tunnels to your localhost, making it accessible over the internet. It is useful for exposing your local Flask server to Vonage's webhooks, allowing Vonage to send incoming messages to your local development environment. It simplifies the development and testing process by providing a public URL for your locally running application.
- **.env**: Contains credentials and configuration parameters for the Mistral model, Mistral fine-tuning, Vonage API, and Database connection settings.
requirements.txt: Contains all necessary import statements for Python dependencies required to run the application.


## Sample Questions

- `Question 1`: 
- `Question 2`:
- `Question 3`: 
- `Question 4`:
- `Question 5`: 


---
