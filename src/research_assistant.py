import os
from tavily import TavilyClient
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain
import time


class ResearchAssistant:
    def __init__(self,tavily_api_key):
        self.tavily_client = TavilyClient(api_key = tavily_api_key)
        self.llm = ChatOllama(model="llama2", base_url="http://localhost:11434")


    def search_web(self, query, max_results = 5, search_depth="advanced", include_domains=None):
        try:
            search_params = {
                "query" : query,
                "max_results" : max_results,
                "search_depth" : search_depth,
                "include_answer" : True
            }

            if include_domains:
                search_params["include_domains"] = include_domains
            
            results = self.tavily_client.search(**search_params)
            
            tavily_answer = results.get('answer', '')
            return {
                'results': results['results'],
                'answer': tavily_answer
            }
        except Exception as e:
            print(f"Error searching the web: {e}")
            return {'results': [], 'answer': ''}
    
    def generate_report(self,query,search_results):
        if not search_results:
            return f"No results found for: {query}"
        
        report = f"============================================\n"
        report += f"Research Report on: {query.upper()}\n\n"
        report += f"============================================\n\n"
        report += f"SUMMARY:\n"
        report += f"Found {len(search_results)} relevant sources\n\n"
        report += f"DETAILED FINDINGS:\n"


        for i, result in enumerate(search_results, 1):
            report += f"SOURCE {i}:\n"
            report += f"Title: {result['title']}\n"
            report += f"URL: {result.get('url', 'No URL available')}\n"
            report += f"Content Summary: {result['content'][:300]}...\n\n"
        
        report += "============================================\n"
        report += "END OF REPORT\n"
        return report
    
    def research(self, query):
        print(f"Researching: {query}")

        search_response = self.search_web(query)
        search_results = search_response['results']
        report = self.generate_report(query,search_results)

        return report
    
    def setup_workflow(self):
        class ResearchState(TypedDict):
            query: str
            search_results: list
            draft: str
            final_report: str
        

        workflow = StateGraph(ResearchState)
        workflow.add_node("search", self.search_node)
        workflow.add_node("draft", self.draft_node)
        workflow.add_node("finalize", self.finalize_node)
    
        workflow.set_entry_point("search")
        workflow.add_edge("search", "draft")
        workflow.add_edge("draft", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()

    def search_node(self, state):
        """Agent 1: Search for information"""
        query = state['query']
        print(f"Agent 1: Searching for information on '{query}'")
    
        # Simulate search (replace with actual Tavily search)
        search_results = self.search_web(query)
    
        # Return updated state
        return {"search_results": search_results['results']}

    def draft_node(self, state):
        query = state['query']
        search_results = state['search_results']
        sources_summary = "\n".join(
            [f"Title: {result['title']}, URL: {result.get('url', 'No URL available')}" 
            for result in search_results.get('results', [])]
        )
        prompt_template = ChatPromptTemplate.from_template(
            """
            You are a research assistant. Based on the following search results:
            {sources}
        
            Please create a comprehensive and well-organized draft report for the research query: "{query}".
            """
        )
        llm_chain = LLMChain(llm=self.llm, prompt=prompt_template)
        chain_input = {"query": query, "sources": sources_summary}
        draft = llm_chain.run(chain_input)
        return {"draft": draft}

    def finalize_node(self, state):
        draft = state['draft']
        search_results = state['search_results']
        finalize_prompt = ChatPromptTemplate.from_template(
            """
            You are an expert research analyst. Below is a draft report:
            {draft}
        
            Improve and refine this report. Ensure that the final report is comprehensive and includes additional details based on these sources:
            {sources}
        
            Final Report:
            """
        )
        finalize_chain = LLMChain(llm=self.llm, prompt=finalize_prompt)
        sources_summary = "\n".join(
            [f"Title: {result['title']}, URL: {result.get('url', 'No URL available')}" 
            for result in search_results.get('results', [])]
        )
        chain_input = {"draft": draft, "sources": sources_summary}
        final_report = finalize_chain.run(chain_input)
        return {"final_report": final_report}

    def research_with_agents(self, query):
        workflow = self.setup_workflow()
        result = workflow.invoke({"query": query})
        return result["final_report"]

def main():
    apiKey = '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'
    assistant = ResearchAssistant(apiKey)
    topics = ["Artificial Intelligence Ethics","Climate Change Solutions","Space Exploration 2025"]
    
    for topic in topics:
        print(f"\n\nNEW RESEARCH TOPIC: {topic}")
        print("=" * 50)
        research_report = assistant.research(topic)
        
        filename = f"{topic.replace(' ', '_')}_report.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(research_report)
        
        print(f"Report saved to {filename}")
        print("\nREPORT PREVIEW:")
        print(research_report[:500] + "...\n")


if __name__ == "__main__":
    main()