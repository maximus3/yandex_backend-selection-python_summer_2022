from typing import Any


class UpdateSet(set[Any]):
    def add(self, element: Any) -> None:
        if element in self:
            self.remove(element)
        super().add(element)
