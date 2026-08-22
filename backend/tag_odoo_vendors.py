import xmlrpc.client

import os
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get('ODOO_URL', 'https://aqura1.odoo.com')
db = os.environ.get('ODOO_DB', 'aqura1')
username = os.environ.get('ODOO_USERNAME')
password = os.environ.get('ODOO_PASSWORD')

vendor_categories = {
    "Apex Systems": "IT Hardware",
    "Northstar Technologies": "IT Hardware",
    "TechNova Distributors": "Electronics",
    "Vertex Cloud Services": "Cloud Services",
    "Quantum Networking": "Network Gear",
    "Blue Sky SaaS": "Software Licensing",
    "Nexa Security": "Cybersecurity",
    "Orbit Office Solutions": "Office Supplies",
    "Metro Office Furniture": "Furniture",
    "Zenith Facility Services": "Facilities",
    "Sierra Industrial": "Industrial Supplies",
    "Alpha Power Solutions": "Energy",
    "Global Logistics Partners": "Logistics",
    "Synergy Consulting": "Professional Services",
    "Swift Print Media": "Marketing Materials"
}

print(f"Authenticating to {url}...")
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if not uid:
    print("Authentication failed.")
    exit(1)

print(f"Success! UID: {uid}. Tagging vendors...")
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Get or create categories
cat_cache = {}
for v_name, cat_name in vendor_categories.items():
    if cat_name not in cat_cache:
        # Check if category exists
        cat_ids = models.execute_kw(db, uid, password, 'res.partner.category', 'search', [[('name', '=', cat_name)]])
        if cat_ids:
            cat_cache[cat_name] = cat_ids[0]
        else:
            new_cat_id = models.execute_kw(db, uid, password, 'res.partner.category', 'create', [{'name': cat_name}])
            cat_cache[cat_name] = new_cat_id

# Find the vendors and tag them
for v_name, cat_name in vendor_categories.items():
    cat_id = cat_cache[cat_name]
    v_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[('name', '=', v_name)]])
    for v_id in v_ids:
        # Write the many2many category
        models.execute_kw(db, uid, password, 'res.partner', 'write', [[v_id], {'category_id': [(4, cat_id)]}])
        print(f"Tagged '{v_name}' with '{cat_name}'.")

print("\nDone tagging all vendors!")
