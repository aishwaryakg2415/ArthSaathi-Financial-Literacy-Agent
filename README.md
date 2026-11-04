# ArthSaathi-Financial-Literacy-Agent

# ArthSaathi – AI Agent for Digital Financial Literacy

IBM SkillsBuild University Engagement (AICTE 2026) – **Problem Statement No. 7**

ArthSaathi ("money companion") is an agentic AI assistant that teaches people in India how to use digital finance safely – UPI, scam safety, interest rates & loans, budgeting and government schemes – in their own language, with answers grounded in trusted sources.

## Built with
| Technology | Used for |
|---|---|
| **Langflow** | RAG pipeline + tool-using agent |
| **IBM Granite** (`granite-4-h-small`, Granite embedding) | Reasoning, multilingual answers, embeddings |
| **IBM watsonx.ai** (IBM Cloud Lite) | Hosting and serving the Granite models |
| **Docling** | Parsing the knowledge documents |
| **IBM Bob** | Building the web chat front-end |

## Features
- Answers grounded in RBI / NPCI / I4C / government-scheme material (RAG), with the source named
- Scam Checker – paste a suspicious SMS/WhatsApp, get red flags + verdict + next steps
- EMI / interest / budget calculations via a Calculator tool
- Fraud emergency guidance (1930, cybercrime.gov.in, RBI zero-liability window)
- Replies in the user's language
- Guardrails: never asks for PIN/OTP/CVV, no investment tips, says "not sure" instead of guessing

## Repository
```
app.json                      Langflow flow export (no API keys)
Problem_Statement_7.pdf       Problem statement
ArthSaathi_Presentation.pptx  Project presentation
knowledge/                    RAG source documents
langflow/                     Agent instructions + flow build guide
web/                          Chat front-end (built with IBM Bob)
assets/                       Architecture diagram
```

## Run it
1. Import `app.json` into Langflow, then fill in your watsonx.ai API key, Project ID and URL in the IBM components.
2. Upload the `knowledge/` files into the Docling component and run the vector-store (ingest) component once.
3. Open the Playground and ask: *"How do I send money via UPI?"*
4. Web app: copy `web/config.example.js` to `web/config.js`, paste your Langflow run URL, then run `python -m http.server 8000` inside `web/` and open http://localhost:8000.

## Disclaimer
ArthSaathi gives general financial education, not personalised investment advice. Rates, limits and scheme details change, so check them with your bank or the official portal.
