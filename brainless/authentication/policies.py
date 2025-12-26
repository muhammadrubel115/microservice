ROLE_POLICIES = {
    "admin": {
        "can_manage_users",
        "can_view_audit",
        "can_access_all",
    },
    "user": {
        "can_use_app",
    },
    "role1": {
        "can_use_app",
        "can_special_action",
    },
}

def get_permissions_for_role(role: str) -> set[str]:
    return ROLE_POLICIES.get(role, set())
