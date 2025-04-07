from typing import Optional, Dict, Any
import os
from groq import Groq
from ..models.ai import AIType, AIResponse, AIRequest

class AIService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "mixtral-8x7b-32768"
        self.system_prompts = {
            AIType.GENERAL: "You are a helpful assistant providing support to users in a chat system.",
            AIType.PSYCHOLOGICAL: "You are a supportive psychological assistant helping users cope with stress and anxiety.",
            AIType.MEDICAL: "You are a medical information assistant providing general health guidance.",
            AIType.LOGISTIC: "You are a logistics assistant helping with evacuation and relocation information."
        }

    async def get_response(self, request: AIRequest) -> AIResponse:
        system_prompt = self.system_prompts.get(request.ai_type, self.system_prompts[AIType.GENERAL])
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ]

        if request.context:
            context_message = f"Context: {request.context}"
            messages.insert(1, {"role": "system", "content": context_message})

        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            stream=False
        )

        response = completion.choices[0].message.content
        confidence = 0.95  # Placeholder confidence score

        return AIResponse(
            content=response,
            confidence=confidence,
            sources=[],  # Add sources if available
            suggested_actions=[]  # Add suggested actions based on the response
        ) 