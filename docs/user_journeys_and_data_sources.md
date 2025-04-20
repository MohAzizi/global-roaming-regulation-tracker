# User Journeys & Data Sources

## 1. User Journeys

1. **Search for Regulations by Country**
   - A user selects a country (or multiple) and gets a list of relevant roaming regulations.
   - The system displays short summaries and highlights the key points (e.g., data caps, pricing rules).

2. **Filter by Regulation Type**
   - Users can narrow results by categories (pricing, licensing, data cap) or effective date range.
   - Summaries are quickly visible; clicking on an entry shows the full text or a detailed summary.

3. **Export Reports**
   - Users generate custom PDF or CSV reports with selected regulations.
   - The system automatically includes metadata (country, date, category) and LLM-generated summary.

4. **Q&A (RAG-Based)**
   - Users type queries like, “What are the latest data cap changes in France?”
   - The system retrieves relevant text from the vector store, then calls the LLM to produce a final answer referencing the actual regulation text.

5. **Future**: Alerts & Watchlists
   - Users can subscribe to certain countries or topics.
   - The system notifies them when new or updated regulations match their preferences (planned for later phases).

---

## 2. Data Sources

1. **Official Government APIs**
   - e.g., FCC in the U.S., ARCEP in France, or telecom authority sites in each region.

2. **Web Pages & PDFs**
   - Some government portals only post updates in HTML or PDF format, requiring scraping or PDF text extraction.

3. **RSS/Atom Feeds**
   - Certain official websites provide RSS for newly published or updated regulations.

4. **Third-Party / Public Databases**
   - Possible aggregated listings from international bodies (e.g., ITU, GSMA).
   - Potential open data portals with telecommunication stats and legal documents.

5. **Manual Uploads (Later)**
   - (Optional) For advanced or restricted documents, an admin could upload a PDF or doc directly into the system.

---

## 3. Next Steps

- Finalize the ingestion plan for each data source (API calls, scraping scripts, or RSS feed polling).
- Begin implementing the search & filter features after we have some example data.

