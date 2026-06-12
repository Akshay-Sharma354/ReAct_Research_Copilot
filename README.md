# ReAct Research Copilot 🚀

An AI-powered research assistant that uses the **ReAct (Reasoning + Acting)** pattern combined with **Retrieval-Augmented Generation (RAG)** to answer complex questions about AI and machine learning research.

## 🎯 Overview

The ReAct Research Copilot is an intelligent agent that:
- 🤔 **Thinks** about what information it needs
- 🔍 **Searches** a document corpus for relevant passages
- 📖 **Reads** and synthesizes information from retrieved documents
- 💬 **Answers** with well-structured, cited responses

This project was built as a **BIA Capstone Project** to demonstrate practical implementation of advanced AI concepts.

---

## 🏗️ Architecture

```
User Query
    ↓
LLM Agent (Groq LLaMA 3.3)
    ↓
ReAct Loop:
  1. Think: What info do I need?
  2. Act: Search corpus for documents
  3. Observe: Read retrieved passages
  4. Decide: Generate answer with citations
    ↓
Response with Sources
```

### Core Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Groq (LLaMA 3.3 70B) | Reasoning and answer generation |
| **Embeddings** | Sentence-Transformers | Semantic document search |
| **Retrieval** | Cosine Similarity (scikit-learn) | Finding relevant passages |
| **Frontend** | Command-line Interface | User interaction |
| **Knowledge Base** | Markdown documents | AI/ML research corpus |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Groq API key (free at https://console.groq.com)
- ~500MB disk space (for embeddings)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Akshay-Sharma354/ReAct_Research_Copilot.git
cd ReAct_Research_Copilot
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment:**
Create a `.env` file in the root directory:
```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

Get your free API key from: https://console.groq.com/keys

5. **Run the application:**
```bash
python src/main.py
```

---

## 💬 Usage

Once running, ask any question about AI/ML research:

```
📝 Your question: What are transformers?
```

**Example Output:**
```
🔍 Searching: transformers definition
🔍 Searching for: transformers definition

--- STEP 2 ---
LLaMA 3.3: Transformers are a neural network architecture...

================================================================================
📊 Summary:
  - Steps taken: 2
  - Searches performed: 1
  - Search queries: transformers definition
```

### Example Questions

- "What is document chunking?"
- "Explain the ReAct pattern"
- "How does Retrieval-Augmented Generation work?"
- "What is knowledge distillation?"
- "Describe few-shot learning"

---

## 📚 Knowledge Base

The corpus includes **36 comprehensive documents** covering:

### AI/ML Fundamentals
- Neural Networks & Deep Learning
- Transformers & Attention Mechanisms
- Natural Language Processing (NLP)

### Advanced Topics
- Prompt Engineering & In-Context Learning
- Fine-tuning & Instruction Tuning
- Model Alignment & Safety
- Multimodal AI & Vision-Language Models

### Specialized Areas
- Retrieval-Augmented Generation (RAG)
- Knowledge Distillation & Model Compression
- Few-Shot Learning & Meta-Learning
- Continual Learning & Catastrophic Forgetting
- Adversarial Robustness
- Ethics in AI

### Documents Organization
```
corpus/
├── documents.md          (20 core AI/ML documents)
├── advanced_topics.md    (15 advanced research topics)
└── chunking.md          (Document chunking strategies)
```

---

## 🔧 Project Structure

```
ReAct_Research_Copilot/
├── src/
│   ├── main.py              # Entry point
│   ├── agent.py             # ReAct agent logic
│   ├── retriever.py         # Document retrieval system
│   └── react_agent.py       # Core ReAct implementation
├── corpus/
│   ├── documents.md         # Core AI/ML knowledge base
│   ├── advanced_topics.md   # Advanced research topics
│   └── chunking.md         # Document chunking guide
├── data/                    # (Empty) For future datasets
├── notebooks/               # (Empty) For Jupyter notebooks
├── requirements.txt         # Python dependencies
├── .env                     # API keys (not in repo)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## 🔄 How ReAct Works

### The ReAct Loop

1. **Thought**: LLM analyzes the query and decides what to search for
   ```
   "The user asked about transformers. I need to search for 'transformers definition'"
   ```

2. **Action**: Agent searches the document corpus
   ```
   Query embedding → Cosine similarity → Top-K documents retrieved
   ```

3. **Observation**: LLM reads the retrieved passages
   ```
   Document chunks analyzed and summarized
   ```

4. **Answer**: LLM synthesizes information with citations
   ```
   "Transformers are [Result 1]... [Result 2]..."
   ```

### RAG Integration

- **Retrieval**: Semantic search finds relevant documents
- **Augmentation**: Retrieved context is added to LLM prompt
- **Generation**: LLM generates grounded, factual answers
- **Citations**: Answers include source references

---

## 🎯 Key Features

✅ **Semantic Search**: Uses embeddings for intelligent document retrieval  
✅ **ReAct Pattern**: Transparent reasoning with step-by-step thinking  
✅ **Citation Support**: All answers reference source documents  
✅ **Fast Inference**: Groq API provides sub-second response times  
✅ **Scalable Corpus**: Easy to add new documents and expand knowledge base  
✅ **No Fine-tuning Required**: Works with base LLaMA model  
✅ **Privacy-Focused**: All processing on your machine (API calls only to Groq)  

---

## 📊 Performance Metrics

Tested on sample questions with 36 documents:

- **Average Response Time**: 2-3 seconds
- **Retrieval Accuracy**: High relevance matches
- **Generation Quality**: Coherent, well-cited answers
- **Hallucination Rate**: Low (grounded in retrieved documents)
- **Token Efficiency**: ~500-2000 tokens per query

---

## 🛠️ Technologies Used

### Core Libraries
- **groq**: Groq API client for LLM access
- **sentence-transformers**: Dense passage retrieval embeddings
- **scikit-learn**: Cosine similarity for document ranking
- **python-dotenv**: Environment variable management

### APIs & Services
- **Groq Cloud**: LLaMA 3.3 70B inference
- **Hugging Face**: Pre-trained sentence embeddings

---

## 🔐 Security & Privacy

### API Key Management
- `.env` file is gitignored (never committed to GitHub)
- API keys stored locally only
- Create separate keys for different environments

### Data Privacy
- Document corpus stored locally
- No user queries sent to external services (except Groq API)
- Retrieved documents processed privately

---

## 🚀 Future Enhancements

- [ ] Web UI (Streamlit/FastAPI)
- [ ] Vector database integration (Pinecone, Weaviate)
- [ ] Multi-document retrieval strategies
- [ ] Custom document upload
- [ ] Fine-tuned models for specific domains
- [ ] Conversation history & context
- [ ] Performance metrics dashboard

---

## 🐛 Troubleshooting

### "Invalid API Key" Error
- Check `.env` file has correct Groq API key
- Verify key is active at https://console.groq.com/keys
- No spaces or quotes in key

### "No documents found" Error
- Ensure `corpus/` folder has `.md` files
- Check file paths are correct
- Verify documents are properly formatted

### Slow responses
- First run processes embeddings (slower)
- Subsequent runs use cached embeddings (faster)
- Groq API latency depends on server load

---

## 📖 Learning Resources

### ReAct Pattern
- Original Paper: "ReAct: Synergizing Reasoning and Acting in Language Models"
- Learn how agents think and act

### RAG Concepts
- Query expansion & document chunking
- Semantic search fundamentals
- Context-aware generation

### Groq API
- Documentation: https://console.groq.com/docs/
- Supported models and pricing
- API rate limits and best practices

---

## 👥 Contributing

### Adding Documents to Corpus
1. Create a new `.md` file in `corpus/`
2. Follow the existing format with clear sections
3. Update this README with topic
4. Test with sample questions
5. Commit and push

### Improving the Agent
- Enhance retrieval strategies
- Optimize prompt engineering
- Add new reasoning patterns
- Improve citation accuracy

---

## 📝 License

This project is open source and available for educational purposes.

---

## 🎓 About This Project

**BIA Capstone Project** - Boston Institute of Analytics  
**Developer**: Akshay Sharma  
**Date**: June 2026  
**Status**: ✅ Complete and functional

This project demonstrates:
- ✅ RAG (Retrieval-Augmented Generation) implementation
- ✅ ReAct (Reasoning + Acting) pattern
- ✅ Semantic search with embeddings
- ✅ LLM API integration (Groq)
- ✅ Full project workflow (dev → GitHub)

---

## 📞 Support

For issues, questions, or suggestions:
1. Check this README first
2. Review error messages carefully
3. Check Groq documentation
4. Create an issue on GitHub

---

## 🎉 Acknowledgments

Built with:
- **Groq** for fast LLM inference
- **Sentence-Transformers** for embeddings
- **scikit-learn** for similarity search
- **LLaMA 3.3** for powerful reasoning

---

**Happy researching! 🚀**

For more AI projects, visit: https://github.com/Akshay-Sharma354