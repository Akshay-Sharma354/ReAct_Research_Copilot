import os
from groq import Groq
from dotenv import load_dotenv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from retriever import DocumentRetriever

load_dotenv()

class ReActAgent:
    def __init__(self):
        """Initialize the ReAct agent with Groq client and document retriever."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
        
        print("📚 Initializing document retriever...")
        self.retriever = DocumentRetriever()
        self.model = "llama-3.3-70b-versatile"
        
    def query(self, user_question: str) -> str:
        """
        Process a user question using the ReAct pattern.
        
        Args:
            user_question: The user's research question
            
        Returns:
            String containing the agent's response with citations
        """
        print(f"\n{'='*80}")
        print(f"USER QUESTION: {user_question}")
        print(f"{'='*80}\n")
        
        # STEP 1: THINK - Decide what to search for
        think_prompt = f"""You are a research assistant. A user has asked the following question:

"{user_question}"

Think about what you need to search for to answer this question. Be specific about search queries.
Respond with just the search queries (one per line), nothing else."""

        think_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": think_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        search_queries = think_response.choices[0].message.content.strip().split('\n')
        search_queries = [q.strip() for q in search_queries if q.strip()]
        
        print("--- STEP 1: THINKING ---")
        print(f"Search queries identified: {search_queries}\n")
        
        # STEP 2: ACT - Search for relevant documents
        print("--- STEP 2: SEARCHING ---")
        all_results = []
        
        for query in search_queries[:3]:  # Limit to 3 searches
            print(f"🔍 Searching: {query}")
            results = self.retriever.search(query, top_k=3)
            all_results.extend(results)
        
        if not all_results:
            return "❌ I couldn't find relevant information in my knowledge base to answer this question. Try asking about AI/ML topics like transformers, RAG, neural networks, etc."
        
        print(f"✅ Found {len(all_results)} relevant passages\n")
        
        # STEP 3: READ - Format retrieved documents
        print("--- STEP 3: READING ---")
        documents_context = self._format_documents(all_results)
        print(f"📖 Formatted {len(all_results)} passages for synthesis\n")
        
        # STEP 4: ANSWER - Generate synthesis
        print("--- STEP 4: ANSWERING ---")
        answer_prompt = f"""Based on the following research passages, answer this question:

QUESTION: {user_question}

RESEARCH PASSAGES:
{documents_context}

Provide a well-structured, comprehensive answer that:
1. Directly answers the question
2. Uses the information from the passages
3. Includes citations like [Result 1], [Result 2], etc.
4. Is clear and informative
5. Organized with clear sections if needed"""

        answer_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": answer_prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        final_answer = answer_response.choices[0].message.content
        
        # Format output
        output = f"""
## 🔬 RESEARCH PROCESS

### Step 1: Thinking
Identified search queries: {', '.join(search_queries[:3])}

### Step 2: Searching
Found {len(all_results)} relevant passages from knowledge base

### Step 3: Reading
Analyzed and synthesized information

### Step 4: Answer
Generated comprehensive response

---

## 📖 FINAL ANSWER

{final_answer}

---

## 📊 Summary

- **Steps taken**: 4 (Think → Search → Read → Answer)
- **Searches performed**: {len(search_queries[:3])}
- **Documents retrieved**: {len(all_results)}
- **Model**: LLaMA 3.3 70B (Groq)
"""
        
        print(f"✅ FINAL ANSWER PROVIDED")
        print(f"{'='*80}\n")
        
        return output
    
    def _format_documents(self, results: list) -> str:
        """Format retrieved documents for the LLM prompt."""
        formatted = ""
        for idx, result in enumerate(results, 1):
            formatted += f"\n[Result {idx}]\n"
            formatted += f"{result}\n"
            formatted += "-" * 60 + "\n"
        return formatted


def main():
    """Main function for testing the agent."""
    print("\n🤖 Initializing ReAct Research Copilot...\n")
    agent = ReActAgent()
    
    print("💬 Ask your research questions (type 'exit' to quit)\n")
    
    while True:
        user_input = input("📝 Your question: ").strip()
        
        if user_input.lower() == 'exit':
            print("\n👋 Thank you for using ReAct Research Copilot!")
            break
        
        if not user_input:
            print("Please enter a question.\n")
            continue
        
        response = agent.query(user_input)
        print(response)


if __name__ == "__main__":
    main()