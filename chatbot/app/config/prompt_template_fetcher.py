import os

class PromptTemplateFetcher:
    def __init__(self, templates_dir: str = "app/config/prompt_templates"):
        self.templates_dir = templates_dir

    def fetch(self, template_name: str) -> str:
        """Fetch the prompt template by name from the templates folder."""
        try:
            template_path = os.path.join(self.templates_dir, f"{template_name}.txt")
            with open(template_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            raise ValueError(f"Prompt template {template_name} not found.")
