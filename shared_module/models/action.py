from pydantic import BaseModel
from typing import Optional


class Action(BaseModel):
    type: str  # Tipo de acción (e.g., input, click, navigation)
    target: Optional[str] = None  # Elemento afectado (e.g., selector CSS)
    value: Optional[str] = None  # Valor ingresado (para inputs)
    url: Optional[str] = None  # URL (para navegaciones)

    def is_login_action(self) -> bool:
        """
        Verifica si esta acción corresponde a un login (ejemplo de patrón).
        """
        return self.type == "input" and self.target and "email" in self.target.lower()

    def is_checkout_navigation(self) -> bool:
        """
        Verifica si esta acción corresponde a una navegación a un checkout.
        """
        return self.type == "navigation" and self.url and "checkout" in self.url.lower()

    def to_test_script_line(self) -> Optional[str]:
        """
        Convierte la acción en una línea de código para un script de test Playwright.
        """
        if self.type == "input":
            return f"page.locator('{self.target}').fill('{self.value}')"
        elif self.type == "click":
            return f"page.locator('{self.target}').click()"
        elif self.type == "navigation":
            return f"page.goto('{self.url}')"
        return None
