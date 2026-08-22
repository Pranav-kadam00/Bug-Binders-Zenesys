import xmlrpc.client
import time

import os
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get('ODOO_URL', 'https://aqura1.odoo.com')
db = os.environ.get('ODOO_DB', 'aqura1')
username = os.environ.get('ODOO_USERNAME')
password = os.environ.get('ODOO_PASSWORD')

vendors = [
    {"name": "Apex Systems", "city": "Bengaluru", "email": "contact@apexsystems.example", "website": "https://apexsystems.example"},
    {"name": "Northstar Technologies", "city": "Mumbai", "email": "sales@northstar.example", "website": "https://northstartech.example"},
    {"name": "Orbit Office Solutions", "city": "Pune", "email": "hello@orbit.example", "website": "https://orbitsolutions.example"},
    {"name": "Vertex Cloud Services", "city": "Hyderabad", "email": "support@vertexcloud.example", "website": "https://vertexcloud.example"},
    {"name": "Sierra Industrial", "city": "Chennai", "email": "info@sierraindustrial.example", "website": "https://sierraindustrial.example"},
    {"name": "Quantum Networking", "city": "Delhi", "email": "sales@quantumnet.example", "website": "https://quantumnet.example"},
    {"name": "Global Logistics Partners", "city": "Mumbai", "email": "logistics@glp.example", "website": "https://glp.example"},
    {"name": "Nexa Security", "city": "Bengaluru", "email": "security@nexa.example", "website": "https://nexa.example"},
    {"name": "Zenith Facility Services", "city": "Pune", "email": "facilities@zenith.example", "website": "https://zenith.example"},
    {"name": "TechNova Distributors", "city": "Noida", "email": "distro@technova.example", "website": "https://technova.example"},
    {"name": "Alpha Power Solutions", "city": "Hyderabad", "email": "power@alphasolutions.example", "website": "https://alphasolutions.example"},
    {"name": "Synergy Consulting", "city": "Gurugram", "email": "consulting@synergy.example", "website": "https://synergy.example"},
    {"name": "Swift Print Media", "city": "Chennai", "email": "print@swiftmedia.example", "website": "https://swiftmedia.example"},
    {"name": "Blue Sky SaaS", "city": "Bengaluru", "email": "licenses@bluesky.example", "website": "https://bluesky.example"},
    {"name": "Metro Office Furniture", "city": "Mumbai", "email": "sales@metrofurniture.example", "website": "https://metrofurniture.example"}
]

print(f"Authenticating to {url}...")
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if not uid:
    print("Authentication failed.")
    exit(1)

print(f"Success! UID: {uid}. Starting vendor insertion...")
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

success_count = 0
for v in vendors:
    try:
        # Create the partner in Odoo
        record = {
            'name': v['name'],
            'is_company': True,
            'supplier_rank': 1, # This marks them as a vendor
            'city': v['city'],
            'email': v['email'],
            'website': v['website']
        }
        
        new_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [record])
        print(f"Added {v['name']} (ID: {new_id})")
        success_count += 1
        time.sleep(0.2) # Small delay to be gentle on the API
    except Exception as e:
        print(f"Failed to add {v['name']}: {e}")

print(f"\nFinished! Successfully inserted {success_count}/{len(vendors)} vendors into Odoo.")
