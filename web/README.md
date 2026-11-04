# ArthSaathi – Digital Financial Literacy Agent

A plain HTML + CSS + JavaScript web app that provides financial literacy guidance through a conversational interface powered by IBM Granite on watsonx.ai via Langflow.

---

## Quick Start

### 1. Configure the app

Copy the example config file and fill in your Langflow details:

```bash
# from inside the web/ folder
cp config.example.js config.js
```

Open `config.js` in any text editor and set:

```js
window.ARTHSAATHI_CONFIG = {
  // Full Langflow run URL for your flow:
  LANGFLOW_URL: "http://localhost:7860/api/v1/run/YOUR-FLOW-ID-HERE",

  // Leave empty if your Langflow instance has no auth key:
  LANGFLOW_API_KEY: ""
};
```

> ⚠️ `config.js` is listed in `.gitignore` – **never commit it**. It may contain secret API keys.

---

### 2. Serve the app

No build step is needed. Serve the `web/` folder with any static file server.

**Python (recommended – ships with Python 3):**

```bash
cd web
python -m http.server 8000
```

Then open <http://localhost:8000> in your browser.

**Node.js alternative (if Python isn't available):**

```bash
npx serve web
```

---

## File Structure

```
web/
├── index.html          # App shell and layout
├── style.css           # All styling (no framework)
├── app.js              # All JavaScript logic
├── config.example.js   # Config template – commit this
├── config.js           # Your local config – DO NOT commit
└── README.md           # This file
```

---

## Features

| Feature | Details |
|---|---|
| **Chat interface** | User messages on the right, agent replies on the left |
| **Markdown rendering** | Bold, bullet lists, and numbered lists in agent replies |
| **Quick chips** | One-tap common questions (UPI, scam check, budget, EMI…) |
| **Language selector** | Reply in English, हिंदी, ಕನ್ನಡ, தமிழ், मराठी, বাংলা |
| **Scam Checker** | Paste a suspicious SMS/WhatsApp message for analysis |
| **Sensitive data guard** | Blocks sending PIN, OTP, CVV, or 12–16 digit card numbers |
| **Emergency banner** | Always-visible fraud helpline: **1930** / cybercrime.gov.in |
| **Typing indicator** | Animated dots while waiting for a response |
| **Mobile-friendly** | Works at 360 px width; large font for elderly users |

---

## Langflow API Format

The app sends:

```json
{
  "input_value":  "<user message>",
  "input_type":   "chat",
  "output_type":  "chat",
  "session_id":   "<random per-tab id>"
}
```

It reads the reply from:

```
data.outputs[0].outputs[0].results.message.text
```

If the response doesn't match that shape, the raw JSON is displayed instead.

---

## Disclaimer

ArthSaathi provides general financial education and information only. It does not constitute investment, legal, or tax advice. Always verify critical financial decisions with a certified professional.
