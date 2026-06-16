# SiteSpin Pro / Lazy AI Agency — Outreach Playbook
*Owner-approved. Pricing: $97/mo (Starter). Requires founder approval before sending.*
*Replace [bracketed fields] with real prospect data from Outscraper.*

---

## 1. Cold SMS (Primary channel)

```
Hey [FIRST NAME], noticed [BUSINESS NAME] doesn't have a website yet.
We build done-for-you sites for [TRADE] businesses — free for 30 days.
If you like it, $97/mo to keep it live. No contracts.
Takes 3 min: [LINK]
```

### AI Worker Upsell (for existing website prospects)
```
Hey [FIRST NAME], I see [BUSINESS NAME] has a site — but who follows up
on the leads? We have an AI team that texts back inquiries in <5 min,
recovers missed calls, and collects Google reviews automatically.
Free for 30 days, then $97/mo. Want to see it?
```

---

## 2. Cold Email

**Subject**: Free website for [BUSINESS NAME]

```
Hey [FIRST NAME],

I build custom websites for [TRADE] businesses. Free for 30 days.
If it works, $97/month to keep it live — hosting, updates, support
included. No contracts, cancel anytime.

Built in 48 hours. You see it before you pay anything.

3 questions to apply: [LINK]

Reply if you want me to send them.
```

### Upgrade Pitch (Day 30 follow-up for trial users)
```
Subject: Your site's results — and what's next

Hey [FIRST NAME],

Your free trial ends in 3 days. Here's what happened:
• [X] website visitors
• [X] form submissions
• [X] calls from your site

Want to keep it live? $97/mo.

Want us to handle the leads too? Upgrade to Pro ($497/mo) and
our AI receptionist texts back every missed call + books appointments.

Complete ($2,497/mo) adds our full AI team — outreach, reviews,
marketing, and more.

Reply and I'll set it up.
```

---

## 3. LinkedIn / Instagram DM

```
Hey [FIRST NAME] — I build custom websites for [TRADE] businesses
in 48 hours, free for 30 days. $97/month after if you want to keep
it. No contracts, cancel anytime. Worth a look?
```

---

## 4. Follow-up Sequence

### Day 3

**Subject**: Bumping this — [BUSINESS NAME]

```
Hey [FIRST NAME],

Just bumping this in case it got buried. We still have free website
slots available this month.

Custom site for [BUSINESS NAME]. Built in 48 hours. Free for 30 days.
$97/month to keep it live.

3 questions to apply: [LINK]
```

### Day 7 (final)

**Subject**: Last follow-up — [BUSINESS NAME]

```
Hey [FIRST NAME],

Last one on this. Free site slots for this month are almost gone.

Zero risk — you see the site before paying anything. $97/mo to keep
it live, cancel any time.

Reply and I'll send you the 3 questions: [LINK]
```

**After Day 7**: status = closed_no_response. No further contact.

---

## 5. Social — Short-Form Video Script (30-60 sec)

**Title**: "If your business still doesn't have a website in 2026..."

```
[0:00-0:05] Direct to camera, serious
"If your business doesn't have a website in 2026, you're losing
jobs to competitors who do. Period."

[0:05-0:15] Screen recording — Google search results
"When someone searches 'plumber near me' or 'salon open now',
if you don't show up, your competitor gets the call."

[0:15-0:25] Back to camera
"Most business owners know they need a site. They just don't
want the hassle, the cost, or the tech."

[0:25-0:40] Screen: fast-loading site, mobile view
"So here's what I do. I build you a custom website in 48 hours.
Free for 30 days. $97/mo to keep it live. No contracts."

[0:40-0:55] CTA
"I take on 10 local businesses a month. DM me 'SITE'."

[End card] Free website · 48 hours · 30-day trial · $97/mo
```

---

## 6. Facebook / Community Group Post

```
Building 10 free websites this month for local service businesses.

48-hour build. Free for 30 days. $97/month after if you want to
keep it live — hosting, updates, and support included. No contracts.

Salons, contractors, dentists, plumbers, real estate, med spas,
restaurants, electricians, landscapers, and more.

Comment SITE or DM me to apply.
```

---

## 7. Priority Outreach Order

Use Outscraper to pull prospects. First batch: one vertical, one city,
20 businesses with no website or outdated site (no mobile, copyright 3+ years old).

| # | Business | Contact | Trade | Current |
|---|---|---|---|---|
| 1 | Santos Salon & Spa | Maria Santos | Hair Salon | No site |
| 2 | Chen Plumbing Co. | James Chen | Plumber | Facebook only |
| 3 | Kim Electric Inc. | David Kim | Electrician | Google Maps only |
| 4 | Mendez Construction | Carlos Mendez | Contractor | No site |
| 5 | Green Med Spa | Dr. Rachel Green | Med Spa | Instagram only |
| 6 | OBrien Landscaping | Ryan OBrien | Landscaper | No site |
| 7 | Sharma Chiropractic | Dr. Priya Sharma | Chiropractor | No site |
| 8 | DiMaggio Pizza | Frank DiMaggio | Restaurant | No site |
| 9 | Hassan Dry Cleaning | Omar Hassan | Dry Cleaning | No site, 3 loc |
| 10 | Rodriguez Law Firm | Mike Rodriguez | Law Firm | Referral only |

---

## 8. Logging Convention

When approved and sent:
- outreach_count += 1
- last_contact_date = datetime('now')
- status = 'contacted'
- Log in outreach_log.md

Follow-ups:
- Day 3: outreach_count += 1, update last_contact_date
- Day 7: outreach_count += 1, update last_contact_date
- After Day 7: status = 'closed_no_response'

---

## 9. Pricing Summary (for reference)

| Tier | Price | Includes |
|---|---|---|
| **Free Trial** | $0/30 days | Custom website + basic AI follow-up |
| **Starter** | $97/mo | Website stays live + Lead Nurturer + Reviews |
| **Pro** | $497/mo | Above + AI Voice Receptionist |
| **Complete** | $2,497/mo | All 5 AI workers |
