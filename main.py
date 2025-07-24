# main.py
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
from tool import search_products, correct_grammar, explain_concept

# --- GLOBAL SCOPE SETUP ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY is not set in .env file!")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

english_grammar_tool = function_tool(correct_grammar)
english_concept_tool = function_tool(explain_concept)
shopping_search_tool = function_tool(search_products) # Keep if needed for other agents


# --- MAIN APPLICATION LOGIC ---
def main():
    print("🎓 Welcome to the English Teacher Agent!")

    english_teacher_agent = Agent(
        name="Teacher English",
        instructions="You are a helpful English teacher. You can correct grammar and explain English concepts. You have access to tools for grammar correction and concept explanation. Always ask the user for the text they want to correct if they express a desire for correction. If the user asks for an explanation, clarify which concept they mean if it's ambiguous. Provide clear and concise answers.",
        model=model,
        tools=[english_grammar_tool, english_concept_tool]
    )

    # --- Conversation Loop ---
    print("\nType 'exit' or 'quit' to end the session.")
    while True:
        user_input = input("\n🗣️ What would you like to learn or correct in English? ")

        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break

        # Run the agent with the user's input
        result = Runner.run_sync(english_teacher_agent, user_input, run_config=config)
        agent_response = result.final_output

        print(f"\n👩‍🏫 Teacher's Response:\n{agent_response}")

if __name__ == "__main__":
    main()