import re
from typing import Dict, List, Optional

import requests
from langchain_core.tools import tool

from backend.tools.env import get_env
from backend.tools.schemas import SecFilingsInput, ToolError


class SecEdgarTool:
    def __init__(self) -> None:
        self.ticker_url = "https://www.sec.gov/files/company_tickers.json"
        self.submissions_url = "https://data.sec.gov/submissions"
        self.default_user_agent = "MyFinanceAgent/1.0 (contact@example.com)"

    def _headers(self) -> Dict[str, str]:
        user_agent = get_env("SEC_USER_AGENT") or self.default_user_agent
        return {
            "User-Agent": user_agent,
            "Accept": "application/json",
        }

    @staticmethod
    def _normalize_ticker(ticker: str) -> str:
        return re.sub(r"[^A-Za-z]", "", ticker or "").upper()

    def _get_cik_for_ticker(self, ticker: str) -> Optional[str]:
        response = requests.get(self.ticker_url, headers=self._headers(), timeout=20)
        response.raise_for_status()
        data = response.json()

        normalized = self._normalize_ticker(ticker)
        for row in data.values():
            if str(row.get("ticker", "")).upper() == normalized:
                cik_num = int(row.get("cik_str"))
                return f"{cik_num:010d}"
        return None

    @staticmethod
    def _parse_forms(forms: Optional[str]) -> Optional[set[str]]:
        if not forms:
            return None
        return {f.strip().upper() for f in forms.split(",") if f.strip()}

    def get_recent_filings(self, ticker: str, forms: Optional[str], limit: int) -> dict:
        sec_user_agent = get_env("SEC_USER_AGENT")
        if not sec_user_agent:
            return ToolError(
                ok=False,
                error="SEC_USER_AGENT is not set",
                source="sec_edgar",
            ).model_dump()

        try:
            cik = self._get_cik_for_ticker(ticker)
            if not cik:
                return ToolError(
                    ok=False,
                    error=f"Ticker '{ticker}' not found in SEC ticker mapping",
                    source="sec_edgar",
                ).model_dump()

            submissions_url = f"{self.submissions_url}/CIK{cik}.json"
            response = requests.get(submissions_url, headers=self._headers(), timeout=20)
            response.raise_for_status()
            payload = response.json()

            recent = payload.get("filings", {}).get("recent", {})
            forms_list = recent.get("form", [])
            accession_numbers = recent.get("accessionNumber", [])
            filing_dates = recent.get("filingDate", [])
            primary_docs = recent.get("primaryDocument", [])

            form_filter = self._parse_forms(forms)

            filings: List[dict] = []
            for idx, form in enumerate(forms_list):
                current_form = str(form).upper()
                if form_filter and current_form not in form_filter:
                    continue

                accession = accession_numbers[idx] if idx < len(accession_numbers) else ""
                filed_at = filing_dates[idx] if idx < len(filing_dates) else ""
                primary_doc = primary_docs[idx] if idx < len(primary_docs) else ""
                accession_no_dash = accession.replace("-", "")

                filing_url = (
                    f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_no_dash}/{primary_doc}"
                    if accession and primary_doc
                    else None
                )

                filings.append(
                    {
                        "ticker": self._normalize_ticker(ticker),
                        "cik": cik,
                        "form": current_form,
                        "filing_date": filed_at,
                        "accession_number": accession,
                        "primary_document": primary_doc,
                        "filing_url": filing_url,
                    }
                )

                if len(filings) >= limit:
                    break

            return {
                "ok": True,
                "source": "sec_edgar",
                "ticker": self._normalize_ticker(ticker),
                "cik": cik,
                "filings": filings,
                "used_user_agent": sec_user_agent,
            }
        except Exception as exc:
            return ToolError(
                ok=False,
                error=f"SEC API request failed: {str(exc)}",
                source="sec_edgar",
            ).model_dump()


_sec_tool = SecEdgarTool()


@tool(args_schema=SecFilingsInput)
def get_sec_filings(ticker: str, forms: Optional[str] = None, limit: int = 5) -> dict:
    """Fetch recent SEC EDGAR filings for a US ticker. Requires SEC_USER_AGENT in .env."""
    return _sec_tool.get_recent_filings(ticker=ticker, forms=forms, limit=limit)
