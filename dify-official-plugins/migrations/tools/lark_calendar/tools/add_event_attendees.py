from typing import Any
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool
from core.tools.utils.lark_api_utils import LarkRequest


class AddEventAttendeesTool(Tool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage:
        app_id = self.runtime.credentials.get("app_id")
        app_secret = self.runtime.credentials.get("app_secret")
        client = LarkRequest(app_id, app_secret)
        event_id = tool_parameters.get("event_id")
        attendee_phone_or_email = tool_parameters.get("attendee_phone_or_email")
        need_notification = tool_parameters.get("need_notification", True)
        res = client.add_event_attendees(event_id, attendee_phone_or_email, need_notification)
        return self.create_json_message(res)
