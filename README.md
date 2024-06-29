
---

# WHATSAPP DATA BUFFET

The WhatsApp Data Buffet is designed to enhance communication and interaction between patients and healthcare providers. Leveraging Mistral AI’s Function Calling fine-tuning APIs, the model is fine-tuned on patient records to efficiently and accurately retrieve information. This assistant handles various patient queries, ensuring quick and precise responses, thereby improving overall patient care and operational efficiency.

## Table of Contents
- [Installation](#installation)
- [Vonage WhatsApp Connection](vonage-whatsapp-connection)
- [Project Structure](project-structure)
- [Sample Questions](sample-questions)
  
## Installation

To run this project on your local machine, follow these steps:

1. Clone the repository:
   ```bash
    git clone https://github.com/WHATSAPP-DATA-BUFFET/Whatsapp_Data_Buffet
   ```
   
2. Navigate to the project directory:
  ```bash
      cd app
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

**Note**: 
The generated webhook will be active for 72 hours only. 
Due to Vonage account limitations, interactions are limited to approximately 15 message exchanges (sending and receiving messages) per account.

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

- **function_calling.py**: Contains function metadata and dynamically calls internal functions based on user queries.
- **db_utils.py**: Manages PostgreSQL connections and generates SQL queries using a Mistral model.
- **vonage.py**: Sends WhatsApp messages via the Vonage API, handling requests and authentication.
- **main.py**: Core application component for processing WhatsApp messages and responding via Flask.
- **ngrok.exe**: Creates secure tunnels to localhost, enabling public access for Vonage webhooks.
- **.env**: Stores credentials and configuration for Mistral, Vonage API, and database connections.
- **requirements.txt**: Lists Python dependencies required to run the application.

## Sample Questions

- `Question 1`: Can you confirm if my lead status is qualified or not for the birth date 1991-03-02.
- `Question 2`: Heyy! I need to know my primary copay balance for a follow-up visit. Can you help? Use this birth date to get my details, 1995-08-27.
- `Question 3`: I want to check if my prior authorization for the MRI at Imaging Center is still valid for my account with DOB 1991-03-02.
- `Question 4`: I need to know if my insurance covers my endoscopy treatment. Here is my birth date 1982-12-05.
- `Question 5`: I reported an adverse effect from a medication. Can you tell me the status of my case for the birth date 1995-08-27? It's important.


---
