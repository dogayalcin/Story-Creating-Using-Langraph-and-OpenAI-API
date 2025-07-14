# 📖 AI-Powered Story Generator

This project is a modular **story generation pipeline** built using [LangGraph](https://github.com/langchain-ai/langgraph) and [OpenAI APIs](https://platform.openai.com/docs). It automatically generates a short creative story, a suitable title, and a cover image — all based on user input such as characters, setting, and grade level.

## 🚀 What It Does

- Accepts input with:
  - Two fictional **characters** (appearance & personality)
  - A **setting** (environment, existence mode, mood)
  - A target **grade level**
- Uses OpenAI's **GPT** models to:
  - Generate a story title
  - Write a story (under 400 words)
- Uses **DALL·E** (via OpenAI) to generate a matching cover image
- Assembles everything into a final formatted result

## 🧠 Technologies Used

- 🧱 [LangGraph](https://github.com/langchain-ai/langgraph) — for building modular state-based logic flows
- 🤖 OpenAI GPT-3.5-turbo — for natural language story & title generation
- 🎨 DALL·E 3 — for AI image generation
- 🐍 Python 3.10+
- `TypedDict`, `Dict`, `Optional` — for strict input/output typing

## 🧩 Code Structure

### Nodes

- `generate_title_node`: Creates a creative title based on characters and setting
- `generate_story_node`: Writes the full story for the target grade level
- `generate_image_node`: Generates a cover image using DALL·E
- `final_node`: Combines the title, story, and image URL into a final formatted output

### LangGraph Flow

```text
generate_title ──▶ generate_story ──▶ generate_image ──▶ final_step
