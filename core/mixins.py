import datetime
from typing import Optional


class AgeMixin:
    """Age property Mixin, needs a birth_date field"""

    @property
    def age(self) -> Optional[int]:
        if self.birth_date:
            today = datetime.date.today()
            return (
                today.year
                - self.birth_date.year
                - (
                    (today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day)
                )
            )
        return None
