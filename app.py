from flask import Flask, send_from_directory
import os
import markdown

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/output")
def output():
    results = {}
    agents = ["architect", "coder", "tester"]
    for agent in agents:
        path = f"output/{agent}.md"
        if os.path.exists(path):
            with open(path, "r") as f:
                results[agent] = markdown.markdown(f.read(), extensions=["fenced_code"])
    return results

@app.route("/preview")
def preview():
    if os.path.exists("output/coder.md"):
        with open("output/coder.md", "r") as f:
            content = f.read()
            import re
            match = re.search(r"```html\n(.*?)```", content, re.DOTALL)
            if match:
                return match.group(1)
    return "Ingen HTML output endnu"

if __name__ == "__main__":
    app.run(debug=True)