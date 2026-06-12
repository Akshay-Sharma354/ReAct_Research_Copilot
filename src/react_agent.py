"""
REACT AGENT - Reason, Act, Observe Loop - GROQ VERSION

ReAct = Reasoning + Acting

The agent:
1. REASON: Think about what information is needed
2. ACT: Call a tool (search documents)
3. OBSERVE: See the results
4. REPEAT: Use results to refine next action or generate answer

This version uses Groq API (FREE, super fast!)
"""

import os
from typing import List, Dict, Optional
from groq import Groq

print("✅ ReAct Agent module loaded (Groq version)!")


class ReActAgent:
    """
    ReAct (Reason + Act) agent that can search documents and answer questions.
    Uses Groq API with LLaMA 3.1 model (super fast!)
    """
    
    def __init__(self, retriever, api_key: str = None):
        """
        Initialize the ReAct agent with Groq.
        
        Args:
            retriever: DocumentRetriever instance for searching
            api_key: Groq API key (from .env file or environment)
        """
        self.retriever = retriever
        
        # Get API key
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in .env or environment!")
            self.client = Groq(api_key=api_key)
        
        # Track all steps in the ReAct loop
        self.conversation_history = []
        self.step_count = 0
        self.max_steps = 10  # Prevent infinite loops
        
        # System prompt tells Groq how to behave
        self.system_prompt = """You are a Research Assistant helping answer questions about AI and Machine Learning.

You have access to a tool to search a document corpus. Use the tool when you need information.

IMPORTANT RULES:
1. ALWAYS think about what information you need
2. Use the search tool to find relevant documents
3. Read the search results carefully
4. Provide citations like [Document: filename]
5. Be accurate - don't make up information
6. If you can't find information, say so
7. Keep answers concise but thorough

When you decide to search, format your response like:
ACTION: search
QUERY: [your search query here]

When you have enough information to answer, provide a complete answer with citations."""
    
    def search_documents(self, query: str) -> str:
        """
        Search documents using the retriever.
        
        This is the "ACT" step in ReAct loop.
        
        Args:
            query: What to search for
        
        Returns:
            Formatted search results as a string
        """
        print(f"🔍 Searching for: {query}")
        
        results = self.retriever.search(query, top_k=5)
        
        if not results:
            return "No relevant documents found for this query."
        
        # Format results nicely
        formatted_results = f"Found {len(results)} relevant passages:\n\n"
        
        for i, result in enumerate(results, 1):
            formatted_results += f"[Result {i}] From {result['filename']}\n"
            formatted_results += f"Relevance: {result['similarity']:.1%}\n"
            formatted_results += f"Content: {result['text']}\n"
            formatted_results += "-" * 80 + "\n\n"
        
        return formatted_results
    
    def process_response(self, response_text: str) -> tuple:
        """
        Check if Groq wants to search or answer.
        
        Returns:
            (should_search, search_query)
        """
        # Check if Groq wants to search
        if "ACTION: search" in response_text:
            # Extract the query
            lines = response_text.split('\n')
            for i, line in enumerate(lines):
                if "QUERY:" in line:
                    query = line.replace("QUERY:", "").strip()
                    return True, query
        
        return False, None
    
    def answer_question(self, question: str, verbose: bool = True) -> Dict:
        """
        Answer a question using ReAct loop with Groq.
        
        The agent will:
        1. Think about what it needs
        2. Search documents if needed
        3. Read results
        4. Provide final answer
        
        Args:
            question: The research question
            verbose: Print step-by-step process
        
        Returns:
            Dictionary with answer and metadata
        """
        print("\n" + "="*80)
        print(f"❓ QUESTION: {question}")
        print("="*80 + "\n")
        
        self.step_count = 0
        self.conversation_history = []
        
        # Add the question to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })
        
        final_answer = None
        search_results = []
        
        # ReAct Loop: Keep going until we have an answer
        while self.step_count < self.max_steps:
            self.step_count += 1
            
            if verbose:
                print(f"--- STEP {self.step_count} ---")
            
            # Get Groq's response using llama-3.3-70b-versatile (latest, most powerful)
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Latest LLaMA 3.3 model
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.conversation_history
                ],
                max_tokens=1000,
                temperature=0.3  # Lower temp for consistency
            )
            
            assistant_message = response.choices[0].message.content
            
            if verbose:
                print(f"LLaMA 3.1: {assistant_message[:200]}...")
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Check if Groq wants to search
            should_search, search_query = self.process_response(assistant_message)
            
            if should_search and search_query:
                # Do the search
                if verbose:
                    print(f"🔍 Searching: {search_query}")
                
                search_result = self.search_documents(search_query)
                search_results.append({
                    'query': search_query,
                    'results': search_result
                })
                
                # Add search results to conversation
                self.conversation_history.append({
                    "role": "user",
                    "content": f"Search results for '{search_query}':\n\n{search_result}\n\nNow please provide your answer to the original question using these results."
                })
            else:
                # Groq has provided final answer
                final_answer = assistant_message
                if verbose:
                    print("\n✅ FINAL ANSWER PROVIDED")
                break
        
        if verbose:
            print("="*80)
            print("📝 FINAL ANSWER:")
            print("="*80)
            print(final_answer)
            print("="*80 + "\n")
        
        return {
            'question': question,
            'answer': final_answer,
            'steps': self.step_count,
            'search_queries': [sr['query'] for sr in search_results],
            'search_results_count': len(search_results)
        }


# Example usage
if __name__ == "__main__":
    from retriever import DocumentRetriever
    import os
    from dotenv import load_dotenv
    
    # Load API key from .env
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env file!")
        print("Please add: GROQ_API_KEY=your_key_here")
    else:
        # Create retriever
        retriever = DocumentRetriever()
        
        # Create agent
        agent = ReActAgent(retriever, api_key=api_key)
        
        # Example question
        question = "What are transformers and how do they work?"
        result = agent.answer_question(question)
        
        print(f"\nAnswer generated in {result['steps']} steps")
        print(f"Searches performed: {result['search_results_count']}")