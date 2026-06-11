#!/usr/bin/env python3
"""
Lazy AI Agency — Client Onboarding Tool
Generates a custom website + configures AI workers for a new client.

Usage:
  python3 onboard.py --name "Servpro Charleston" --phone "(843) 555-0123" \
    --niche "water" --city "Charleston, SC" --domain servpro-charleston
  python3 onboard.py --interactive
"""

import json, os, sys, argparse, re, shutil, time
from string import Template
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "website-template"
OUTPUT_DIR = BASE_DIR / "clients"

# Default services by niche
SERVICES = {
    "water": [
        ("💧", "Water Extraction", "24/7 emergency water removal from your property. Fast response to prevent mold and structural damage."),
        ("🌀", "Drying & Dehumidification", "Industrial-grade drying equipment to restore your property to pre-damage condition."),
        ("🛡️", "Mold Remediation", "Professional mold inspection, containment, and removal to keep your family safe."),
        ("🔥", "Fire & Smoke Restoration", "Complete fire damage cleanup, smoke removal, and structural restoration."),
    ],
    "garage": [
        ("🔧", "Garage Door Repair", "Fast, professional repair for broken springs, cables, openers, and tracks."),
        ("🆕", "Door Installation", "New garage door installation from top brands. Free consultation and quote."),
        ("🎛️", "Opener Systems", "Smart garage door openers with WiFi, battery backup, and quiet operation."),
        ("🔩", "Preventive Maintenance", "Annual tune-ups to keep your door running smoothly and catch issues early."),
    ],
    "roofing": [
        ("🏠", "Roof Repair", "Fast leak detection and repair. We patch, seal, and restore any roof type."),
        ("🔄", "Roof Replacement", "Complete tear-off and replacement. Shingle, metal, tile, and flat roofs."),
        ("🌪️", "Storm Damage", "Insurance claims assistance for hail, wind, and storm-damaged roofs."),
        ("🔍", "Roof Inspection", "Thorough inspection with drone photography and detailed report."),
    ],
    "fitness": [
        ("🏋️", "Personal Training", "One-on-one coaching tailored to your goals. Results guaranteed."),
        ("👥", "Group Classes", "High-energy group workouts including HIIT, yoga, Pilates, and cycling."),
        ("📋", "Nutrition Coaching", "Custom meal plans and nutrition guidance to maximize your results."),
        ("🎯", "Membership", "Flexible membership plans with no long-term contracts. Try free for 7 days."),
    ],
    "beauty": [
        ("💇", "Hair Styling", "Cuts, color, highlights, blowouts, and extensions by experienced stylists."),
        ("💅", "Nail Services", "Manicure, pedicure, gel, acrylics, and nail art in a relaxing environment."),
        ("✨", "Facials & Skincare", "Custom facials, microdermabrasion, chemical peels, and anti-aging treatments."),
        ("💄", "Makeup", "Professional makeup for everyday, special events, weddings, and photoshoots."),
    ],
    "dental": [
        ("🦷", "General Dentistry", "Cleanings, exams, fillings, and preventive care for the whole family."),
        ("😁", "Cosmetic Dentistry", "Teeth whitening, veneers, bonding, and smile makeovers."),
        ("🦷", "Orthodontics", "Braces, Invisalign, and clear aligners for straight, healthy teeth."),
        ("🦷", "Emergency Dental", "Same-day appointments for toothaches, broken teeth, and dental emergencies."),
    ],
    "auto": [
        ("🔧", "Oil Change", "Full synthetic oil change with multi-point inspection in under 30 minutes."),
        ("🛞", "Brake Service", "Pad replacement, rotor resurfacing, and complete brake system inspection."),
        ("🔩", "Engine Repair", "Diagnostic and repair for check engine lights, overheating, and performance issues."),
        ("🚗", "AC & Heating", "Air conditioning recharge, compressor repair, and heating system service."),
    ],
    "vet": [
        ("🐾", "Wellness Exams", "Annual check-ups, vaccinations, and preventive care for dogs and cats."),
        ("🏥", "Surgery", "Spay/neuter, dental cleaning, and soft tissue surgery by experienced vets."),
        ("🩺", "Emergency Care", "Same-day urgent care for injuries, illness, and pet emergencies."),
        ("✂️", "Grooming", "Bath, haircut, nail trim, and ear cleaning. Gentle handling for anxious pets."),
    ],
    "chiro": [
        ("💆", "Spinal Adjustment", "Gentle, effective chiropractic adjustments to relieve pain and restore mobility."),
        ("🏃", "Sports Therapy", "Injury rehab, performance optimization, and recovery for athletes of all levels."),
        ("🧘", "Massage Therapy", "Deep tissue, sports, and therapeutic massage to complement your adjustment."),
        ("📋", "Wellness Plans", "Custom wellness plans combining adjustment, exercise, and nutrition guidance."),
    ],
}

def parse_phone(phone):
    """Normalize phone to format: (555) 123-4567"""
    d = re.sub(r'\D', '', phone)
    if len(d) == 10:
        return f"({d[:3]}) {d[3:6]}-{d[6:]}"
    if len(d) == 11 and d[0] == '1':
        d = d[1:]
        return f"({d[:3]}) {d[3:6]}-{d[6:]}"
    return phone

def parse_phone_short(phone):
    """Just the last 4 digits for display"""
    d = re.sub(r'\D', '', phone)
    return d[-4:] if d else phone

def slugify(text):
    """Convert to URL-friendly slug."""
    return re.sub(r'[^a-z0-9-]', '', text.lower().replace(' ', '-').replace('--', '-')).strip('-')

def generate_site(client):
    """Generate the client's customized website."""
    niche = client.get('niche', 'water')
    services = SERVICES.get(niche, SERVICES['water'])
    name = client['name']
    city = client.get('city', 'Your City')
    phone = client['phone']
    domain = client.get('domain', slugify(name))

    phone_f = parse_phone(phone)
    phone_s = parse_phone_short(phone)

    # Read template
    template_path = TEMPLATE_DIR / "index.html"
    if not template_path.exists():
        # Fall back to repo root template
        template_path = BASE_DIR / "landing-page" / "index.html"
    
    with open(TEMPLATE_DIR / "index.html") as f:
        html = f.read()

    # Quick replacements (handlebars-style)
    city_name = city.split(',')[0] if city else city
    
    replacements = {
        "{{business_name}}": name,
        "{{tagline}}": f"Professional {services[0][1]} Services in {city_name}",
        "{{meta_description}}": f"Trusted {services[0][1]} services in {city_name}. Free quote. Fast response. Family-owned.",
        "{{phone}}": phone_f,
        "{{phone_short}}": phone_s,
        "{{headline}}": f"Professional {services[0][1]} Services in {city_name}",
        "{{subheadline}}": f"Fast, reliable, and trusted by {city_name} residents. Get a free quote within minutes.",
        "{{city}}": city_name,
        "{{review_count}}": "500+",
        "{{about_text}}": f"At {name}, we've been serving {city_name} and the surrounding area for over 15 years. Our team of certified professionals is committed to providing top-quality service, transparent pricing, and genuine care for every customer. We don't just fix the problem — we make sure it stays fixed.",
        "#contact": "#contact",
        "#services": "#services",
        "#about": "#about",
        "#reviews": "#reviews",
    }

    for old, new in replacements.items():
        html = html.replace(old, new)

    # Build services HTML block
    services_html = ""
    for icon, title, desc in services:
        services_html += f'''
            <div class="service-card" style="cursor:default;">
                <div class="icon" style="font-size:2.5rem;">{icon}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>'''

    # Simple services replacement (remove the handlebars loop)
    service_block_start = '{{#each services}}'
    service_block_end = '{{/each}}'
    pattern_start = html.find(service_block_start)
    if pattern_start >= 0:
        start = html.rfind('<div', 0, pattern_start)
        end = html.find('</div>', html.find(service_block_end)) + len('</div>')
        html = html[:start] + services_html + html[end:]

    # Remove other handlebars
    html = re.sub(r'{{#if [^}]+}}', '', html)
    html = re.sub(r'{{/if}}', '', html)
    html = re.sub(r'{{#each [^}]+}}', '', html)
    html = re.sub(r'{{/each}}', '', html)
    html = re.sub(r'{{[^}]+}}', '', html)

    # Add review testimonials
    reviews_block = '''
            <div class="review-card">
                <div class="stars">★★★★★</div>
                <p>"They showed up within an hour and had the problem fixed. Couldn't believe how fast and professional they were."</p>
                <div class="author">— Michael R., ''' + city_name + '''</div>
            </div>
            <div class="review-card">
                <div class="stars">★★★★★</div>
                <p>"I've used them twice now. Fair prices, great work, and they actually call you back. Rare these days."</p>
                <div class="author">— Sarah T., ''' + city_name + '''</div>
            </div>
            <div class="review-card">
                <div class="stars">★★★★★</div>
                <p>"Saved us thousands compared to the other quote we got. Would recommend to anyone in ''' + city_name + '''."</p>
                <div class="author">— James K., ''' + city_name + '''</div>
            </div>'''
    
    reviews_start = html.find('<div class="reviews-grid">')
    if reviews_start >= 0:
        grid_end = html.find('</div>', html.find('</div>', reviews_start + 30) + 1) + 6
        html = html[:reviews_start + len('<div class="reviews-grid">')] + reviews_block + html[grid_end:]

    # Write output
    client_dir = OUTPUT_DIR / domain
    client_dir.mkdir(parents=True, exist_ok=True)
    
    out_path = client_dir / "index.html"
    with open(out_path, 'w') as f:
        f.write(html)

    # Copy netlify config and function
    if (TEMPLATE_DIR / "netlify.toml").exists():
        shutil.copy(TEMPLATE_DIR / "netlify.toml", client_dir / "netlify.toml")
    
    func_dir = client_dir / "netlify" / "functions"
    func_dir.mkdir(parents=True, exist_ok=True)
    if (TEMPLATE_DIR / "netlify" / "functions" / "lead-capture.js").exists():
        shutil.copy(
            TEMPLATE_DIR / "netlify" / "functions" / "lead-capture.js",
            func_dir / "lead-capture.js"
        )

    return client_dir

def interactive():
    """Interactive onboarding wizard."""
    print("\n" + "="*60)
    print("  Lazy AI Agency — Client Onboarding Wizard")
    print("="*60 + "\n")

    niches = list(SERVICES.keys())
    niche_names = {
        "water": "💧 Water Damage Restoration",
        "garage": "🚪 Garage Door Repair",
        "roofing": "🏠 Roofing",
        "fitness": "🏋️ Fitness / Gym",
        "beauty": "💇 Beauty Salon / Barber",
        "dental": "🦷 Dental",
        "auto": "🔧 Auto Repair",
        "vet": "🐾 Vet & Pet",
        "chiro": "💆 Chiro & PT",
    }

    print("Select their niche:")
    for i, n in enumerate(niches, 1):
        print(f"  {i}. {niche_names.get(n, n)}")
    niche_idx = int(input("\nNumber: ")) - 1
    niche = niches[niche_idx]

    name = input("Business name: ")
    phone = input("Phone: ")
    city = input("City (e.g. 'Charleston, SC'): ")
    domain = input("Domain slug (e.g. 'servpro-charleston'): ") or slugify(name)

    client = {
        "niche": niche,
        "name": name,
        "phone": phone,
        "city": city,
        "domain": domain,
    }

    print(f"\nGenerating site for {name}...")
    out_dir = generate_site(client)
    
    print(f"\n✅ Site generated at: {out_dir}")
    print(f"   Deploy with: cd {out_dir} && npx netlify deploy --prod")
    print(f"\n📋 Client Summary:")
    print(f"   Name:   {name}")
    print(f"   Niche:  {niche_names.get(niche, niche)}")
    print(f"   Phone:  {parse_phone(phone)}")
    print(f"   City:   {city}")
    print(f"   Site:   {out_dir}/index.html")
    print()

def main():
    p = argparse.ArgumentParser(description='Lazy AI Agency — Client Onboarding')
    p.add_argument('--interactive', '-i', action='store_true', help='Interactive wizard')
    p.add_argument('--name', '-n', help='Business name')
    p.add_argument('--niche', choices=list(SERVICES.keys()), default='water', help='Niche')
    p.add_argument('--phone', '-p', help='Phone number')
    p.add_argument('--city', '-c', help='City, State')
    p.add_argument('--domain', '-d', help='URL slug')
    args = p.parse_args()

    if args.interactive or not args.name:
        interactive()
        return

    client = {
        "niche": args.niche,
        "name": args.name,
        "phone": args.phone or "(555) 000-0000",
        "city": args.city or "Your City",
        "domain": args.domain or slugify(args.name),
    }

    print(f"Generating site for {client['name']}...")
    out_dir = generate_site(client)
    print(f"✅ Site generated at: {out_dir}")
    print(f"   Deploy: cd {out_dir} && npx netlify deploy --prod")

if __name__ == '__main__':
    main()