from dataclasses import dataclass, field

@dataclass
class Player:
    account: str
    character: str
    helmet_name: str
    helmet_base: str
    display_name: str = field(init= False, default=None)
    ilv: int
    unique: bool
    enchantment: str

    def __post_init__(self):
        self.display_name = self.helmet_name if self.unique else self.helmet_base