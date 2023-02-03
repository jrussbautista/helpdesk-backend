from rest_framework import permissions


class IsTicketOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, ticket):
        user_id = request.user.id
        return ticket.created_by_id == user_id
