from duckduckgo_search import DDGS
from typing import Optional

class HQProvider:
    """
    Provider for finding Company HQ Addresses using web search.
    """
    
    def __init__(self):
        pass

    def get_hq_address(self, company_name: str) -> Optional[str]:
        """
        Searches for the HQ address of the given company.
        """
        query = f"{company_name} headquarters address"
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                
            if not results:
                return "Address not found"
            
            # Simple heuristic: return the snippet of the first result
            # In a real app, we'd use an LLM or specific address parsing logic
            first_result = results[0]
            return f"{first_result['title']} - {first_result['body']}"

        except Exception as e:
            print(f"Error finding HQ address: {e}")
            return "Address lookup failed"

if __name__ == "__main__":
    provider = HQProvider()
    print(provider.get_hq_address("Tesla"))
