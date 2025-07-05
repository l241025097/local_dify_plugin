from typing import Any, Generator
import requests
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool


class Flux1ProNewTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        headers = {
            "Authorization": f"Key {self.runtime.credentials['fal_api_key']}",
            "Content-Type": "application/json",
        }
        prompt = tool_parameters.get("prompt", "")
        sanitized_prompt = prompt.replace("\\", "")
        payload = {
            "prompt": sanitized_prompt,
            "image_size": tool_parameters.get("image_size", "landscape_4_3"),
            "num_inference_steps": tool_parameters.get("num_inference_steps", 28),
            "guidance_scale": tool_parameters.get("guidance_scale", 3.5),
            "seed": tool_parameters.get("seed"),
            "num_images": tool_parameters.get("num_images", 1),
            "safety_tolerance": tool_parameters.get("safety_tolerance", "2"),
            "sync_mode": tool_parameters.get("sync_mode", False),
        }
        url = "https://fal.run/fal-ai/flux-pro/new"
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            yield self.create_text_message(f"Got Error Response: {response.text}")
        res = response.json()
        result = [self.create_json_message(res)]
        for image_info in res.get("images", []):
            image_url = image_info.get("url")
            if image_url:
                result.append(self.create_image_message(image_url=image_url))
        yield from result