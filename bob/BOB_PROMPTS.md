# Using IBM Bob to build the ArthSaathi web app

Bob builds a small chat web page (plain HTML/CSS/JavaScript – no extra frameworks) that talks to your Langflow flow. The AI is still 100% Langflow + IBM Granite on watsonx.ai; Bob is the IBM tool you use to write the front-end.

**Before you start:** finish the Langflow flow and copy its API run URL (see `langflow/LANGFLOW_BUILD_GUIDE.md`, Part D).

Open IBM Bob → open the `ArthSaathi` folder → use **Code/Agent mode**. Paste the prompts one at a time and accept the changes after checking them. **Take a screenshot of Bob while it works** (for your deck / video – proof you used Bob).

---

### Prompt 1 – Build the app

```
Create a simple web app in a folder called "web" for "ArthSaathi – Digital Financial Literacy Agent".
Use only plain HTML, CSS and vanilla JavaScript (no frameworks, no build step, no npm).

Files:
- web/index.html
- web/style.css
- web/app.js
- web/config.example.js  (defines window.ARTHSAATHI_CONFIG = { LANGFLOW_URL: "http://localhost:7860/api/v1/run/<FLOW_ID>", LANGFLOW_API_KEY: "" })
- web/config.js is created by the user by copying config.example.js; add "web/config.js" to a .gitignore at the repo root.

Features:
1. Header with the app name, the tagline "Learn digital money safely – in your language", and a small IBM Granite badge.
2. A chat window. User messages on the right, agent replies on the left. Render the reply text with line breaks and bullet points kept (convert simple markdown: **bold**, "- " bullets, numbered lists). Escape HTML first to avoid XSS.
3. A row of quick-question chips: "How do I send money via UPI?", "Is this message a scam?", "Calculate my loan EMI", "Help me make a budget", "Government saving schemes", "I was cheated – what now?".
4. A language dropdown (English, हिंदी, ಕನ್ನಡ, தமிழ், मराठी, বাংলা). Prepend "Please reply in <language>." to the message sent to the agent.
5. A "Scam Checker" button that opens a textarea where the user pastes a suspicious SMS/WhatsApp message; send it as "Check this message for scam red flags: <text>".
6. A red emergency banner always visible at the bottom: "Lost money to fraud? Call 1930 or visit cybercrime.gov.in".
7. Before sending, check the message for a 4–6 digit number next to the words PIN/OTP/CVV, or a 12–16 digit number. If found, warn: "Never share your PIN, OTP, CVV or card number – not even with ArthSaathi." and do not send it.
8. Send messages with fetch POST to LANGFLOW_URL with JSON body
   { "input_value": <message>, "input_type": "chat", "output_type": "chat", "session_id": <a random id kept for the browser tab> }
   and header "x-api-key" if LANGFLOW_API_KEY is set.
   Read the reply from data.outputs[0].outputs[0].results.message.text (fall back to showing the raw JSON if the shape is different).
9. Show a typing indicator while waiting, and a friendly error message if the request fails.
10. Footer disclaimer: "ArthSaathi gives general financial education, not investment advice. Powered by IBM Granite on watsonx.ai via Langflow."

Design: clean, mobile-friendly, large readable font (good for elderly users), high contrast, IBM-blue (#0f62fe) accent, works at 360px width.
Also create a short web/README.md explaining how to run it: copy config.example.js to config.js, fill in the URL, then run "python -m http.server 8000" inside the web folder and open http://localhost:8000.
```

### Prompt 2 – Review (makes Bob check its own work)

```
Review the web folder for bugs, accessibility problems (labels, keyboard use, contrast) and security issues (XSS, secrets committed to git). Fix what you find and list the changes.
```

### Prompt 3 – If you get a CORS error in the browser console

```
The browser shows a CORS error when calling Langflow at localhost:7860. Explain the cause and give me the exact environment variable to set when starting Langflow so that http://localhost:8000 is allowed.
```
(Usually: start Langflow with `LANGFLOW_CORS_ORIGINS=http://localhost:8000`.)

---

## Run the demo
1. Start Langflow (your flow must be saved).
2. In `web/`, copy `config.example.js` → `config.js` and paste your run URL (and Langflow API key if needed).
3. `cd web` then `python -m http.server 8000`, open http://localhost:8000.
4. Ask the 7 test questions from the Langflow guide. Screenshot / screen-record → "Demo" for the deck or video.
