import json
from typing import Any, Generator

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class NominatimReverseTool(Tool):
    def _invoke(
            self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        lat = tool_parameters.get("lat")
        lon = tool_parameters.get("lon")
        if lat is None or lon is None:
            yield self.create_text_message("Please provide both latitude and longitude")
        params = {"lat": lat, "lon": lon, "format": "json", "addressdetails": 1}
        yield self._make_request("reverse", params)

    def _make_request(self, endpoint: str, params: dict) -> ToolInvokeMessage:
        base_url = self.runtime.credentials.get("base_url", "https://nominatim.openstreetmap.org")
        try:
            headers = {"User-Agent": "DifyNominatimTool/1.0"}
            s = requests.session()
            response = s.request(method="GET", headers=headers, url=f"{base_url}/{endpoint}", params=params)
            response_data = response.json()
            if response.status_code == 200:
                s.close()
                return self.create_text_message(
                    self.session.model.summary.invoke(text=json.dumps(response_data, ensure_ascii=False),
                                                      instruction="")
                )
            else:
                return self.create_text_message(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            return self.create_text_message(f"An error occurred: {str(e)}")
