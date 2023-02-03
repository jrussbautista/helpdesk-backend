class TicketStatus:
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CANCELLED = "cancelled"
    RESOLVED = "resolved"

    choices = (
        (OPEN, "Open"),
        (IN_PROGRESS, "In progress"),
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
