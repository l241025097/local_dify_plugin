from typing import Any
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool
from core.tools.utils.feishu_api_utils import FeishuRequest


class AddMembersTool(Tool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage:
        app_id = self.runtime.credentials.get("app_id")
        app_secret = self.runtime.credentials.get("app_secret")
        client = FeishuRequest(app_id, app_secret)
        task_guid = tool_parameters.get("task_guid")
        member_phone_or_email = tool_parameters.get("member_phone_or_email")
        member_role = tool_parameters.get("member_role", "follower")
        res = client.add_members(task_guid, member_phone_or_email, member_role)
        return self.create_json_message(res)
