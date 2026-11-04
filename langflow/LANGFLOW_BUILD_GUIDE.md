# Build the ArthSaathi flow in Langflow (about 45 minutes)

**Technologies used (only those allowed in the guidelines):** Langflow · IBM watsonx.ai (on IBM Cloud Lite) · IBM Granite models · Docling.
No third-party vector database or LLM is used.

You need: Langflow running, an IBM Cloud account with a **watsonx.ai project**, your **API key**, **Project ID** and **region URL** (e.g. `https://us-south.ml.cloud.ibm.com`).

Where to find them:
- API key: IBM Cloud → Manage → Access (IAM) → API keys → Create.
- Project ID: watsonx.ai → your project → Manage tab → General → Project ID.
- Make sure the project has a **Watson Machine Learning** service associated (Manage → Services & integrations).

---

*Written for Langflow 1.13. Start Langflow with `C:\Users\Aishwarya\langflow-env\start-langflow.ps1` and open http://localhost:7860.*

## Part A – Load the knowledge base (RAG ingestion)

**A1. Connect IBM watsonx.ai once.** Click your profile icon (top right) → **Settings → Model Providers → IBM WatsonX**. Enter the API Key, Project ID and Endpoint URL → **Save**. Both Granite models should then be enabled:
- Language model: `ibm/granite-4-h-small`
- Embedding model: `ibm/granite-embedding-278m-multilingual`

**A2. Create the flow.** On the home page click **Create first flow** (or **New Flow**) → **Blank Flow**. Rename it `ArthSaathi`.

**A3. Build the ingestion chain.** Search the left component panel and drag in each component:

```
[Docling] ──► [Export DoclingDocument] ──► [Split Text] ──► [Knowledge Ingestion]
```

1. **Docling** – click *Files* and upload all 5 `.md` files from `Downloads\ArthSaathi_knowledge`. Leave Pipeline `standard` and OCR `None`.
2. **Export DoclingDocument** – Export format `Markdown`. Drag from Docling's **Files** dot to Export's **JSON or Table** input.
3. **Split Text** – Chunk Size `800`, Chunk Overlap `150`. Connect Export's **Table** output → Split Text **Input**.
4. **Knowledge Ingestion** – Mode **Ingest**. In the *Knowledge* dropdown choose **+ Create new knowledge** (or create it on the Knowledge page). Name it `arthsaathi_kb` and pick the embedding model `ibm/granite-embedding-278m-multilingual`. Connect Split Text **Chunks** → Knowledge Ingestion **Input**.

**A4. Run it.** Click ▶ on **Knowledge Ingestion**. The first Docling run downloads its models, which takes 1–3 minutes. When every component shows a green tick, the knowledge base is loaded. You only need to do this again if you change the files.

## Part B – The agent (query side)

Build this in the same flow, below the ingestion chain:

```
[Chat Input] ──► [Agent – IBM Granite on watsonx.ai] ──► [Chat Output]
                        ▲                     ▲
   tools:  [Knowledge Base (Retrieve), Tool Mode]   [Calculator, Tool Mode]
```

1. **Chat Input** – default.
2. **Agent** – Language Model `ibm/granite-4-h-small`. Paste everything from `agent_instructions.txt` into **Agent Instructions**.
3. **Knowledge Base** – Mode **Retrieve**, Knowledge `arthsaathi_kb`. Turn on **Tool Mode** (component header menu). Edit the tool description to: *"Search trusted RBI/NPCI/government material about UPI, scams, interest rates, loans, budgeting and government schemes. Use for every factual question."* Connect its **Toolset** → Agent **Tools**.
4. **Calculator** – turn on Tool Mode and connect it → Agent **Tools**.
5. **Chat Output** – connect Agent **Response** → Chat Output.

## Part C – Test in the Playground

Click **Playground** and try these (screenshot the good answers for the deck):

1. `How do I send money via UPI?`
2. `Someone on OLX sent me a QR code and said scan it to receive ₹5000. Is it safe?`
3. `I want a ₹1,00,000 loan at 12% for 12 months. What will my EMI be?`
4. `What is a safe interest rate for a personal loan?`
5. `मुझे बजट बनाना सिखाओ, मेरी सैलरी 20,000 है`
6. `I shared my OTP with a caller 10 minutes ago, what do I do?`
7. `Which stock should I buy to double my money?` (it should politely refuse and educate)

## Part D – Things the deck needs from you

- **Screenshot of the whole flow canvas** → slide "Langflow workflow".
- **Token usage**: in the Playground message details (or watsonx.ai project → usage) note tokens before and after your test prompts → slide "Token Usage". Screenshot both.
- **Export**: flow menu (top-left) → **Export** → keep *"Save with my API keys"* **OFF** → save as `app.json`. This goes in GitHub. **Never upload a file containing your API key.**
- **API endpoint for the Bob web app**: click **Share → API access** and copy the run URL – it looks like `http://localhost:7860/api/v1/run/<flow-id>`. If Langflow asks for an API key, create one in Settings → Langflow API Keys.
