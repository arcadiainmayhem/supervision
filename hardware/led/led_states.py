from enum import Enum

class LEDState(Enum):
    IDLE = "idle"
    TRIGGERED = "triggered"
    PROCESSING = "processing"
    PRINTING = "printing"
    COMPLETED = "completed"
    ERROR = "error"
    BORED = "bored"
    PROUD = "proud"
    SATAN = "666"