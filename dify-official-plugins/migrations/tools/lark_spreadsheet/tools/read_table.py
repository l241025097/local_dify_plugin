from typing import Any
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool
from core.tools.utils.lark_api_utils import LarkRequest


class ReadTableTool(Tool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage:
        app_id = self.runtime.credentials.get("app_id")
        app_secret = self.runtime.credentials.get("app_secret")
        client = LarkRequest(app_id, app_secret)
        spreadsheet_token = tool_parameters.get("spreadsheet_token")
        sheet_id = tool_parameters.get("sheet_id")
        sheet_name = tool_parameters.get("sheet_name")
        num_range = tool_parameters.get("num_range")
        query = tool_parameters.get("query")
        user_id_type = tool_parameters.get("user_id_type", "open_id")
        res = client.read_table(spreadsheet_token, sheet_id, sheet_name, num_range, query, user_id_type)
        return self.create_json_message(res)
