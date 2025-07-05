from typing import Any
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool
from core.tools.utils.lark_api_utils import LarkRequest


class CreateEventTool(Tool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage:
        app_id = self.runtime.credentials.get("app_id")
        app_secret = self.runtime.credentials.get("app_secret")
        client = LarkRequest(app_id, app_secret)
        summary = tool_parameters.get("summary")
        description = tool_parameters.get("description")
        start_time = tool_parameters.get("start_time")
        end_time = tool_parameters.get("end_time")
        attendee_ability = tool_parameters.get("attendee_ability")
        need_notification = tool_parameters.get("need_notification", True)
        auto_record = tool_parameters.get("auto_record", False)
        res = client.create_event(
            summary, description, start_time, end_time, attendee_ability, need_notification, auto_record
        )
        return self.create_json_message(res)
