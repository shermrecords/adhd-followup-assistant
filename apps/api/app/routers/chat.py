from fastapi import APIRouter
from pydantic import BaseModel
from together import Together
import os

router = APIRouter()

class ChatIn(BaseModel):
    patient_id: str
    message: str

# Initialize Together client
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

@router.post("/chat")
async def chat_endpoint(body: ChatIn):
    """
    Chat endpoint that sends patient messages to Together.ai and returns a reply.
    """

    try:
        # Send conversation to Together
        resp = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are an ADHD follow-up assistant for patient {body.patient_id}. "
                        "Respond in a clear, supportive, and practical way. Offer ADHD strategies "
                        "for focus, organization, relationships, and daily life. Write at least 3 sentences."
                    ),
                },
                {"role": "user", "content": body.message},
            ],
            max_tokens=300,
            temperature=0.7,
        )

        print("Together raw response:", resp)

        # ✅ Correct way to access chat completion reply
        reply = resp.choices[0].message.content.strip()

        if not reply:
            reply = "[no reply from model]"

        print("Reply text:", repr(reply))
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"[error: {e}]"}
