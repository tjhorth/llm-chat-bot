# import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()
MODEL = "claude-sonnet-5-5"
SYSTEM = "You are a concie, helpful assistant."


def main():
    messages = []
    print("Chat started. /reset to clear, /exit to quit.")
    while True:
        try:
            user = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user == "/exit":
            break
        if user == "/reset":
            messages.clear()
            continue
        if not user:
            continue

        messages.append({"role": "user", "content": user})
        print("\nbot> ", end="", flush=True)
        with client.messages.stream(model=MODEL, max_tokens=1024, system=SYSTEM, messages=messages) as stream:
            for text in stream.text_stream:
                print(text, end="\n", flush=True)
            final = stream.get_final_message()
        reply = "".join(b.text for b in final.content if b.type == "text")
        messages.append({"role": "assistant", "content": reply})
    print(f"\n[in: {final.usage.input_tokens} / out: {final.usage.output_tokens} tokens]")


if __name__ == "__main__":
    main()