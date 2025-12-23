import os
import json
import re
import requests

class AIBrain:
    """AI-powered decision engine using HuggingFace API"""
    
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        self.system_prompt = """You are an expert video editor AI assistant.
Analyze the user's editing request and create a JSON editing plan.

Available operations:
- remove_fillers: Remove um, uh, ah, etc.
- remove_silence: Cut silent parts
- enhance_audio: Noise reduction & normalization
- add_subtitles: Add animated subtitles (params: style - "mrbeast" or "standard")
- add_music: Background music (params: volume - 0.0 to 1.0)
- speed_adjust: Change playback speed (params: speed - 0.5 to 2.0)

Return ONLY valid JSON:
{
    "operations": [
        {"name": "remove_fillers", "priority": 1, "params": {}},
        {"name": "add_subtitles", "priority": 2, "params": {"style": "mrbeast"}}
    ],
    "explanation": "Brief explanation"
}

Priority: 1 = first, higher numbers = later."""
    
    async def analyze_request(self, user_prompt: str, video_metadata: dict) -> dict:
        """Analyze user request and generate editing plan"""
        try:
            if self.api_key:
                return await self._call_huggingface_api(user_prompt, video_metadata)
            else:
                print("⚠️  No HUGGINGFACE_API_KEY found, using fallback")
                return self._fallback_analysis(user_prompt)
        except Exception as e:
            print(f"⚠️  AI analysis failed: {e}, using fallback")
            return self._fallback_analysis(user_prompt)
    
    async def _call_huggingface_api(self, prompt: str, metadata: dict) -> dict:
        """Call HuggingFace API for intelligent analysis"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            full_prompt = f"""{self.system_prompt}

Video Details:
Duration: {metadata.get('duration', 'unknown')}s
Resolution: {metadata.get('resolution', 'unknown')}
FPS: {metadata.get('fps', 'unknown')}

User Request: {prompt}

Generate the editing plan in JSON format ONLY. No other text."""
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "return_full_text": False
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract text from response
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                else:
                    generated_text = str(result)
                
                # Try to extract JSON from the response
                json_match = re.search(r'\{.*\}', generated_text, re.DOTALL)
                
                if json_match:
                    plan = json.loads(json_match.group())
                    print(f"✅ AI Brain generated plan with {len(plan.get('operations', []))} operations")
                    return plan
                else:
                    print("⚠️  Could not parse AI response, using fallback")
                    return self._fallback_analysis(prompt)
            
            elif response.status_code == 503:
                print("⚠️  Model is loading, using fallback")
                return self._fallback_analysis(prompt)
            
            else:
                print(f"⚠️  HuggingFace API error: {response.status_code}")
                return self._fallback_analysis(prompt)
        
        except Exception as e:
            print(f"⚠️  HuggingFace API error: {e}")
            return self._fallback_analysis(prompt)
    
    def _fallback_analysis(self, prompt: str) -> dict:
        """Rule-based fallback when AI unavailable"""
        operations = []
        priority = 1
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["filler", "um", "uh", "ah"]):
            operations.append({
                "name": "remove_fillers",
                "priority": priority,
                "params": {}
            })
            priority += 1
        
        if any(word in prompt_lower for word in ["silence", "pause", "quiet"]):
            operations.append({
                "name": "remove_silence",
                "priority": priority,
                "params": {}
            })
            priority += 1
        
        if any(word in prompt_lower for word in ["clean", "audio", "noise", "enhance"]):
            operations.append({
                "name": "enhance_audio",
                "priority": priority,
                "params": {}
            })
            priority += 1
        
        if any(word in prompt_lower for word in ["subtitle", "caption", "text"]):
            style = "mrbeast" if "mrbeast" in prompt_lower else "standard"
            operations.append({
                "name": "add_subtitles",
                "priority": priority,
                "params": {"style": style}
            })
            priority += 1
        
        if any(word in prompt_lower for word in ["music", "background", "audio track"]):
            operations.append({
                "name": "add_music",
                "priority": priority,
                "params": {"volume": 0.15}
            })
            priority += 1
        
        if not operations:
            operations = [
                {"name": "remove_fillers", "priority": 1, "params": {}},
                {"name": "enhance_audio", "priority": 2, "params": {}}
            ]
        
        return {
            "operations": operations,
            "explanation": f"Rule-based analysis detected {len(operations)} operations from your request."
        }