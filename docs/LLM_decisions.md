# LLM Usage Decisions

This document describes why we chose external LLM providers (OpenAI, Anthropic) and how we plan to integrate them in the Global Roaming Regulation Tracker.

---

## 1. Why OpenAI / Anthropic?

- **Reliability & Quality**: These commercial APIs are known to provide high-quality, state-of-the-art language models suitable for summarization and classification tasks.
- **Ease of Integration**: Both offer REST-based APIs, making it straightforward to call them from a Python-based backend (e.g., FastAPI).
- **Scalability**: They can handle large volumes of text with robust infrastructure, scaling as our data grows.

---

## 2. How We Plan to Use LLMs

1. **Offline Summarization**
   - When new regulatory documents are ingested, we send the cleaned text to the LLM to generate a concise summary.
   - Store these summaries in MongoDB for quick display in the UI.

2. **Classification / Labeling**
   - Prompt the LLM to assign categories (e.g., data cap, pricing, licensing).
   - Use these labels as metadata fields to enhance search and filtering.

3. **RAG-Based Q&A**
   - For user queries, we first retrieve the most relevant chunks from our vector store (MongoDB Atlas Search, Milvus, or Weaviate).
   - We then send those chunks, plus the user’s question, to the LLM for a final answer grounded in real regulation text.
   - This ensures accurate, reference-based responses.

---

## 3. Future Considerations (Agent-Based Workflows)

- **Phase 2+**: We may introduce multi-step reasoning or “agentic” behavior if users need complex cross-country comparisons or multi-step tasks. 
- **Guardrails**: Should we implement an agent approach, we’ll need robust monitoring and fallback logic to avoid misinterpretation or hallucinations.

---

## 4. Summary

Using OpenAI and Anthropic helps us get production-ready LLM features quickly. We’ll start with offline summarization + RAG. If advanced workflows are needed later, we’ll explore agent-based approaches.
