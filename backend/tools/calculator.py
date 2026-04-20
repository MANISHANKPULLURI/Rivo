import math

class FinancialCalculator:
    """
    Knowledge: This class provides exact mathematical calculations.
    It prevents the LLM from 'guessing' numbers.
    """
    
    @staticmethod
    def calculate_pe_ratio(price: float, earnings: float):
        """Standard P/E Calculation: Price / Earnings Per Share"""
        try:
            if earnings == 0:
                return "N/A (Zero Earnings)"
            return round(price / earnings, 2)
        except Exception:
            return "Calculation Error"

    @staticmethod
    def convert_currency(amount: float, rate: float):
        """
        Normalization: Converts INR to USD or vice versa.
        Example: Today's rate is ~92.8 INR per USD.
        """
        return round(amount / rate, 2)

    @staticmethod
    def calculate_cagr(present_value: float, past_value: float, years: int):
        """CAGR: [(Present/Past)^(1/n)] - 1"""
        try:
            cagr = (pow((present_value / past_value), (1 / years)) - 1) * 100
            return f"{round(cagr, 2)}%"
        except Exception:
            return "Error calculating CAGR"