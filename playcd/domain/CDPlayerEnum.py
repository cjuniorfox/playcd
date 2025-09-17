from enum import Enum

class CDPlayerEnum(Enum):
    REW =   ("rewind"      , "\uf04a", "q", "[Q]")
    PREV =  ("previous"    , "\uf049", "a", "[A]")
    STOP =  ("stop"        , "\uf04d", "s", "[S]")
    PLAY =  ("play"        , "\uf04b", "w", "[W]")
    PAUSE = ("pause"       ,"\uf04c" , " ", "[Space]")
    NEXT =  ("next"        , "\uf050", "d", "[D]")
    FF =    ("fast-forward", "\uf04e", "e", "[E]")
    DISC =  ("eject"       , "\uede9", "x", None)
    QUIT =  ("quit"        , "\uf011", "z", "[Z]")

    def __init__(self, command: str, icon: str, key: str, key_display: str) -> None:
        self.command = command
        self.key = key
        self.key_display = key_display
        self.icon = icon

    @staticmethod
    def from_key(key: str):
        for action in CDPlayerEnum:
            if action.key == key:
                return action
        return None
    
    @staticmethod
    def from_command(command: str):
        for action in CDPlayerEnum:
            if action.command == command:
                return action
        return None
    
    def __str__(self) -> str:
        return self.command
