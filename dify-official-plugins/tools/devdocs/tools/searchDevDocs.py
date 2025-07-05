from typing import Any, Generator
import requests
from pydantic import BaseModel, Field
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool


class SearchDevDocsInput(BaseModel):
    doc: str = Field(..., description="The name of the documentation.")
    topic: str = Field(..., description="The path of the section/topic.")


class SearchDevDocsTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invokes the DevDocs search tool with the given user ID and tool parameters.

        Args:
            user_id (str): The ID of the user invoking the tool.
            tool_parameters (dict[str, Any]): The parameters for the tool, including 'doc' and 'topic'.

        Returns:
            ToolInvokeMessage | list[ToolInvokeMessage]: The result of the tool invocation,
             which can be a single message or a list of messages.
        """
        doc = tool_parameters.get("doc", "")
        topic = tool_parameters.get("topic", "")
        if not doc:
            yield self.create_text_message("Please provide the documentation name.")
        if not topic:
            yield self.create_text_message("Please provide the topic path.")
        url = f"https://documents.devdocs.io/{doc}/{topic}.html"
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            yield self.create_text_message(
                self.session.model.summary.invoke(text=content, instruction="")
            )
        else:
            yield self.create_text_message(
                f"Failed to retrieve the documentation. Status code: {response.status_code}"
            )
