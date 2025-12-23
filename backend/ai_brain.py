import os
import json
import re
import requests


class AIBrain:
    """AI-powered decision engine using Hugging Face Router (Chat Completions)"""

    def __init__(self):
        # ✅ Router-supported free model
        self.model = os.getenv(
            "HF_MODEL",
            "google/gemma-2-2b-it"
        )

        # ✅ CORRECT Router endpoint (OpenAI compatible)
        self.api_url = "https://router.huggingface.co/v1/chat/completions"

        self.api_key = os.getenv("HUGGINGFACE_API_KEY")

        self.system_prompt = """You are an expert video editor AI assistant.
Analyze the user's editing request and create a JSON editing plan.

Available operations:
- remove_fillers
- remove_silence
- enhance_audio
- add_subtitles (style: mrbeast | standard)
- add_music (volume: 0.0 to 1.0)
- speed_adjust (speed: 0.5 to 2.0)

Return ONLY valid JSON:
{
  "operations": [
    {"name": "remove_fillers", "priority": 1, "params": {}}
  ],
  "explanation": "Brief explanation"
}

Do not include any text outside JSON.
"""

    async def analyze_request(self, user_prompt: str, video_metadata: dict) -> dict:
        try:
            if not self.api_key:
                print("⚠️ No HF token found, using fallback")
                return self._fallback_analysis(user_prompt)

            return await self._call_huggingface_api(user_prompt, video_metadata)

        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")
            return self._fallback_analysis(user_prompt)

    async def _call_huggingface_api(self, prompt: str, metadata: dict) -> dict:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            user_message = f"""
Video Details:
Duration: {metadata.get('duration', 'unknown')} seconds
Resolution: {metadata.get('resolution', 'unknown')}
FPS: {metadata.get('fps', 'unknown')}

User Request:
{prompt}

Return JSON ONLY.
"""

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.6,
                "max_tokens": 500
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code != 200:
                print(f"⚠️ HuggingFace API error: {response.status_code}")
                return self._fallback_analysis(prompt)

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if not json_match:
                print("⚠️ JSON parsing failed")
                return self._fallback_analysis(prompt)

            plan = json.loads(json_match.group())
            print(f"✅ AI Brain generated {len(plan.get('operations', []))} operations")
            return plan

        except Exception as e:
            print(f"⚠️ HuggingFace exception: {e}")
            return self._fallback_analysis(prompt)

    def _fallback_analysis(self, prompt: str) -> dict:
        operations = []
        priority = 1
        p = prompt.lower()

        if any(w in p for w in ["filler", "um", "uh", "ah"]):
            operations.append({"name": "remove_fillers", "priority": priority, "params": {}})
            priority += 1

        if any(w in p for w in ["silence", "pause", "quiet"]):
            operations.append({"name": "remove_silence", "priority": priority, "params": {}})
            priority += 1

        if any(w in p for w in ["noise", "audio", "clean", "enhance"]):
            operations.append({"name": "enhance_audio", "priority": priority, "params": {}})
            priority += 1

        if any(w in p for w in ["subtitle", "caption", "text"]):
            operations.append({
                "name": "add_subtitles",
                "priority": priority,
                "params": {"style": "mrbeast" if "mrbeast" in p else "standard"}
            })
            priority += 1

        if any(w in p for w in ["music", "background"]):
            operations.append({
                "name": "add_music",
                "priority": priority,
                "params": {"volume": 0.15}
            })

        if not operations:
            operations = [
                {"name": "remove_fillers", "priority": 1, "params": {}},
                {"name": "enhance_audio", "priority": 2, "params": {}}
            ]

        return {
            "operations": operations,
            "explanation": f"Rule-based analysis detected {len(operations)} operations."
        }
