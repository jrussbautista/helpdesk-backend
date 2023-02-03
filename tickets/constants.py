class TicketStatus:
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

    choices = ((OPEN, "Open"), (IN_PROGRESS, "In progress"), (CLOSED, "closed"))


class TicketPriority:
    NORMAL = "normal"
    MEDIUM = "medium"
    HIGH = "high"
    IMMEDIATE = "immediate"

    choices = (
        (NORMAL, "Normal"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
        (IMMEDIATE, "Immediate"),
    )
