import json
from typing import Any, Generator
import requests
from httpx import post
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool


class ExecuteCodeTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        api_key = self.runtime.credentials["X-RapidAPI-Key"]
        url = "https://judge0-ce.p.rapidapi.com/submissions"
        querystring = {"base64_encoded": "false", "fields": "*"}
        headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
        }
        payload = {
            "language_id": tool_parameters["language_id"],
            "source_code": tool_parameters["source_code"],
            "stdin": tool_parameters.get("stdin", ""),
            "expected_output": tool_parameters.get("expected_output", ""),
            "additional_files": tool_parameters.get("additional_files", ""),
        }
        response = post(url, data=json.dumps(payload), headers=headers, params=querystring)
        if response.status_code != 201:
            raise Exception(response.text)
        token = response.json()["token"]
        url = f"https://judge0-ce.p.rapidapi.com/submissions/{token}"
        headers = {"X-RapidAPI-Key": api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            yield self.create_text_message(
                text=f"stdout: {result.get('stdout', '')}\nstderr: {result.get('stderr', '')}\ncompile_output: {result.get('compile_output', '')}\nmessage: {result.get('message', '')}\nstatus: {result['status']['description']}\ntime: {result.get('time', '')} seconds\nmemory: {result.get('memory', '')} bytes"
            )
        else:
            yield self.create_text_message(text=f"Error retrieving submission details: {response.text}")
