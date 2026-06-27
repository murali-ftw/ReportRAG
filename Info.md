# Task Assigned :

- To answer the user questions from the give file.
- The file can be an Annual or a Sustainability report of any company.
- The file path must be obtained from a backend schema stored in a PostgreSQL database.
- The question must be obtained from the user
- A frontend has to be built using Streamlit.

# Tasks Performed :

- Created ReportRAG which asks questions over company reports through a Langflow RAG pipeline. The app uses Postgres as the source of truth for report metadata, looks up the correct PDF path from the company name entered by the user, and sends the resolved inputs to a Langflow API endpoint.

1. The user opens the Streamlit app.
2. The user enters:
   - Company name
   - Question
3. The app searches Postgres for a matching `"CompanyName"` in the configured reports table.
4. The app selects the newest matching document by `"DocumentYear"`.
5. The app sends these inputs to Langflow:
   - `pdf_path`: the `"Path"` value from Postgres
   - question: the user's question
   - company name: the exact `"CompanyName"` value stored in Postgres
6. The Langflow has multiple components which :
   - Takes the file as input, parses it and adds metadata.
   - Divides the file into multiple chunks.
   - Each chunk is stored as a vectorised record in ChromaDB locally.
   - One collection is created per file. If the file is uploaded again, the existing collection is replaced.
   - The user's question is vectorised and is searched through the respective collection to find the matching records
   - The matching records are then collected and a parsed into a string.
   - The user question and the string is then passed as a prompt into an LLM(Google Gemini) for the generation of an answer.
   - The answer is displayed to the user.
   - The Question, Answer, Page Number and the Source Sentences are stored in an AstraDB Database.

# Difficulties Faced and Solutions Used:

| Flow Stage | Problem Faced | Initial Query Used | Solution Used |
|---|---|---|---|
| 1. Prompting & Structured Output | Extracting structured outputs (answer, page numbers, source sentences) from GPT responses in Langflow | “give me a prompt for open ai langflow. i have a pdf put into an md file as an input” | Custom JSON-only prompt template with fixed output schema |
| 2. Variable Extraction | Building custom components to separately extract answer, page numbers, and source sentences | “give a code for a custom component, which gets the output variables from the gpt answer” | Separate Langflow custom extractor components |
| 3. PDF → Markdown Conversion | Converting large PDFs into markdown while preserving structure/page references | “custom component for conversion of a large pdf (upto 15mb) into a md file” | Custom PDF-to-Markdown converter component |
| 4. Markdown Output Formatting | Returning markdown as a string instead of file path/JSON | “i want a md output... not a md file and file path output” | Returned markdown directly as string output |
| 5. Chunking | Chunking PDFs while preserving metadata/page numbers | “give me a custom code to chunk the extracted meta data from the file reader....” | Custom metadata-preserving chunker |
| 6. Chunking | Losing page numbers during chunking/vectorization/retrieval | “The PDF is a list of images stitched together, so each page number is an index...” | Embedded page markers and metadata into chunks |
| 7. Chunking | Chunker creating meaningless micro-chunks | “there is very low chunk characters.... the chunks are not meaningful” | Increased chunk size and reduced overlap |
| 8. Chunking / Langflow Data Types | Langflow type mismatches (`NoneType`, JSON/Data/Table issues) | “the parser returns the meta data in json format... the chunker must return chuncks in a data/dataframe/table format...” | Converted outputs into Langflow Data/DataFrame-compatible objects |
| 9. Chunking / LangChain Docs | `'Document' object has no attribute 'get'` due to LangChain Document handling | “Error building Component Chunk Documents:'Document' object has no attribute 'get'” | Switched from dict access to LangChain Document object handling |
| 10. Vectorization / Upload | Only one chunk being vectorized/uploaded | “the error is that i am getting only one chunk... not getting the updated in the vector table.” | Fixed chunk iteration and batch ingestion logic |
| 11. AstraDB Ingestion | Uploading extracted outputs into AstraDB | “create a custom component which gets the answer, pgno, and source sentences ans input and uploads it to a astra db collection "qnans"” | Custom AstraDB upload component |
| 12. AstraDB Parsing | Parser losing page numbers and returning malformed AstraDB results | “the parser which is supposed to conver the astradb search results is giving me this format. this is also a place where the page number is getting lost... give a custom code for the parser” | Custom parser preserving metadata and page references |
| 13. AstraDB Search | AstraDB vector search returning no results after ingestion | “i uploaded the chunks successfully to astradb and is vectorised... i have vectorised my question and i am not getting any search results... what could have been the error” | Fixed content field mapping and embedding consistency |
| 14. AstraDB Component Build | AstraDB UNSUPPORTED_SCHEMA_NAME / null collection error | “Error building Component Astra DB: The used schema name is not supported... unsupported Collection name: '(null)'” | Explicitly passed valid collection name/schema |
| 15. AstraDB Retrieval | AstraDB retrieval returning wrong document results (Walmart → Aramco contamination) | “i have attached my old ingestion code for astradb... if i input walmart.pdf and ask a question from it i am getting the answer from aramco.pdf... give a code for ingestion” | Added metadata/source-based filtering during retrieval |
| 16. AstraDB Metadata | Metadata filtering not working because metadata was stored incorrectly | “every vector is stored like this... give a exact complete code for the retrieval from astra dbv” | Stored metadata in proper metadata fields instead of chunk text |
| 17. Duplicate Handling | Duplicate vectors / repeated ingestion | “this is my flow.. i want two new requirements” | One-time vectorization logic + collection overwrite prevention |
| 18. Vectorization Logic | Designing automatic one-time vectorization logic | “so give a logic( in text only ) how you are going to find out whether a document has been vectorised before?” | PostgreSQL registry + file hash checking |
| 19. PostgreSQL Integration | PostgreSQL setup failures (missing DB / role) | “this is the schema being built by my team mate. i want to manually create this schema in postgres.” | Manual schema creation + corrected DB/user configuration |
| 20. Frontend Integration | Building Streamlit frontend integrated with Langflow | “build a front end with a proper flow..... i want a text input from user and a file input from the user using streamlit-python....” | Streamlit frontend connected to Langflow API |
| 21. Gemini Embeddings | Gemini embedding model failures (`404 NOT_FOUND`, unsupported embedding models) | “now i am trying google generative ai” | Switched from Gemini embeddings to OpenAI embeddings|
| 22. ChromaDB Migration | ChromaDB migration and collection isolation | “Summary: LangFlow AstraDB → ChromaDB Migration” | Migrated to ChromaDB with one collection per document |
| 23. Prompt Template | Prompt template failures due to malformed braces/template vars | “Flow build failed Error building Component Astra Result Parser:'list' object has no attribute 'value'” | Corrected prompt template syntax and variable names |

