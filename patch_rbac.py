import re
import os

# --- PATCH backend/app/main.py ---
main_path = r'backend/app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    main_code = f.read()

# Add a check_role helper
auth_helpers_str = """
def require_user(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> dict[str, Any]:
"""
new_auth_helpers_str = """
def check_role(current: dict[str, Any], allowed_roles: list[str]):
    if not current or current.get("role") not in allowed_roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized for this role.")

def require_user(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> dict[str, Any]:
"""
if "def check_role(" not in main_code:
    main_code = main_code.replace(auth_helpers_str, new_auth_helpers_str)

# Now inject check_role into endpoints
main_code = main_code.replace(
    'def get_vendor(\n    id: int,\n    _: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:',
    'def get_vendor(\n    id: int,\n    current: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:\n    check_role(current, ["procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def comparison(\n    purchaseRequestId: int,\n    _: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:',
    'def comparison(\n    purchaseRequestId: int,\n    current: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:\n    check_role(current, ["procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def decision_twin(\n    purchaseRequestId: int,\n    _: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:',
    'def decision_twin(\n    purchaseRequestId: int,\n    current: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:\n    check_role(current, ["procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def rerun_decision_twin(\n    purchaseRequestId: int,\n    _: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:',
    'def rerun_decision_twin(\n    purchaseRequestId: int,\n    current: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:\n    check_role(current, ["procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def list_purchase_orders(_: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:',
    'def list_purchase_orders(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:\n    check_role(current, ["procurement_manager", "approver", "admin"])'
)
main_code = main_code.replace(
    'def get_purchase_order(\n    id: int,\n    _: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:',
    'def get_purchase_order(\n    id: int,\n    current: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:\n    check_role(current, ["procurement_manager", "approver", "admin"])'
)
main_code = main_code.replace(
    'def update_purchase_order(\n    id: int,\n    payload: dict[str, Any],\n    _: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:',
    'def update_purchase_order(\n    id: int,\n    payload: dict[str, Any],\n    current: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:\n    check_role(current, ["procurement_manager", "approver", "admin"])'
)
main_code = main_code.replace(
    'def create_purchase_order(\n    payload: PurchaseOrderInput,\n    current: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:',
    'def create_purchase_order(\n    payload: PurchaseOrderInput,\n    current: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:\n    check_role(current, ["procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def tracking(_: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:',
    'def tracking(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:\n    check_role(current, ["procurement_manager", "approver", "employee", "admin"])'
)
main_code = main_code.replace(
    'def update_tracking(\n    purchase_order_id: int,\n    payload: dict[str, Any],\n    _: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:',
    'def update_tracking(\n    purchase_order_id: int,\n    payload: dict[str, Any],\n    current: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:\n    check_role(current, ["procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def vendor_performance(_: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:',
    'def vendor_performance(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:\n    check_role(current, ["procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def single_vendor_performance(\n    vendor_id: int,\n    _: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:',
    'def single_vendor_performance(\n    vendor_id: int,\n    current: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:\n    check_role(current, ["procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def list_requests(\n    search: Optional[str] = Query(None),\n    status: Optional[str] = Query(None),\n    page: int = Query(1, ge=1),\n    _: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:',
    'def list_requests(\n    search: Optional[str] = Query(None),\n    status: Optional[str] = Query(None),\n    page: int = Query(1, ge=1),\n    current: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:\n    # filter by owner if employee\n    if current and current.get("role") == "employee":\n        pass # Handled below'
)
if '# filter by owner if employee' in main_code:
    main_code = main_code.replace(
        'if (not search or search.lower() in (r["title"] + r["requestNumber"] + r["department"]).lower())\n        and (not status or r["status"].lower() == status.lower())',
        'if (not search or search.lower() in (r["title"] + r["requestNumber"] + r["department"]).lower())\n        and (not status or r["status"].lower() == status.lower())\n        and (not current or current.get("role") != "employee" or r.get("requester") == current.get("name"))'
    )
main_code = main_code.replace(
    'def get_request(\n    id: int,\n    _: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:',
    'def get_request(\n    id: int,\n    current: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> dict[str, Any]:\n    pass'
)
main_code = main_code.replace(
    'def list_approvals(\n    search: Optional[str] = Query(None),\n    _: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> list[dict[str, Any]]:',
    'def list_approvals(\n    search: Optional[str] = Query(None),\n    current: Optional[dict[str, Any]] = Depends(get_current_user),\n) -> list[dict[str, Any]]:\n    check_role(current, ["approver", "procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def approve_request(\n    id: int,\n    payload: ApprovalAction,\n    _: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:',
    'def approve_request(\n    id: int,\n    payload: ApprovalAction,\n    current: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:\n    check_role(current, ["approver", "procurement_manager", "admin"])'
)
main_code = main_code.replace(
    'def reject_request(\n    id: int,\n    payload: ApprovalAction,\n    _: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:',
    'def reject_request(\n    id: int,\n    payload: ApprovalAction,\n    current: dict[str, Any] = Depends(require_user),\n) -> dict[str, Any]:\n    check_role(current, ["approver", "procurement_manager", "admin"])'
)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(main_code)
print("Updated main.py")
