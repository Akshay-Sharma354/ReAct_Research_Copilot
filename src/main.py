"""
MAIN.PY - Run the ReAct Research Copilot with Groq

This file brings everything together and runs the agent with Groq API!
FREE, super fast, no quotas!
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our modules
from retriever import DocumentRetriever
from react_agent import ReActAgent


def main():
    """Main function to run the ReAct Research Copilot with Groq."""
    
    print("\n" + "="*80)
    print("🚀 REACT RESEARCH COPILOT - GROQ VERSION")
    print("="*80 + "\n")
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not found in .env file!")
        print("\nTo fix this:")
        print("1. Go to: https://console.groq.com/")
        print("2. Get your API key")
        print("3. Open .env file and add: GROQ_API_KEY=your_key_here")
        print("4. Run this script again")
        sys.exit(1)
    
    print("✅ Groq API Key found!\n")
    
    # Step 1: Create retriever (loads and indexes documents)
    print("📚 Initializing document retriever...")
    try:
        retriever = DocumentRetriever(corpus_path="./corpus")
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        print("Make sure you have a 'corpus' folder with .md or .txt files")
        sys.exit(1)
    
    # Step 2: Create agent
    print("🤖 Initializing ReAct agent with Groq...")
    try:
        agent = ReActAgent(retriever, api_key=api_key)
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        sys.exit(1)
    
    # Step 3: Interactive loop - ask questions!
    print("\n" + "="*80)
    print("💬 Ask your research questions (type 'exit' to quit)")
    print("="*80 + "\n")
    
    while True:
        try:
            # Get question from user
            question = input("📝 Your question: ").strip()
            
            # Check for exit command
            if question.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using ReAct Research Copilot!")
                break
            
            # Skip empty questions
            if not question:
                print("Please enter a question.\n")
                continue
            
            # Answer the question!
            result = agent.answer_question(question, verbose=True)
            
            # Print summary
            print(f"\n📊 Summary:")
            print(f"  - Steps taken: {result['steps']}")
            print(f"  - Searches performed: {result['search_results_count']}")
            if result['search_queries']:
                print(f"  - Search queries: {', '.join(result['search_queries'])}")
            print()
            
        except KeyboardInterrupt:
            # User pressed Ctrl+C
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error processing question: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()