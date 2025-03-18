import requests
import re

def get_joke():
    url = "https://v2.jokeapi.dev/joke/Programming?type=single&safe-mode"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if not data["error"]:
            return data["joke"]
    return None

def update_readme(joke):
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()

        # Define the joke section markers
        start_marker = "<!-- JOKE-START -->"
        end_marker = "<!-- JOKE-END -->"
        
        # Check if markers exist, if not add them before the last section
        if start_marker not in content:
            # Add the joke section before the last section
            joke_section = f"\n\n## 😄 **Daily Programming Joke**\n{start_marker}\n{joke}\n{end_marker}\n"
            if "---" in content:
                last_section_index = content.rindex("---")
                content = content[:last_section_index] + joke_section + "\n---\n" + content[last_section_index:]
            else:
                content += joke_section
        else:
            # Update existing joke
            pattern = f"{start_marker}.*?{end_marker}"
            replacement = f"{start_marker}\n{joke}\n{end_marker}"
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(content)
            
    except Exception as e:
        print(f"Error updating README: {str(e)}")
        raise e

def main():
    joke = get_joke()
    if joke:
        update_readme(joke)
    else:
        print("Failed to fetch joke")
        exit(1)

if __name__ == "__main__":
    main() 