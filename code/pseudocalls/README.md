# Pseudocalls – Fake Customer Call Generator for Foundry IQ

Generate realistic fake customer call transcripts for testing AI agents, analytics pipelines, and conversation tools. Each call simulates a ~10-minute meeting between 3–5 participants (Solution Engineers, Solution Architects, Technical Leads, etc.) discussing **Foundry IQ** implementation across multiple vertical markets.

## Features

- **5 Vertical Markets**: Healthcare, Financial Services, Retail, Manufacturing, Technology
- **4 Call Archetypes**:
  - **Problem Discovery** – Participants articulate current pain points with business impact
  - **Requirements Gathering** – Explicit functional and non-functional requirements discussion
  - **Architecture Review** – Deep technical dives on ontology, pipelines, CI/CD, and security
  - **Mixed** – Combination of all three segments
- **Realistic Dialogue**: Natural speaker rotation, follow-up questions, clarifications, and action items
- **Timestamped Transcripts**: Every line includes `[MM:SS]` timestamps
- **Structured Metadata**: JSON output with call details, participants, vertical, duration, and call type

## Quick Start

```bash
python generate_fake_calls.py
```

This generates two files:

| File | Description |
|------|-------------|
| `fake_customer_calls_2.txt` | All call transcripts with timestamps |
| `calls_metadata_2.json` | Structured metadata for each call |

## Configuration

Edit the constants at the top of `generate_fake_calls.py` to customize:

- **Number of calls** – Change the range in the `main()` loop (default: 50)
- **Output filenames** – Change `output_file` and `metadata_file` in `main()`
- **Verticals** – Add/remove entries in the `VERTICALS` dict
- **Participant roles** – Modify the `PARTICIPANT_ROLES` list
- **Companies** – Add to the `COMPANIES` list

## Sample Output

```
================================================================================
CALL #001 - Pioneer Tech (Healthcare)
Date: 2026-02-11
Duration: ~10 minutes
Participants: 5
Call Type: Problem Discovery
================================================================================

[00:00] Priya White (Data Engineer):
Good morning everyone, thanks for joining today's call. I'm Priya White and I'll
be facilitating our discussion on the Foundry IQ implementation for Pioneer Tech.

[00:10] Priya White (Data Engineer):
Before we jump in, let me do a quick round of introductions so everyone knows
who's on the line.

[00:16] Michael Jones (Customer Success Manager):
Hey team, I'm Michael Jones, serving as Customer Success Manager. Looking forward
to a productive session.

[00:24] Wei Jones (Solution Engineer):
Hi everyone, Wei Jones here. I'm the Solution Engineer on this engagement.
Excited to be part of this.

[01:10] Priya White (Data Engineer):
Let's start by getting a clear picture of the current pain points. Can someone
walk us through the biggest challenges you're facing today?

[01:25] Amanda Nakamura (Product Manager):
Our population health models are running on stale data - sometimes 48 hours old.
By the time we identify at-risk patients, interventions are already too late.

[01:46] Daniel Thompson (Solution Architect):
Walk me through a specific example. What does that look like day-to-day for
your team?
```

## Sample Metadata

```json
{
  "call_id": 1,
  "company": "Pioneer Tech",
  "vertical": "Healthcare",
  "call_type": "problem_discovery",
  "participants": [
    "Priya White (Data Engineer)",
    "Michael Jones (Customer Success Manager)",
    "Wei Jones (Solution Engineer)",
    "Amanda Nakamura (Product Manager)",
    "Daniel Thompson (Solution Architect)"
  ],
  "duration_seconds": 623,
  "duration_minutes": 10.4
}
```

## MCP Server – `extract_customer_questions`

An MCP (Model Context Protocol) server that exposes a tool to extract customer questions from call transcripts, with **sentiment** and **urgency** classification.

### Tools Provided

| Tool | Description |
|------|-------------|
| `extract_customer_questions` | Accepts raw transcript text, returns structured questions with classification |
| `extract_customer_questions_from_file` | Accepts a file path, reads the transcript, and returns structured questions |

### Sample Tool Output

```json
{
  "total_questions": 13,
  "urgency_breakdown": { "high": 2, "medium": 5, "low": 6 },
  "sentiment_breakdown": { "positive": 1, "neutral": 9, "negative": 3 },
  "questions": [
    {
      "timestamp": "01:10",
      "speaker": "Priya White (Data Engineer)",
      "question": "Can someone walk us through the biggest challenges you're facing today?",
      "urgency": "medium",
      "sentiment": "neutral"
    },
    {
      "timestamp": "03:01",
      "speaker": "Michael Jones (Customer Success Manager)",
      "question": "How long has this been a problem?",
      "urgency": "low",
      "sentiment": "negative"
    }
  ]
}
```

### Run the MCP Server Locally

```bash
cd mcp_server
pip install -r requirements.txt
python server.py
```

The server starts on `http://127.0.0.1:8000` with an SSE endpoint at `/sse`.

---

## Copilot Studio Integration

Follow these steps to connect the MCP server to Microsoft Copilot Studio as an action.

### Prerequisites

- The MCP server must be accessible over HTTPS from the internet (e.g., deployed to Azure App Service, Azure Container Apps, or tunneled via `devtunnel` / `ngrok` for testing)
- A Copilot Studio environment with agent authoring access

### Step 1 – Deploy the MCP Server

**Option A: Azure App Service (Production)**

1. Create an Azure App Service (Python 3.10+ Linux)
2. Deploy the `mcp_server/` folder
3. Set the startup command: `python server.py`
4. Note the public URL: `https://<your-app>.azurewebsites.net`

**Option B: Dev Tunnel (Local Testing)**

```bash
# Start the MCP server
cd mcp_server && python server.py

# In another terminal, create a tunnel
devtunnel host -p 8000 --allow-anonymous
```

Note the tunnel URL (e.g., `https://abc123.devtunnels.ms`)

### Step 2 – Add the MCP Action in Copilot Studio

1. Open [Copilot Studio](https://copilotstudio.microsoft.com)
2. Navigate to your agent → **Actions** in the left sidebar
3. Click **+ Add an action**
4. Select **MCP Server (preview)** as the action type
5. Enter the SSE endpoint URL:
   ```
   https://<your-server>/sse
   ```
6. Copilot Studio will auto-discover the available tools (`extract_customer_questions`, `extract_customer_questions_from_file`)
7. Click **Next** → review the tool schemas → **Add**

### Step 3 – Configure the Action in a Topic

1. Go to **Topics** → create or edit a topic (e.g., "Analyze Customer Call")
2. Add a **Question** node to collect the transcript from the user (or connect an input variable)
3. Add an **Action** node → select the `extract_customer_questions` action
4. Map the `transcript` input parameter to the user's message or variable
5. Add a **Message** node to display the results back to the user
6. Use **Power Fx** or **Adaptive Cards** to format the JSON response:

   ```
   Topic.extract_customer_questions.response
   ```

### Step 4 – Test

1. Click **Test** in the top-right corner of Copilot Studio
2. Paste a sample transcript from `fake_customer_calls.txt`
3. The agent should return the extracted questions with urgency and sentiment tags

### Architecture Diagram

```
┌──────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  Copilot      │ SSE  │   MCP Server     │      │   Transcript     │
│  Studio Agent │─────▶│  (Python/FastMCP)│◀─────│   Data           │
│              │◀─────│   :8000/sse      │      │                  │
└──────────────┘ JSON  └──────────────────┘      └──────────────────┘
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Could not connect to MCP server" | Ensure the server is running and the `/sse` endpoint is accessible over HTTPS |
| No tools discovered | Verify the server starts without errors; check `python server.py` logs |
| Timeout errors | Increase the Copilot Studio action timeout; large transcripts may need more processing time |
| Authentication errors | If using Azure App Service with auth, configure an API key or disable Easy Auth for testing |

---

## Requirements

- Python 3.10+
- `mcp[cli]` (for MCP server)

## License

MIT
