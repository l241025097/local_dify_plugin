from typing import Any, Union
import requests
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool
from collections.abc import Generator

ALPHAVANTAGE_API_URL = "https://www.alphavantage.co/query"


class QueryStockTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        stock_code = tool_parameters.get("code", "")
        if not stock_code:
            yield self.create_text_message("Please tell me your stock code")
        if "api_key" not in self.runtime.credentials or not self.runtime.credentials.get("api_key"):
            yield self.create_text_message("Alpha Vantage API key is required.")
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock_code,
            "outputsize": "compact",
            "datatype": "json",
            "apikey": self.runtime.credentials["api_key"],
        }
        response = requests.get(url=ALPHAVANTAGE_API_URL, params=params)
        response.raise_for_status()
        result = self._handle_response(response.json())
        yield self.create_json_message(result)

    def _handle_response(self, response: dict[str, Any]) -> dict[str, Any]:
        result = response.get("Time Series (Daily)", {})
        if not result:
            return {}
        stock_result = {}
        for k, v in result.items():
            stock_result[k] = {}
            stock_result[k]["open"] = v.get("1. open")
            stock_result[k]["high"] = v.get("2. high")
            stock_result[k]["low"] = v.get("3. low")
            stock_result[k]["close"] = v.get("4. close")
            stock_result[k]["volume"] = v.get("5. volume")
        return stock_result
