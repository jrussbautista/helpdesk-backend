class TicketStatus:
    OPEN = "open"
    PROCESSING = "processing"
    CANCELLED = "cancelled"
    RESOLVED = "resolved"

    choices = (
        (OPEN, "Open"),
        (PROCESSING, "processing"),
        (CANCELLED, "Cancelled"),
        (RESOLVED, "Resolved"),
    )


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
