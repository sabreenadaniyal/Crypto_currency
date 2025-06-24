from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
from dotenv import load_dotenv
import chainlit as cl
import os
import requests

# 🔑 Load .env
load_dotenv()
Gemini_Api_Key=os.getenv("GEMINI_API_KEY")

# 🔹 Tool: Get coin price
@function_tool
def get_coin_price(currency):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={currency}"
    response = requests.get(url)
    data = response.json()
    return f"{currency} price is {data} USD"
    

# 🔧 Setup OpenAI Client for Gemini
external_client=AsyncOpenAI(
    api_key=Gemini_Api_Key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)
config=RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled= True
)

# 🤖 Agent setup
agent = Agent(
    name="Digital Coins Agent",
    instructions=
    """
      You are a crypto assistant. Use tools to fetch the latest prices of coins 
      like BTCUSDT, ETHUSDT, and more..
    """,
    tools=[get_coin_price]
)

# #----------------------------
@cl.on_chat_start
async def start_message():
   await cl.Message(content="💰 Welcome to the world of Cryptocurrency! 🚀 Let's get started..").send()
#----------------------------
@cl.on_message
async def my_message(msg: cl.Message):
    user_input = msg.content

    response = Runner.run_sync(agent, user_input,run_config=config)
    await cl.Message(content = response.final_output).send()