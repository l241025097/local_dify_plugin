import json
from typing import Any, Generator, Union
import requests
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool


class GeocoderTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        base_url = "http://api.tianditu.gov.cn/geocoder"
        keyword = tool_parameters.get("keyword", "")
        if not keyword:
            yield self.create_text_message("Invalid parameter keyword")
            return
        tk = self.runtime.credentials["tianditu_api_key"]
        params = {"keyWord": keyword}
        result = requests.get(
            base_url + "?ds=" + json.dumps(params, ensure_ascii=False) + "&tk=" + tk
        ).json()
        yield self.create_json_message(result)
