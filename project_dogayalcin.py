import openai
from typing import Dict, TypedDict, Optional
from langgraph.graph import StateGraph

openai.api_key = 'API key'

class GraphState(TypedDict):
    character: Optional[list] = None
    setting: Optional[Dict[str, str]] = None
    grade: Optional[str] = None
    story: Optional[str] = None
    title: Optional[str] = None
    final_story: Optional[str] = None
    image_url: Optional[str] = None  

workflow = StateGraph(GraphState)

def generate_story_node(state):
    characters = state.get("character", [])
    setting = state.get("setting", {})
    grade = state.get("grade", "")

    story_prompt = (
        f"In the depths of a {setting['Environment']} in an {setting['Existence mode']}, "
        f"two aliens met. One was {characters[0]['Appearance']} and {characters[0]['Personality']}. "
        f"The other was {characters[1]['Appearance']} and {characters[1]['Personality']}. "
        f"This story is tailored for {grade} students. How will their adventure unfold?"
        "This is a short story with less then 400 words"
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": story_prompt}
        ],
        max_tokens=600
    )

    story = response.choices[0].message.content.strip()
    return {"story": story}

def generate_title_node(state):
    characters = state.get("character", [])
    setting = state.get("setting", {})

    title_prompt = (
        f"Generate a story title based on the following: Aliens, "
        f"{characters[0]['Appearance']} and {characters[1]['Appearance']}, "
        f"in a {setting['Environment']}."
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": title_prompt}
        ],
        max_tokens=60
    )

    title = response.choices[0].message.content.strip()
    return {"title": title}

def generate_image_node(state):
    story = state.get("story", "")
    grade = state.get("grade", "")

    prompt = f"Create a cover image for this story which is tailored for {grade} students: {story[:100]}..."

    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1, 
        size="1024x1024" 
    )
    
    image_url = response.data[0].url
    state["image_url"] = image_url 
    return state


def final_node(state):
    title = state.get('title', 'No Title Provided')
    story = state.get('story', 'No Story Provided')
    image_url = state.get('image_url', 'No Image URL Provided')

    final_story = f"Title: {title}\n\nStory: {story}\n\nImage: {image_url}"
    return {"final_story": final_story}


workflow.add_node("generate_title", generate_title_node)
workflow.add_node("generate_story", generate_story_node)
workflow.add_node("final_step", final_node)
workflow.add_node("generate_image", generate_image_node)



workflow.add_edge("generate_title", "generate_story")
workflow.add_edge("generate_story", "generate_image")
workflow.add_edge("generate_image", "final_step")


workflow.set_entry_point("generate_title")


app = workflow.compile()


input_data = {
    "Story": {
        "Character": [
            {"Type": "Alien", "Appearance": "Sporty", "Personality": "Cheerful"},
            {"Type": "Alien", "Appearance": "Tall", "Personality": "Brave"}
        ],
        "Setting": {
            "Existence mode": "Imaginary world",
            "Environment": "Forest",
            "Mood": "Peaceful"
        },
        "Grade": "1st Grade"
    }
}

inputs = {
    "character": input_data["Story"]["Character"],
    "setting": input_data["Story"]["Setting"],
    "grade": input_data["Story"]["Grade"]
}


result = app.invoke(inputs)

print("Final Result:\n", result.get('final_story'))
