"""
CRUD operations for database models.
Re-exports admin panel CRUD functions from admin_crud.
"""
from admin_crud import (
    create_user,
    create_admin_user,
    get_all_users,
    get_users,
    get_user_by_id,
    get_user,
    update_user_by_id,
    update_user,
    delete_user_by_id,
    delete_user,
    authenticate_admin,
)

