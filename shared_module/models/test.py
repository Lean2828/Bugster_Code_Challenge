from pydantic import BaseModel
from typing import List
from models.story import Story
from models.action import Action  # Asegúrate de importar Action

class Test(BaseModel):
    story_id: str
    test_script: str

    @classmethod
    def from_story(cls, story: Story) -> "Test":
        """
        Genera un test de Playwright basado en una historia de usuario.

        Args:
            story (Story): Historia de usuario.

        Returns:
            Test: Instancia del test generado.
        """
        script = cls.generate_script_from_actions(story.actions)
        return cls(story_id=story.id, test_script=script)

    @staticmethod
    def generate_script_from_actions(actions: List[Action]) -> str:
        script_lines = [
            "from playwright.sync_api import sync_playwright",
            "",
            "def test_generated():",
            "    with sync_playwright() as p:",
            "        browser = p.chromium.launch()",
            "        page = browser.new_page()",
        ]

        for action in actions:
            # Usamos atributos de la clase Action en lugar de índices
            if action.type == "input":
                script_lines.append(f"        page.locator('{action.target}').fill('{action.value}')")
            elif action.type == "click":
                script_lines.append(f"        page.locator('{action.target}').click()")
            elif action.type == "navigation":
                script_lines.append(f"        page.goto('{action.url}')")
            else:
                script_lines.append(f"        # Unsupported action: {action.type}")

        script_lines.append("        browser.close()")
        return "\n".join(script_lines)
