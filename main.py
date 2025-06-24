# === Load Required Libraries ===
import asyncio  # For handling async execution
from dotenv import load_dotenv  # To load environment variables from .env file
import os  # For accessing environment variables
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled  # Custom agent classes
import rich  # For colorful console output
from openai.types.responses import ResponseTextDeltaEvent  # Event type for streamed response

# === Load Environment Config ===
load_dotenv()  # Load .env variables (including API key)
set_tracing_disabled(disabled=True)  # Disable agent tracing logs

# === Fetch API Key for OpenRouter ===
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')  # Securely get key from env file

# === Initialize OpenRouter Async Client ===
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url='https://openrouter.ai/api/v1'
)

# === Configure Agent with Instructions and Model ===
agent = Agent(
    name='my agent',  # Agent identifier
    instructions='you are a helpful assistant',  # System prompt or instructions
    model=OpenAIChatCompletionsModel(
        model='deepseek/deepseek-r1:free',  # Specify the OpenRouter model
        openai_client=client  # Pass initialized client
    ),
)

# === Main Async Function to Run Chat ===
async def main():
    # Start streamed chat with a simple user message
    result = Runner.run_streamed(agent, 'hi')

    # Listen to and print streamed events in real-time
    async for event in result.stream_events():
        if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
            rich.print(event.data.delta, end="", flush=True)  # Stream delta token to terminal

# === Run Async Function ===
asyncio.run(main())  # Start the chatbot




