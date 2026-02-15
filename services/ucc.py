from typing import List, Dict, Any

class MockUCCProvider:
    """
    Mock provider for UCC (Uniform Commercial Code) filing data.
    Simulates retrieving asset information based on company type.
    """
    
    def __init__(self):
        pass

    def get_ucc_assets(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Returns mock UCC asset data based on the company name.
        """
        # Simple heuristic to make data look somewhat realistic
        name_lower = company_name.lower()
        
        assets = []
        
        if "construction" in name_lower or "contracting" in name_lower:
            assets = [
                {"collateral": "2023 Caterpillar 320 Excavator", "filing_date": "2023-05-12", "status": "Active"},
                {"collateral": "2022 John Deere 410L Backhoe", "filing_date": "2022-11-01", "status": "Active"},
                {"collateral": "Various Hand Tools and Equipment", "filing_date": "2021-03-15", "status": "Active"},
            ]
        elif "tech" in name_lower or "software" in name_lower or "systems" in name_lower:
            assets = [
                {"collateral": "Server Equipment and Networking Hardware", "filing_date": "2024-01-10", "status": "Active"},
                {"collateral": "Intellectual Property Rights - Patent #123456", "filing_date": "2023-06-20", "status": "Active"},
            ]
        elif "transport" in name_lower or "logistics" in name_lower:
            assets = [
                {"collateral": "2024 Freightliner Cascadia", "filing_date": "2024-02-01", "status": "Active"},
                {"collateral": "53' Dry Van Trailer Fleet", "filing_date": "2023-08-15", "status": "Active"},
            ]
        else:
            # Generic fallback
            assets = [
                {"collateral": "Accounts Receivable and Inventory", "filing_date": "2023-01-01", "status": "Active"},
                {"collateral": "Office Furniture and Fixtures", "filing_date": "2022-06-30", "status": "Active"},
            ]
            
        return assets
