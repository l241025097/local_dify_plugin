from typing import Any
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool
from core.tools.utils.lark_api_utils import LarkRequest


class CreateTableTool(Tool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage:
        app_id = self.runtime.credentials.get("app_id")
        app_secret = self.runtime.credentials.get("app_secret")
        client = LarkRequest(app_id, app_secret)
        app_token = tool_parameters.get("app_token")
        table_name = tool_parameters.get("table_name")
        default_view_name = tool_parameters.get("default_view_name")
        fields = tool_parameters.get("fields")
        res = client.create_table(app_token, table_name, default_view_name, fields)
        return self.create_json_message(res)
