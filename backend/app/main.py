"""
AQURA Procurement Intelligence — FastAPI Backend
================================================
Architecture:
  React Frontend  →  FastAPI (this file)  →  SQLAlchemy  →  Supabase PostgreSQL

When DATABASE_URL is not set the application runs entirely on in-memory demo
data so you can evaluate the full UI without a database.

Run locally:
  uvicorn backend.app.main:app --reload          # from repo root
  uvicorn app.main:app --reload                  # from backend/ directory
"""

from __future__ import annotations

import os
import warnings

# Suppress passlib's bcrypt version-detection warning (cosmetic only).
warnings.filterwarnings("ignore", ".*error reading bcrypt version.*")

from datetime import date, datetime, timedelta, timezone
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from .schemas.vendor_discovery import VendorDiscoveryRequest
from .repositories.vendor_repository import VendorRepository
from .services.vendor_discovery_service import VendorDiscoveryService

# ── Load .env ────────────────────────────────────────────────────────────────
load_dotenv()

# ── Config ───────────────────────────────────────────────────────────────────
APP_ENV                   = os.getenv("APP_ENV", "development")
DEBUG                     = os.getenv("DEBUG", "true").lower() == "true"
JWT_SECRET                = os.getenv("JWT_SECRET", "aqura-dev-secret-change-in-production")
JWT_ALGORITHM             = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
DATABASE_URL              = os.getenv("DATABASE_URL", "")

raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:4173")
CORS_ORIGINS = [o.strip() for o in raw_origins.split(",") if o.strip()]

# ── Password hashing ─────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict[str, Any]) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="AQURA Procurement Intelligence API",
    version="1.0.0",
    description="Backend API for the AQURA procurement intelligence platform.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── In-memory store ───────────────────────────────────────────────────────────
# Replaced by a real database when DATABASE_URL is set (SQLAlchemy layer to be
# added in a follow-up migration). For now, mutations update these lists so the
# demo remains consistent within a single server session.

_hashed_demo_pw = hash_password("password123")

_users: list[dict[str, Any]] = [
    {
        "id": 1,
        "name": "Maya Chen",
        "email": "maya@aqura.demo",
        "hashed_password": _hashed_demo_pw,
        "role": "procurement_manager",
        "department": "Procurement",
        "createdAt": "2026-01-01",
    },
    {
        "id": 2,
        "name": "Aarav Mehta",
        "email": "aarav@aqura.demo",
        "hashed_password": _hashed_demo_pw,
        "role": "employee",
        "department": "Engineering",
        "createdAt": "2026-01-01",
    },
    {
        "id": 3,
        "name": "Kavita Rao",
        "email": "kavita@aqura.demo",
        "hashed_password": _hashed_demo_pw,
        "role": "approver",
        "department": "Finance",
        "createdAt": "2026-01-01",
    },
    {
        "id": 4,
        "name": "Admin User",
        "email": "admin@aqura.demo",
        "hashed_password": _hashed_demo_pw,
        "role": "admin",
        "department": "Operations",
        "createdAt": "2026-01-01",
    },
    {
        "id": 5,
        "name": "Vendor Demo",
        "email": "vendor@aqura.demo",
        "hashed_password": _hashed_demo_pw,
        "role": "vendor",
        "department": "External",
        "createdAt": "2026-01-01",
    },
]

_vendors: list[dict[str, Any]] = [
    {
        "id": 1, "companyName": "Apex Systems", "category": "IT Hardware",
        "location": "Bengaluru, IN", "rating": 4.8, "performance": 94,
        "reliability": 96, "status": "Preferred",
        "contactPerson": "Ravi Menon", "email": "ravi@apex.example",
        "address": "12 Koramangala, Bengaluru 560034",
        "website": "https://apexsystems.example",
        "totalOrders": 128,
    },
    {
        "id": 2, "companyName": "Northstar Technologies", "category": "IT Hardware",
        "location": "Mumbai, IN", "rating": 4.5, "performance": 86,
        "reliability": 82, "status": "Active",
        "contactPerson": "Priya Shah", "email": "priya@northstar.example",
        "address": "45 Bandra Kurla Complex, Mumbai 400051",
        "website": "https://northstartech.example",
        "totalOrders": 64,
    },
    {
        "id": 3, "companyName": "Orbit Office Solutions", "category": "Office Supplies",
        "location": "Pune, IN", "rating": 4.2, "performance": 79,
        "reliability": 78, "status": "Active",
        "contactPerson": "Amit Rao", "email": "amit@orbit.example",
        "address": "88 Hinjewadi Phase 1, Pune 411057",
        "website": "https://orbitsolutions.example",
        "totalOrders": 43,
    },
    {
        "id": 4, "companyName": "Vertex Cloud Services", "category": "Cloud Services",
        "location": "Hyderabad, IN", "rating": 4.7, "performance": 91,
        "reliability": 92, "status": "Preferred",
        "contactPerson": "Neha Iyer", "email": "neha@vertex.example",
        "address": "14 HITEC City, Hyderabad 500081",
        "website": "https://vertexcloud.example",
        "totalOrders": 97,
    },
    {
        "id": 5, "companyName": "Sierra Industrial", "category": "Industrial Supplies",
        "location": "Chennai, IN", "rating": 4.1, "performance": 73,
        "reliability": 70, "status": "Review",
        "contactPerson": "Karan Das", "email": "karan@sierra.example",
        "address": "22 Anna Salai, Chennai 600002",
        "website": "https://sierraindustrial.example",
        "totalOrders": 31,
    },
]

# Demo capability records mirror the fields persisted by the production vendor
# and vendor-product-capability tables. They keep the local fallback fully testable.
_discovery_capabilities = {
    1: (12.9716, 77.5946, 80, 500, 1000, "Business laptop", 20, 800, 44000, 5, True),
    2: (19.0760, 72.8777, 120, 500, 1000, "Business laptop", 20, 1200, 42500, 7, True),
    3: (18.5204, 73.8567, 35, 40, 10, "Ergonomic office chair", 10, 250, 2100, 4, True),
    4: (17.3850, 78.4867, 80, 100, 1, "Cloud observability license", 1, 100, 4500, 2, True),
    5: (13.0827, 80.2707, 50, 10000, 500, "Industrial equipment", 500, 5000, 18500, 9, True),
}
for _vendor in _vendors:
    _latitude, _longitude, _delivery_radius, _available, _minimum, _product_name, _minimum_capacity, _maximum_capacity, _bulk_price, _lead_time, _delivery = _discovery_capabilities[_vendor["id"]]
    _vendor.update({
        "latitude": _latitude, "longitude": _longitude, "country": "India",
        "bulkOrderSupported": True, "minimumOrderQuantity": _minimum,
        "maximumSupplyCapacity": _maximum_capacity, "deliveryRadiusKm": _delivery_radius,
        "averageBulkPrice": _bulk_price,
        "capabilities": [{"productName": _product_name, "productCategory": _vendor["category"], "minimumOrderQuantity": _minimum, "availableQuantity": _available, "maximumOrderCapacity": _maximum_capacity, "bulkPrice": _bulk_price, "unit": "units", "deliveryAvailable": _delivery, "leadTimeDays": _lead_time, "isActive": True}],
        "defaultCapability": {"productName": _product_name, "availableQuantity": _available, "maximumOrderCapacity": _maximum_capacity, "bulkPrice": _bulk_price, "minimumOrderQuantity": _minimum, "deliveryAvailable": _delivery, "leadTimeDays": _lead_time},
    })

_seed_locations = [
    ("Pune BuildMart", "Construction Materials", "Pune", 18.59, 73.74, "Cement", 5000, 30000, 92),
    ("Pune Office Works", "Office Supplies", "Pune", 18.56, 73.78, "Ergonomic office chair", 80, 500, 2150),
    ("Mumbai Industrial Hub", "Industrial Supplies", "Mumbai", 19.12, 72.92, "Industrial equipment", 1000, 15000, 17800),
    ("Mumbai Tech Depot", "IT Hardware", "Mumbai", 19.02, 72.86, "Business laptop", 30, 900, 41800),
    ("Bengaluru Device House", "IT Hardware", "Bengaluru", 12.93, 77.62, "Business laptop", 25, 600, 43500),
    ("Bengaluru Workspace", "Furniture", "Bengaluru", 13.01, 77.56, "Ergonomic office chair", 50, 400, 2050),
    ("Hyderabad Cloud Supply", "Cloud Services", "Hyderabad", 17.44, 78.39, "Cloud observability license", 1, 200, 4300),
    ("Hyderabad Hardware Co", "IT Hardware", "Hyderabad", 17.35, 78.51, "Business laptop", 20, 500, 42750),
    ("Chennai Packworks", "Packaging", "Chennai", 13.06, 80.25, "Packaging boxes", 500, 25000, 18),
    ("Chennai Industrial", "Industrial Supplies", "Chennai", 12.99, 80.21, "Industrial equipment", 250, 8000, 18200),
    ("Delhi Raw Materials", "Raw Materials", "Delhi", 28.63, 77.22, "Cement", 1000, 50000, 89),
    ("Delhi Office Source", "Office Supplies", "Delhi", 28.57, 77.31, "Ergonomic office chair", 20, 700, 1980),
    ("Kolkata Supply Network", "Packaging", "Kolkata", 22.57, 88.39, "Packaging boxes", 200, 12000, 20),
    ("Ahmedabad Material House", "Construction Materials", "Ahmedabad", 23.05, 72.59, "Cement", 500, 40000, 90),
    ("Jaipur Furnishings", "Furniture", "Jaipur", 26.91, 75.79, "Ergonomic office chair", 25, 600, 2025),
]
for _index, (_name, _category, _city, _latitude, _longitude, _product, _minimum, _capacity, _price) in enumerate(_seed_locations, start=6):
    _vendors.append({
        "id": _index, "companyName": _name, "category": _category, "location": f"{_city}, IN", "rating": round(4.0 + (_index % 9) / 10, 1), "performance": 76 + (_index % 22), "reliability": 74 + (_index % 25), "status": "Active", "contactPerson": "Vendor desk", "email": f"desk{_index}@aqura.example", "address": _city, "latitude": _latitude, "longitude": _longitude, "bulkOrderSupported": True, "minimumOrderQuantity": _minimum, "maximumSupplyCapacity": _capacity, "deliveryRadiusKm": 75, "averageBulkPrice": _price,
        "capabilities": [{"productName": _product, "productCategory": _category, "minimumOrderQuantity": _minimum, "availableQuantity": _capacity, "maximumOrderCapacity": _capacity, "bulkPrice": _price, "unit": "units", "deliveryAvailable": True, "leadTimeDays": 2 + (_index % 7), "isActive": True}],
        "defaultCapability": {"productName": _product, "availableQuantity": _capacity, "maximumOrderCapacity": _capacity, "bulkPrice": _price, "minimumOrderQuantity": _minimum, "deliveryAvailable": True, "leadTimeDays": 2 + (_index % 7)},
    })

_vendor_discovery_service = VendorDiscoveryService()
_vendor_repository = VendorRepository(DATABASE_URL)

_requests: list[dict[str, Any]] = [
    {
        "id": 1042, "requestNumber": "PR-1042",
        "title": "Engineering laptops — Q3 refresh",
        "description": "Refresh 20 engineering workstations ahead of Q3 hiring wave. Machines require 32 GB RAM and a discrete GPU.",
        "department": "Engineering", "requester": "Aarav Mehta",
        "priority": "High", "budget": 482000.0,
        "requiredDate": "2026-09-18", "status": "Under review",
        "createdAt": "2026-08-19",
        "items": [
            {"id": 1, "itemName": "Business laptop 32GB", "description": "32 GB RAM, 14-inch, discrete GPU",
             "category": "IT Hardware", "itemType": "Product", "quantity": 20, "unit": "units",
             "estimatedUnitPrice": 24100.0, "total": 482000.0},
        ],
    },
    {
        "id": 1041, "requestNumber": "PR-1041",
        "title": "Cloud observability licenses",
        "description": "Annual renewal of Datadog APM + Logs for 40 services.",
        "department": "Platform", "requester": "Maya Joshi",
        "priority": "Medium", "budget": 186000.0,
        "requiredDate": "2026-09-30", "status": "Approved",
        "createdAt": "2026-08-18",
        "items": [
            {"id": 1, "itemName": "Datadog APM — 40 services 1yr", "description": "",
             "category": "Cloud Services", "itemType": "Service", "quantity": 1, "unit": "license",
             "estimatedUnitPrice": 186000.0, "total": 186000.0},
        ],
    },
    {
        "id": 1040, "requestNumber": "PR-1040",
        "title": "Ergonomic seating — Bengaluru",
        "description": "40 ergonomic chairs for new floor 3 workspace.",
        "department": "People", "requester": "Rohan Kapoor",
        "priority": "Low", "budget": 92000.0,
        "requiredDate": "2026-10-04", "status": "Draft",
        "createdAt": "2026-08-17",
        "items": [
            {"id": 1, "itemName": "Ergonomic office chair", "description": "Lumbar support, adjustable",
             "category": "Office Supplies", "quantity": 40, "unit": "units",
             "estimatedUnitPrice": 2300.0, "total": 92000.0},
        ],
    },
    {
        "id": 1039, "requestNumber": "PR-1039",
        "title": "Network switches for floor 4",
        "description": "48-port managed switches for new floor 4 infrastructure buildout.",
        "department": "IT", "requester": "Ishita Roy",
        "priority": "High", "budget": 274000.0,
        "requiredDate": "2026-09-10", "status": "In vendor selection",
        "createdAt": "2026-08-14",
        "items": [
            {"id": 1, "itemName": "48-port managed switch", "description": "Layer 3, 10G uplinks",
             "category": "IT Hardware", "quantity": 8, "unit": "units",
             "estimatedUnitPrice": 34250.0, "total": 274000.0},
        ],
    },
]

_approvals: list[dict[str, Any]] = [
    {
        "id": 1, "requestNumber": "PR-1042",
        "title": "Engineering laptops — Q3 refresh",
        "requester": "Aarav Mehta", "amount": 482000.0,
        "status": "Pending", "approver": "Kavita Rao",
        "level": 1, "comment": None, "createdAt": "2026-08-19",
    },
    {
        "id": 2, "requestNumber": "PR-1037",
        "title": "Security monitoring renewal",
        "requester": "Dev Patel", "amount": 328000.0,
        "status": "Pending", "approver": "Kavita Rao",
        "level": 1, "comment": None, "createdAt": "2026-08-16",
    },
]

_purchase_orders: list[dict[str, Any]] = [
    {
        "id": 1, "poNumber": "PO-2088", "vendor": "Vertex Cloud Services",
        "requestNumber": "PR-1041", "amount": 186000.0,
        "expectedDelivery": "2026-09-30", "status": "Processing",
        "createdAt": "2026-08-18",
        "subtotal": 186000.0, "tax": 33480.0, "riskLevel": "Low",
        "items": [
            {"id": 1, "itemName": "Datadog APM license", "quantity": 1,
             "unitPrice": 186000.0, "total": 186000.0}
        ],
        "timeline": [
            {"id": 1, "action": "Purchase order created", "actor": "AQURA", "timestamp": "2026-08-18"},
            {"id": 2, "action": "Vendor acknowledged PO", "actor": "Vertex Cloud Services", "timestamp": "2026-08-19"},
        ],
    },
    {
        "id": 2, "poNumber": "PO-2087", "vendor": "Apex Systems",
        "requestNumber": "PR-1039", "amount": 274000.0,
        "expectedDelivery": "2026-09-10", "status": "Shipped",
        "createdAt": "2026-08-14",
        "subtotal": 274000.0, "tax": 49320.0, "riskLevel": "Low",
        "items": [
            {"id": 1, "itemName": "48-port managed switch", "quantity": 8,
             "unitPrice": 34250.0, "total": 274000.0}
        ],
        "timeline": [
            {"id": 1, "action": "Purchase order created", "actor": "AQURA", "timestamp": "2026-08-14"},
            {"id": 2, "action": "Vendor confirmed dispatch", "actor": "Apex Systems", "timestamp": "2026-08-20"},
            {"id": 3, "action": "Shipment picked up by carrier", "actor": "BlueDart Logistics", "timestamp": "2026-08-21"},
        ],
    },
]

_notifications: list[dict[str, Any]] = [
    {
        "id": 1, "title": "Approval required",
        "message": "PR-1042 is waiting for your review.",
        "type": "approval", "isRead": False,
        "createdAt": "2026-08-22T10:00:00",
    },
    {
        "id": 2, "title": "AQURA risk alert",
        "message": "Sierra Industrial has elevated delivery risk on PO-2085.",
        "type": "risk", "isRead": False,
        "createdAt": "2026-08-21T14:30:00",
    },
    {
        "id": 3, "title": "Decision Twin ready",
        "message": "AQURA finished analysing vendor options for PR-1039.",
        "type": "insight", "isRead": True,
        "createdAt": "2026-08-20T09:15:00",
    },
    {
        "id": 4, "title": "Purchase order shipped",
        "message": "PO-2087 has been dispatched by Apex Systems.",
        "type": "info", "isRead": True,
        "createdAt": "2026-08-20T08:00:00",
    },
]


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class RegisterInput(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(min_length=5)
    password: str = Field(min_length=8)
    role: str = "employee"
    department: str = "General"


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict[str, Any]


class PurchaseRequestInput(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    department: str
    priority: str
    requiredDate: str
    items: list[dict[str, Any]] = Field(min_length=1)


class VendorInput(BaseModel):
    companyName: str
    category: str
    location: str
    contactPerson: str = ""
    email: str = ""


class ApprovalAction(BaseModel):
    comment: str = ""


class ChatInput(BaseModel):
    message: str = Field(min_length=1)


class PurchaseOrderInput(BaseModel):
    purchaseRequestId: int
    vendorId: int


class ContactVendorInput(BaseModel):
    message: str = Field(min_length=1)


# ── Auth helpers ──────────────────────────────────────────────────────────────

def _user_public(u: dict[str, Any]) -> dict[str, Any]:
    """Return a user dict without the hashed password."""
    return {k: v for k, v in u.items() if k != "hashed_password"}


def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[dict[str, Any]]:
    """
    Soft auth: returns None when no token is provided (public endpoints can
    call this and get None).  Protected endpoints should use require_user.
    """
    if not token:
        return None
    try:
        payload = decode_token(token)
        user_id: int = int(payload.get("sub", 0))
        user = next((u for u in _users if u["id"] == user_id), None)
        return _user_public(user) if user else None
    except JWTError:
        return None


def check_role(current: dict[str, Any], allowed_roles: list[str]):
    if not current or current.get("role") not in allowed_roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized for this role.")

def require_user(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> dict[str, Any]:
    if current is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current


# ── Vendor comparison / Decision Twin helpers ─────────────────────────────────

def _vendor_options() -> list[dict[str, Any]]:
    return [
        {
            "vendorId": 1, "vendorName": "Apex Systems",
            "quotedPrice": 520000.0, "deliveryDays": 5,
            "pricingScore": 88, "deliveryScore": 91,
            "reliability": 96, "performance": 94,
            "overallScore": 92, "rank": 1,
        },
        {
            "vendorId": 2, "vendorName": "Northstar Technologies",
            "quotedPrice": 498000.0, "deliveryDays": 8,
            "pricingScore": 95, "deliveryScore": 76,
            "reliability": 82, "performance": 86,
            "overallScore": 84, "rank": 2,
        },
        {
            "vendorId": 5, "vendorName": "Sierra Industrial",
            "quotedPrice": 475000.0, "deliveryDays": 12,
            "pricingScore": 100, "deliveryScore": 58,
            "reliability": 70, "performance": 73,
            "overallScore": 72, "rank": 3,
        },
    ]


def _decision_twin_analyses() -> list[dict[str, Any]]:
    """
    AQURA Decision Twin™ — deterministic risk model.

    True Purchase Cost = Quoted Price + Delay Cost + Reliability Risk Cost + Quality Risk Cost
    """
    return [
        {
            "vendorId": 1, "vendorName": "Apex Systems",
            "purchaseCost": 520000.0,
            "deliveryDays": 5,
            "reliability": 96,
            "delayRisk": 8.0,           # % probability of a delivery delay
            "businessImpact": 8000.0,   # estimated ₹ cost of a delay
            "truePurchaseCost": 548000.0,   # 520000 + 8% * 350000 impact
            "confidence": 94,
            "riskLevel": "Low",
            "recommendation": "Recommended — best balance of price, reliability, and schedule certainty.",
        },
        {
            "vendorId": 2, "vendorName": "Northstar Technologies",
            "purchaseCost": 498000.0,
            "deliveryDays": 8,
            "reliability": 82,
            "delayRisk": 24.0,
            "businessImpact": 45000.0,
            "truePurchaseCost": 564000.0,
            "confidence": 84,
            "riskLevel": "Medium",
            "recommendation": "Acceptable — lower quote but moderate reliability reduces margin advantage.",
        },
        {
            "vendorId": 5, "vendorName": "Sierra Industrial",
            "purchaseCost": 475000.0,
            "deliveryDays": 12,
            "reliability": 70,
            "delayRisk": 42.0,
            "businessImpact": 150000.0,
            "truePurchaseCost": 630000.0,
            "confidence": 76,
            "riskLevel": "High",
            "recommendation": "Not recommended — cheapest quote but highest True Purchase Cost due to delay exposure.",
        },
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/api/healthz", tags=["health"], summary="Health check")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "1.0.0", "env": APP_ENV}


# ── Auth ──────────────────────────────────────────────────────────────────────

@app.post("/api/v1/auth/register", tags=["auth"], summary="Register a new user")
def register(payload: RegisterInput) -> dict[str, Any]:
    if any(u["email"] == payload.email for u in _users):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    new_id = max(u["id"] for u in _users) + 1
    user: dict[str, Any] = {
        "id": new_id,
        "name": payload.name,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "role": payload.role,
        "department": payload.department,
        "createdAt": date.today().isoformat(),
    }
    _users.append(user)
    token = create_access_token({"sub": str(new_id), "email": payload.email, "role": payload.role})
    return {"access_token": token, "token_type": "bearer", "user": _user_public(user)}


@app.post("/api/v1/auth/login", tags=["auth"], summary="Log in and receive a JWT")
def login(form: OAuth2PasswordRequestForm = Depends()) -> dict[str, Any]:
    username_clean = (form.username or "").strip().lower()
    user = next((u for u in _users if u["email"].lower() == username_clean), None)
    if not user or not verify_password(form.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": str(user["id"]), "email": user["email"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "user": _user_public(user)}


@app.get("/api/v1/auth/me", tags=["auth"], summary="Get current user profile")
def me(current: dict[str, Any] = Depends(require_user)) -> dict[str, Any]:
    return current


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.get("/api/v1/dashboard", tags=["dashboard"], summary="Get procurement dashboard")
def dashboard(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> dict[str, Any]:
    user_requests = _requests
    user_approvals = _approvals
    user_orders = _purchase_orders
    
    if current and current.get("role") == "employee":
        user_requests = [r for r in _requests if r.get("requester") == current.get("name")]
        user_approvals = []
        user_orders = []
        
    return {
        "metrics": {
            "activeRequests": len(user_requests),
            "pendingApprovals": len([a for a in user_approvals if a["status"] == "Pending"]),
            "activeOrders": len(user_orders),
            "totalSpend": sum(o["amount"] for o in user_orders),
        },
        "monthlySpend": [
            {"month": m, "amount": a}
            for m, a in zip(
                ["Mar", "Apr", "May", "Jun", "Jul", "Aug"],
                [310000, 428000, 375000, 522000, 468000, 615000],
            )
        ],
        "requestsByStatus": [
            {"status": s, "count": len([r for r in _requests if r["status"] == s])}
            for s in {"Approved", "Under review", "Draft", "In vendor selection"}
        ],
        "recentRequests": [
            {k: v for k, v in r.items() if k != "items"} for r in _requests[:5]
        ],
        "insights": [
            {
                "id": 1, "kind": "risk",
                "title": "Apex Systems delivery signal improved",
                "detail": "Reliability is up 8% over the last 90 days.",
                "tone": "positive",
            },
            {
                "id": 2, "kind": "savings",
                "title": "₹2.4 lakh potential savings identified",
                "detail": "Across 6 current requests with comparable supplier quotes.",
                "tone": "accent",
            },
            {
                "id": 3, "kind": "attention",
                "title": f"PR-{_requests[0]['id']} needs your attention",
                "detail": f"Waiting for approval for 3 days.",
                "tone": "warning",
            },
        ],
    }


# ── Purchase requests ─────────────────────────────────────────────────────────

@app.get("/api/v1/purchase-requests", tags=["purchase-requests"], summary="List purchase requests")
def list_requests(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    current: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    # filter by owner if employee
    if current and current.get("role") == "employee":
        pass # Handled below
    items = [
        r for r in _requests
        if (not search or search.lower() in (r["title"] + r["requestNumber"] + r["department"]).lower())
        and (not status or r["status"].lower() == status.lower())
        and (not current or current.get("role") != "employee" or r.get("requester") == current.get("name"))
    ]
    # Return without nested items for list view
    return {
        "items": [{k: v for k, v in r.items() if k != "items"} for r in items],
        "total": len(items),
        "page": page,
    }


@app.post("/api/v1/purchase-requests", tags=["purchase-requests"], status_code=201, summary="Create a purchase request")
def create_request(
    payload: PurchaseRequestInput,
    current: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    new_id = max(r["id"] for r in _requests) + 1
    budget = sum(
        float(i.get("quantity", 0)) * float(i.get("estimatedUnitPrice", 0))
        for i in payload.items
    )
    items_with_id = [
        {**i, "id": idx + 1, "total": float(i.get("quantity", 0)) * float(i.get("estimatedUnitPrice", 0))}
        for idx, i in enumerate(payload.items)
    ]
    req: dict[str, Any] = {
        "id": new_id,
        "requestNumber": f"PR-{new_id}",
        "title": payload.title,
        "description": payload.description,
        "department": payload.department,
        "requester": current["name"] if current else "You",
        "priority": payload.priority,
        "budget": budget,
        "requiredDate": payload.requiredDate,
        "status": "Draft",
        "createdAt": date.today().isoformat(),
        "items": items_with_id,
    }
    _requests.insert(0, req)
    return {k: v for k, v in req.items() if k != "items"}


@app.get("/api/v1/purchase-requests/{id}", tags=["purchase-requests"], summary="Get purchase request details")
def get_request(
    id: int,
    current: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    pass
    req = next((r for r in _requests if r["id"] == id), None)
    if not req:
        raise HTTPException(404, f"Purchase request {id} not found.")
    related_approvals = [a for a in _approvals if a["requestNumber"] == req["requestNumber"]]
    return {
        **req,
        "approvals": related_approvals,
        "activity": [
            {"id": 1, "action": "Request submitted for review", "actor": req["requester"], "timestamp": req["createdAt"]},
        ],
    }


@app.put("/api/v1/purchase-requests/{id}", tags=["purchase-requests"], summary="Update a purchase request")
def update_request(
    id: int,
    payload: PurchaseRequestInput,
    _: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    req = next((r for r in _requests if r["id"] == id), None)
    if not req:
        raise HTTPException(404, f"Purchase request {id} not found.")
    req.update({
        "title": payload.title,
        "description": payload.description,
        "department": payload.department,
        "priority": payload.priority,
        "requiredDate": payload.requiredDate,
        "items": payload.items,
        "budget": sum(
            float(i.get("quantity", 0)) * float(i.get("estimatedUnitPrice", 0))
            for i in payload.items
        ),
    })
    return {k: v for k, v in req.items() if k != "items"}


@app.delete("/api/v1/purchase-requests/{id}", tags=["purchase-requests"], status_code=204)
def delete_request(id: int, _: dict[str, Any] = Depends(require_user)) -> None:
    global _requests
    if not any(r["id"] == id for r in _requests):
        raise HTTPException(404, f"Purchase request {id} not found.")
    _requests = [r for r in _requests if r["id"] != id]


# ── Approvals ─────────────────────────────────────────────────────────────────

@app.get("/api/v1/approvals", tags=["approvals"], summary="List pending approvals")
def list_approvals(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:
    # In a real app, this would query by current user's approver role
    if current and current.get("role") == "employee":
        return [a for a in _approvals if a.get("requester") == current.get("name")]
    return _approvals


@app.post("/api/v1/approvals/{id}/approve", tags=["approvals"], summary="Approve a request")
def approve_request(
    id: int,
    payload: Optional[ApprovalAction] = None,
    _: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    approval = next((a for a in _approvals if a["id"] == id), None)
    if not approval:
        raise HTTPException(404, f"Approval {id} not found.")
    approval["status"] = "Approved"
    approval["comment"] = payload.comment if payload else ""
    # Sync status on the linked purchase request
    req = next((r for r in _requests if r["requestNumber"] == approval["requestNumber"]), None)
    if req:
        req["status"] = "Approved"
    return approval


@app.post("/api/v1/approvals/{id}/reject", tags=["approvals"], summary="Reject a request")
def reject_request(
    id: int,
    payload: Optional[ApprovalAction] = None,
    _: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    approval = next((a for a in _approvals if a["id"] == id), None)
    if not approval:
        raise HTTPException(404, f"Approval {id} not found.")
    approval["status"] = "Rejected"
    approval["comment"] = payload.comment if payload else ""
    req = next((r for r in _requests if r["requestNumber"] == approval["requestNumber"]), None)
    if req:
        req["status"] = "Rejected"
    return approval


@app.post("/api/v1/approvals/{id}/request-changes", tags=["approvals"], summary="Request changes on an approval")
def request_changes(
    id: int,
    payload: Optional[ApprovalAction] = None,
    _: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    approval = next((a for a in _approvals if a["id"] == id), None)
    if not approval:
        raise HTTPException(404, f"Approval {id} not found.")
    approval["status"] = "Changes requested"
    approval["comment"] = payload.comment if payload else ""
    req = next((r for r in _requests if r["requestNumber"] == approval["requestNumber"]), None)
    if req:
        req["status"] = "Changes requested"
    return approval


# ── Vendors ───────────────────────────────────────────────────────────────────

@app.get("/api/v1/vendors/discover", tags=["vendors"], summary="Discover vendors for a product")
def discover_vendors(
    product: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    _: Optional[dict[str, Any]] = Depends(get_current_user),
) -> list[dict[str, Any]]:
    """
    Deterministic vendor discovery — matches on category and/or product keyword.
    Returns a scored shortlist.  No external API required.
    """
    candidates = list(_vendors)
    if product:
        kw = product.lower()
        candidates = [
            v for v in candidates
            if kw in v["companyName"].lower()
            or kw in v["category"].lower()
            or kw in v.get("address", "").lower()
        ] or candidates  # fall back to full list if no match
    if category:
        candidates = [v for v in candidates if v["category"].lower() == category.lower()] or candidates
    # Sort by performance descending
    candidates = sorted(candidates, key=lambda v: v["performance"], reverse=True)
    return [_vendor_public(v) for v in candidates[:6]]


@app.post("/api/v1/vendors/discover", tags=["vendors"], summary="Discover qualified bulk vendors")
def discover_bulk_vendors(
    payload: VendorDiscoveryRequest,
    _: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    try:
        return _vendor_discovery_service.discover(payload, _vendor_repository.discovery_vendors(_vendors))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.get("/api/v1/vendors", tags=["vendors"], summary="List vendors")
def list_vendors(
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    _: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    items = [
        v for v in _vendors
        if not search or search.lower() in (v["companyName"] + v["category"] + v["location"]).lower()
    ]
    return {"items": [_vendor_public(v) for v in items], "total": len(items), "page": page}


@app.post("/api/v1/vendors", tags=["vendors"], status_code=201, summary="Create a vendor")
def create_vendor(
    payload: VendorInput,
    _: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    vendor: dict[str, Any] = {
        "id": max(v["id"] for v in _vendors) + 1,
        "companyName": payload.companyName,
        "category": payload.category,
        "location": payload.location,
        "contactPerson": payload.contactPerson,
        "email": payload.email,
        "address": payload.location,
        "website": "",
        "rating": 0.0,
        "performance": 0.0,
        "reliability": 0.0,
        "totalOrders": 0,
        "status": "New",
    }
    _vendors.append(vendor)
    return _vendor_public(vendor)


@app.get("/api/v1/vendors/{id}", tags=["vendors"], summary="Get vendor details")
def get_vendor(
    id: int,
    current: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    check_role(current, ["procurement_manager", "admin"])
    vendor = next((v for v in _vendors if v["id"] == id), None)
    if not vendor:
        raise HTTPException(404, f"Vendor {id} not found.")
    return {
        **vendor,
        "metrics": [
            {"label": "On-time delivery",    "value": vendor["performance"], "change": 4.2},
            {"label": "Reliability",         "value": vendor["reliability"], "change": 6.1},
            {"label": "Order accuracy",      "value": 97,                   "change": 1.8},
        ],
        "recentActivity": [
            {"id": 1, "action": "Quarterly performance review completed",
             "actor": "AQURA", "timestamp": datetime.now(timezone.utc).isoformat()},
        ],
    }


@app.put("/api/v1/vendors/{id}", tags=["vendors"], summary="Update a vendor")
def update_vendor(
    id: int,
    payload: VendorInput,
    _: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    vendor = next((v for v in _vendors if v["id"] == id), None)
    if not vendor:
        raise HTTPException(404, f"Vendor {id} not found.")
    vendor.update({
        "companyName": payload.companyName,
        "category": payload.category,
        "location": payload.location,
        "contactPerson": payload.contactPerson,
        "email": payload.email,
    })
    return _vendor_public(vendor)


def _vendor_public(v: dict[str, Any]) -> dict[str, Any]:
    return {k: val for k, val in v.items() if k not in {"metrics", "recentActivity"}}


# ── Vendor comparison ─────────────────────────────────────────────────────────

@app.get("/api/v1/vendor-comparisons/{purchaseRequestId}", tags=["intelligence"], summary="Compare vendors for a purchase request")
def comparison(
    purchaseRequestId: int,
    current: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    check_role(current, ["procurement_manager", "admin"])
    req = next((r for r in _requests if r["id"] == purchaseRequestId), None)
    req_number = req["requestNumber"] if req else f"PR-{purchaseRequestId}"
    return {
        "requestNumber": req_number,
        "vendors": _vendor_options(),
        "recommendedVendorId": 1,
        "riskReduction": 42,
        "confidence": 94,
    }


# ── Decision Twin ─────────────────────────────────────────────────────────────

@app.get("/api/v1/decision-twin/{purchaseRequestId}", tags=["intelligence"], summary="Simulate procurement outcomes (Decision Twin)")
def decision_twin(
    purchaseRequestId: int,
    current: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    check_role(current, ["procurement_manager", "admin"])
    req = next((r for r in _requests if r["id"] == purchaseRequestId), None)
    req_number = req["requestNumber"] if req else f"PR-{purchaseRequestId}"
    analyses = _decision_twin_analyses()
    return {
        "requestNumber": req_number,
        "analyses": analyses,
        "recommendedVendorId": 1,
        "riskReduction": 42,
        "confidence": 94,
        "recommendation": "Apex Systems",
        "explanation": (
            "Apex Systems is not the lowest quote, but its 96% reliability score and "
            "5-day delivery window produce the lowest True Purchase Cost (₹5,48,000) and "
            "materially reduce operational schedule risk compared with the cheaper alternatives."
        ),
    }


@app.post("/api/v1/decision-twin/analyze/{purchaseRequestId}", tags=["intelligence"], summary="Re-run Decision Twin analysis")
def rerun_decision_twin(
    purchaseRequestId: int,
    current: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    check_role(current, ["procurement_manager", "admin"])
    return decision_twin(purchaseRequestId)


# ── Purchase orders ───────────────────────────────────────────────────────────

@app.get("/api/v1/purchase-orders", tags=["orders"], summary="List purchase orders")
def list_purchase_orders(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:
    if current and current.get("role") == "employee":
        # Usually POs are linked to PRs, for demo we just filter if needed, 
        # but let's filter if there's a requester match (if we add it to POs)
        return [] # Employees don't own POs directly in this mock unless added
    check_role(current, ["procurement_manager", "approver", "admin"])
    return [{k: v for k, v in o.items() if k not in {"items", "timeline"}} for o in _purchase_orders]


@app.post("/api/v1/purchase-orders", tags=["purchase-orders"], status_code=201, summary="Create a purchase order")
def create_purchase_order(
    payload: PurchaseOrderInput,
    current: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    check_role(current, ["procurement_manager", "admin"])
    vendor = next((v for v in _vendors if v["id"] == payload.vendorId), _vendors[0])
    req = next((r for r in _requests if r["id"] == payload.purchaseRequestId), _requests[0])
    new_id = max(o["id"] for o in _purchase_orders) + 1
    order: dict[str, Any] = {
        "id": new_id,
        "poNumber": f"PO-{2086 + new_id}",
        "vendor": vendor["companyName"],
        "requestNumber": req["requestNumber"],
        "amount": req["budget"],
        "expectedDelivery": req["requiredDate"],
        "status": "Created",
        "createdAt": date.today().isoformat(),
        "subtotal": req["budget"],
        "tax": round(req["budget"] * 0.18),
        "riskLevel": "Low",
        "items": req.get("items", []),
        "timeline": [
            {"id": 1, "action": "Purchase order created", "actor": current["name"], "timestamp": date.today().isoformat()},
        ],
    }
    _purchase_orders.append(order)
    return {k: v for k, v in order.items() if k not in {"items", "timeline"}}


@app.get("/api/v1/purchase-orders/{id}", tags=["purchase-orders"], summary="Get purchase order detail")
def get_purchase_order(
    id: int,
    current: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    check_role(current, ["procurement_manager", "approver", "admin"])
    order = next((o for o in _purchase_orders if o["id"] == id), None)
    if not order:
        raise HTTPException(404, f"Purchase order {id} not found.")
    return order


@app.put("/api/v1/purchase-orders/{id}", tags=["purchase-orders"], summary="Update purchase order status")
def update_purchase_order(
    id: int,
    payload: dict[str, Any],
    current: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    check_role(current, ["procurement_manager", "approver", "admin"])
    order = next((o for o in _purchase_orders if o["id"] == id), None)
    if not order:
        raise HTTPException(404, f"Purchase order {id} not found.")
    if "status" in payload:
        order["status"] = payload["status"]
    return {k: v for k, v in order.items() if k not in {"items", "timeline"}}


# ── Order tracking ────────────────────────────────────────────────────────────

@app.get("/api/v1/order-tracking", tags=["order-tracking"], summary="Get active order tracking")
def tracking(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:
    check_role(current, ["procurement_manager", "approver", "employee", "admin"])
    return [
        {
            "id": o["id"],
            "poNumber": o["poNumber"],
            "vendor": o["vendor"],
            "status": o["status"],
            "expectedDelivery": o["expectedDelivery"],
            "lastUpdate": o["timeline"][-1]["timestamp"] if o.get("timeline") else o["createdAt"],
            "delayRisk": "High" if o["status"] == "At risk" else "Low",
        }
        for o in _purchase_orders
    ]


@app.post("/api/v1/order-tracking/{purchase_order_id}", tags=["order-tracking"], summary="Update order tracking status")
def update_tracking(
    purchase_order_id: int,
    payload: dict[str, Any],
    current: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    check_role(current, ["procurement_manager", "admin"])
    order = next((o for o in _purchase_orders if o["id"] == purchase_order_id), None)
    if not order:
        raise HTTPException(404, f"Purchase order {purchase_order_id} not found.")
    if "status" in payload:
        order["status"] = payload["status"]
    if "note" in payload:
        new_event = {
            "id": len(order.get("timeline", [])) + 1,
            "action": payload["note"],
            "actor": "AQURA",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        order.setdefault("timeline", []).append(new_event)
    return {"id": order["id"], "poNumber": order["poNumber"], "status": order["status"]}


# ── Vendor performance ────────────────────────────────────────────────────────

@app.get("/api/v1/vendor-performance", tags=["vendor-performance"], summary="Get vendor performance rankings")
def vendor_performance(current: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:
    check_role(current, ["procurement_manager", "admin"])
    return [
        {
            "vendorId": v["id"],
            "vendorName": v["companyName"],
            "onTimeRate": v["performance"],
            "avgDeliveryDays": round(5.2 + (100 - v["performance"]) / 12, 1),
            "priceCompetitiveness": max(60, v["performance"] - 2),
            "accuracy": 97,
            "reliability": v["reliability"],
            "quality": min(99, v["performance"] + 2),
            "overall": v["performance"],
        }
        for v in _vendors
    ]


@app.get("/api/v1/vendor-performance/{vendor_id}", tags=["vendor-performance"], summary="Get individual vendor performance")
def single_vendor_performance(
    vendor_id: int,
    current: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    check_role(current, ["procurement_manager", "admin"])
    vendor = next((v for v in _vendors if v["id"] == vendor_id), None)
    if not vendor:
        raise HTTPException(404, f"Vendor {vendor_id} not found.")
    return {
        "vendorId": vendor["id"],
        "vendorName": vendor["companyName"],
        "onTimeRate": vendor["performance"],
        "avgDeliveryDays": round(5.2 + (100 - vendor["performance"]) / 12, 1),
        "priceCompetitiveness": max(60, vendor["performance"] - 2),
        "accuracy": 97,
        "reliability": vendor["reliability"],
        "quality": min(99, vendor["performance"] + 2),
        "overall": vendor["performance"],
    }


# ── Analytics ─────────────────────────────────────────────────────────────────

@app.get("/api/v1/analytics", tags=["analytics"], summary="Get analytics")
def analytics(_: Optional[dict[str, Any]] = Depends(get_current_user)) -> dict[str, Any]:
    return {
        "monthlySpend": [
            {"month": m, "amount": a}
            for m, a in zip(
                ["Mar", "Apr", "May", "Jun", "Jul", "Aug"],
                [310000, 428000, 375000, 522000, 468000, 615000],
            )
        ],
        "categorySpend": [
            {"category": c, "amount": a}
            for c, a in [
                ("IT Hardware", 980000),
                ("Cloud", 620000),
                ("Office", 340000),
                ("Services", 290000),
            ]
        ],
        "topVendors": [
            {"vendorId": v["id"], "vendorName": v["companyName"], "spend": v["totalOrders"] * 50000}
            for v in sorted(_vendors, key=lambda x: x["performance"], reverse=True)[:5]
        ],
        "processingTime": 2.4,
        "approvalTime": 1.2,
        "completionRate": 87,
    }


# ── Notifications ─────────────────────────────────────────────────────────────

@app.get("/api/v1/notifications", tags=["notifications"], summary="List notifications")
def list_notifications(_: Optional[dict[str, Any]] = Depends(get_current_user)) -> list[dict[str, Any]]:
    return _notifications


@app.post("/api/v1/notifications/{id}/read", tags=["notifications"], summary="Mark one notification as read")
def mark_notification_read(
    id: int,
    _: dict[str, Any] = Depends(require_user),
) -> dict[str, Any]:
    notif = next((n for n in _notifications if n["id"] == id), None)
    if not notif:
        raise HTTPException(404, f"Notification {id} not found.")
    notif["isRead"] = True
    return notif


@app.post("/api/v1/notifications/read-all", tags=["notifications"], summary="Mark all notifications as read")
def mark_all_read(_: dict[str, Any] = Depends(require_user)) -> list[dict[str, Any]]:
    for n in _notifications:
        n["isRead"] = True
    return _notifications


# ── AI assistant ──────────────────────────────────────────────────────────────

_CONVERSATIONS: list[dict[str, Any]] = []


@app.post("/api/v1/ai/chat", tags=["ai"], summary="Ask AQURA Assistant")
def chat_with_assistant(
    payload: ChatInput,
    _: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    # Mock assistant logic
    message = payload.message.lower()
    response_text = "I'm AQURA Assistant. I can help you understand the signals behind a purchase decision."
    
    if "northstar" in message:
        response_text = "Northstar Systems is not the cheapest option, but its 91 reliability score reduces estimated schedule exposure by 6.2 days for this request."
    elif "risk" in message:
        response_text = "Sierra Industrial has elevated delivery risk based on historical data. Apex Systems provides the most reliable delivery window."
    elif "status" in message or "pr-1048" in message:
        response_text = "PR-1048 (Q3 data center cooling upgrade) is currently Pending approval from Maya Chen. The requested budget is $184,500."
    
    return {"message": response_text}
def ai_chat(
    payload: ChatInput,
    _: Optional[dict[str, Any]] = Depends(get_current_user),
) -> dict[str, Any]:
    q = payload.message.lower()

    # Intent matching — deterministic mock AI
    if any(w in q for w in ["reliab", "trust", "dependab"]):
        answer = (
            "Apex Systems currently leads reliability at 96%, followed by Vertex Cloud Services "
            "at 92%. Sierra Industrial is the weakest performer at 70% — AQURA flags it as high risk."
        )
    elif any(w in q for w in ["pending", "approval", "approve", "queue"]):
        pending = [a for a in _approvals if a["status"] == "Pending"]
        answer = (
            f"You have {len(pending)} pending approval(s). "
            + (f"{pending[0]['requestNumber']} has been waiting the longest." if pending else "")
        )
    elif any(w in q for w in ["spend", "budget", "cost", "money"]):
        total = sum(o["amount"] for o in _purchase_orders)
        answer = f"Total committed spend across active purchase orders is ₹{total:,.0f}."
    elif any(w in q for w in ["vendor", "supplier", "partner"]):
        answer = (
            f"There are {len(_vendors)} vendors in your directory. "
            "Apex Systems and Vertex Cloud Services are your preferred partners."
        )
    elif any(w in q for w in ["decision twin", "twin", "risk", "true cost"]):
        answer = (
            "The AQURA Decision Twin™ calculates True Purchase Cost = Quoted Price + "
            "Predicted Delay Cost + Reliability Risk Cost + Quality Risk Cost. "
            "A cheaper quote is not always the lower-risk purchase."
        )
    elif any(w in q for w in ["order", "po", "deliver", "track"]):
        answer = (
            f"There are {len(_purchase_orders)} active purchase orders. "
            "PO-2087 (Apex Systems) is currently shipped and on track."
        )
    else:
        answer = (
            "I can help with pending approvals, vendor reliability, spend analysis, "
            "order tracking, and Decision Twin risk explanations. What would you like to explore?"
        )

    return {
        "message": answer,
        "suggestions": [
            "Show pending approvals",
            "Which vendor has the best reliability?",
            "What is the True Purchase Cost for PR-1042?",
        ],
        "context": "AQURA procurement workspace",
    }


@app.get("/api/v1/ai/conversations", tags=["ai"], summary="List AI conversations")
def list_conversations(_: dict[str, Any] = Depends(require_user)) -> list[dict[str, Any]]:
    return _CONVERSATIONS


# ── Users (admin) ──────────────────────────────────────────────────────────────

@app.get("/api/v1/users", tags=["users"], summary="List users (admin)")
def list_users(current: dict[str, Any] = Depends(require_user)) -> list[dict[str, Any]]:
    if current.get("role") != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin access required.")
    return [_user_public(u) for u in _users]
