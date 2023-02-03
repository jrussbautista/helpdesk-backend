from django.conf import settings
from django.db import models
from projects.models import Project
from tickets import constants


class TicketType(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="types")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(
        TicketType, on_delete=models.CASCADE, related_name="tickets"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tickets"
    )
    status = models.CharField(
        choices=constants.TicketStatus.choices,
        default=constants.TicketStatus.OPEN,
        max_length=100,
    )
    priority = models.CharField(
        choices=constants.TicketPriority.choices,
        default=constants.TicketPriority.NORMAL,
        max_length=100,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_by_tickets",
    )

    # Mutators
    def in_progress(self):
        self.status = constants.TicketStatus.IN_PROGRESS
        self.save()

    def cancel(self):
        self.status = constants.TicketStatus.CANCELLED
        self.save()

    def resolved(self):
        self.status = constants.TicketStatus.RESOLVED
        self.save()
