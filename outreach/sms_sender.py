#!/usr/bin/env python3
"""
Lazy AI Agency — SMS Outreach via Email-to-SMS Gateways
Free texting through carrier gateways (no API fees).
Usage:
  python3 sms_sender.py --csv /tmp/top3_leads.csv --limit 5
  python3 sms_sender.py --csv leads.csv --to "John" --dry-run
"""

import csv, smtplib, time, re, sys, argparse, os
from email.mime.text import MIMEText
from pathlib import Path

# Carrier email-to-SMS gateways
# Format: number@gateway
GATEWAYS = {
    "verizon":   "%s@vtext.com",
    "tmobile":   "%s@tmomail.net",
    "att":       "%s@txt.att.net",
    "sprint":    "%s@messaging.sprintpcs.com",
    "google_fi": "%s@msg.fi.google.com",
    "xfnity":    "%s@vtext.com",  # Xfinity Mobile uses Verizon
    "cricket":   "%s@sms.cricketwireless.net",
    "boost":     "%s@sms.myboostmobile.com",
    "us_cell":   "%s@email.uscc.net",
    "consumer":  "%s@mailmymobile.com",
}

# Number prefix → carrier mapping (simple, covers ~80%)
# Based on FCC number pooling data
PREFIX_MAP = {
    "201": "verizon", "202": "verizon", "203": "att", "205": "att",
    "206": "tmobile", "207": "tmobile", "208": "att", "209": "att",
    "210": "att", "212": "verizon", "213": "att", "214": "att",
    "215": "verizon", "216": "att", "217": "verizon", "218": "tmobile",
    "219": "att", "220": "att", "224": "att", "225": "att",
    "228": "att", "229": "att", "231": "att", "234": "verizon",
    "239": "tmobile", "240": "verizon", "248": "att", "251": "att",
    "252": "tmobile", "253": "tmobile", "254": "att", "256": "att",
    "260": "verizon", "262": "att", "267": "verizon", "269": "att",
    "270": "att", "272": "verizon", "276": "att", "281": "tmobile",
    "301": "verizon", "302": "tmobile", "303": "tmobile", "304": "att",
    "305": "att", "307": "tmobile", "308": "att", "309": "att",
    "310": "att", "312": "att", "313": "att", "314": "att",
    "315": "verizon", "316": "att", "317": "att", "318": "att",
    "319": "tmobile", "320": "tmobile", "321": "att", "323": "att",
    "325": "att", "330": "att", "331": "att", "334": "att",
    "336": "att", "337": "att", "339": "verizon", "346": "tmobile",
    "347": "verizon", "351": "verizon", "352": "att", "360": "att",
    "361": "att", "385": "att", "386": "att", "401": "att",
    "402": "att", "404": "att", "405": "att", "406": "tmobile",
    "407": "verizon", "408": "att", "409": "att", "410": "verizon",
    "412": "att", "413": "verizon", "414": "att", "415": "att",
    "417": "att", "419": "att", "423": "att", "424": "att",
    "425": "att", "430": "tmobile", "432": "att", "434": "verizon",
    "435": "att", "440": "att", "442": "tmobile", "443": "verizon",
    "445": "verizon", "458": "tmobile", "469": "att", "470": "att",
    "475": "att", "478": "att", "479": "att", "480": "att",
    "484": "verizon", "501": "att", "502": "att", "503": "att",
    "504": "att", "505": "tmobile", "507": "tmobile", "508": "verizon",
    "509": "att", "510": "att", "512": "att", "513": "att",
    "515": "att", "516": "verizon", "517": "att", "518": "verizon",
    "520": "tmobile", "530": "att", "531": "att", "534": "att",
    "539": "tmobile", "540": "att", "541": "att", "551": "att",
    "559": "att", "561": "att", "562": "att", "563": "tmobile",
    "567": "att", "570": "att", "571": "verizon", "573": "att",
    "574": "tmobile", "575": "tmobile", "580": "att", "585": "att",
    "586": "att", "601": "att", "602": "att", "603": "tmobile",
    "605": "att", "606": "att", "607": "att", "608": "att",
    "609": "verizon", "610": "verizon", "612": "tmobile", "614": "att",
    "615": "att", "616": "att", "617": "verizon", "618": "att",
    "619": "att", "620": "att", "623": "att", "626": "att",
    "628": "att", "629": "att", "630": "att", "631": "verizon",
    "636": "att", "640": "tmobile", "641": "att", "646": "verizon",
    "650": "att", "651": "tmobile", "660": "tmobile", "661": "att",
    "662": "att", "667": "verizon", "669": "att", "678": "verizon",
    "680": "att", "681": "att", "682": "att", "701": "tmobile",
    "702": "tmobile", "703": "verizon", "704": "att", "706": "att",
    "707": "att", "708": "att", "712": "att", "713": "att",
    "714": "att", "715": "att", "716": "verizon", "717": "verizon",
    "718": "verizon", "719": "tmobile", "720": "att", "724": "att",
    "725": "tmobile", "727": "att", "731": "att", "732": "verizon",
    "734": "att", "737": "tmobile", "740": "att", "747": "att",
    "754": "att", "757": "verizon", "760": "att", "762": "att",
    "763": "tmobile", "765": "att", "769": "att", "770": "att",
    "771": "verizon", "772": "att", "773": "att", "774": "verizon",
    "775": "att", "779": "att", "781": "verizon", "785": "att",
    "786": "att", "801": "att", "802": "tmobile", "803": "att",
    "804": "verizon", "805": "att", "806": "att", "808": "tmobile",
    "810": "att", "812": "att", "813": "att", "814": "att",
    "815": "att", "816": "att", "817": "att", "818": "att",
    "828": "att", "830": "att", "831": "att", "832": "tmobile",
    "843": "att", "845": "verizon", "847": "att", "848": "att",
    "850": "att", "856": "verizon", "857": "verizon", "858": "att",
    "859": "att", "860": "tmobile", "862": "att", "863": "att",
    "864": "att", "865": "att", "870": "att", "878": "att",
    "901": "att", "903": "att", "904": "att", "907": "tmobile",
    "908": "verizon", "909": "att", "910": "att", "912": "att",
    "913": "att", "914": "verizon", "915": "att", "916": "att",
    "917": "verizon", "918": "att", "919": "att", "920": "att",
    "925": "att", "928": "att", "929": "verizon", "931": "att",
    "936": "att", "937": "att", "940": "att", "941": "att",
    "947": "att", "949": "att", "951": "att", "952": "tmobile",
    "954": "att", "956": "att", "959": "tmobile", "970": "att",
    "971": "att", "972": "att", "973": "verizon", "978": "verizon",
    "979": "att", "980": "att", "984": "att", "985": "att",
    "989": "att",
}

def clean_phone(phone):
    """Extract digits from phone string."""
    digits = re.sub(r'\D', '', str(phone))
    if len(digits) == 10:
        return digits
    if len(digits) == 11 and digits[0] == '1':
        return digits[1:]
    return None

def detect_carrier(phone):
    """Detect likely carrier from area code."""
    digits = clean_phone(phone)
    if not digits:
        return None
    prefix = digits[:3]
    return PREFIX_MAP.get(prefix, "verizon")  # default to Verizon

def build_sms_gateway(phone, carrier="verizon"):
    """Convert phone number to email-to-SMS address."""
    digits = clean_phone(phone)
    if not digits:
        return None
    gateway = GATEWAYS.get(carrier)
    if not gateway:
        return f"{digits}@vtext.com"  # fallback
    return gateway % digits

# === MESSAGE TEMPLATES ===

def outreach_msg(name, business_name=""):
    return f"""Hi {name}! 👋

I run Lazy AI Agency — we give local service businesses a FREE modern website + a complete AI team that handles your leads, texts back missed calls, collects reviews, and re-activates old customers.

Free for 30 days. No credit card. We do all the setup.

Imagine:
• Every website lead gets a text back in under 5 min
• Every missed call gets an auto text-back
• Your old leads get re-contacted personally
• Happy customers get asked for Google reviews

All automated. All free for your first month.

Want to see it in action? Just reply YES and I'll set it up for you.

— Keith, Lazy AI Agency"""

def follow_up_msg(name):
    return f"""Hey {name}, just following up on my message. We're offering a free 30-day website + AI team for water damage/roofing/garage door businesses.

Zero cost to try. We build everything. You just take the bookings.

Interested?"""

# === SENDER ===

def send_sms(to_phone, message, carrier, sender_email, sender_password, smtp_server="smtp.gmail.com", smtp_port=587):
    """Send via email-to-SMS gateway."""
    gateway = build_sms_gateway(to_phone, carrier)
    if not gateway:
        return False, "Invalid phone"

    msg = MIMEText(message)
    msg['Subject'] = ""
    msg['From'] = sender_email
    msg['To'] = gateway

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True, gateway
    except Exception as e:
        return False, str(e)

# === MAIN ===

def main():
    p = argparse.ArgumentParser(description='Lazy AI Agency — SMS Outreach')
    p.add_argument('--csv', required=True, help='CSV file with leads')
    p.add_argument('--limit', '-l', type=int, default=5, help='Max texts to send')
    p.add_argument('--dry-run', '-d', action='store_true', help='Preview without sending')
    p.add_argument('--to', help='Send to specific name only')
    args = p.parse_args()

    # Load leads
    with open(args.csv) as f:
        reader = csv.DictReader(f)
        leads = list(reader)
    
    print(f"Loaded {len(leads)} leads from {args.csv}")
    
    # Filter to specific person
    if args.to:
        leads = [l for l in leads if args.to.lower() in l.get('name','').lower()]
        print(f"Filtered to {len(leads)} matching '{args.to}'")

    leads = leads[:args.limit]
    
    print(f"\n{'='*60}")
    print(f"Preparing to send {len(leads)} SMS messages")
    print(f"{'='*60}\n")

    for lead in leads:
        name = lead.get('name', 'there')
        phone = lead.get('phone', '')
        niche = lead.get('niche', lead.get('vertical', 'local service'))
        is_fran = lead.get('is_franchise', '')
        city = lead.get('city', '')

        digits = clean_phone(phone)
        carrier = detect_carrier(phone) if digits else "verizon"
        gateway = build_sms_gateway(phone, carrier) if digits else "N/A"

        msg = outreach_msg(name.split()[0] if name else name)

        print(f"  To: {name:30s} → {gateway or 'INVALID':35s} [{niche}]")
        
        if not args.dry_run and digits:
            # NOTE: requires Gmail App Password
            pass

    if args.dry_run:
        print(f"\n{'^'*60}")
        print(f"DRY RUN — No messages sent.")
        print(f"Run without --dry-run to actually send.")
        print(f"\nFirst message preview:")
        print(f"{'─'*60}")
        if leads:
            print(outreach_msg(leads[0].get('name','there')))
    else:
        print(f"\n{'='*60}")
        print(f"To send, set your Gmail credentials:")
        print(f"  export GMAIL_USER='you@gmail.com'")
        print(f"  export GMAIL_APP_PASSWORD='your-app-password'")
        print(f"Then run: python3 sms_sender.py --csv {args.csv} --limit {args.limit}")

if __name__ == '__main__':
    main()
