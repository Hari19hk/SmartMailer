from smartmailer import SmartMailer, TemplateModel, TemplateEngine

print("[DEBUG] Imports successful")

# ---------------- Schema ----------------
class MySchema(TemplateModel):
    name: str
    committee: str
    allotment: str
    email: str

print("[DEBUG] Schema defined")

# ---------------- Templates (Jinja2 Features) ----------------
subject = "Test Mail for {{ name }}"

body = """
Dear {{ name }},

You are assigned to {{ committee }} with allotment {{ allotment }}.

{% if committee == "UNDP" %}
This is a special committee assignment.
{% else %}
This is a regular committee assignment.
{% endif %}

Regards,
SmartMailer Team
"""

print("[DEBUG] Templates created with Jinja2 syntax")

template = TemplateEngine(subject=subject, body_text=body)
print("[DEBUG] TemplateEngine initialized")

# ---------------- Recipients ----------------
recipients = [
    MySchema(
        name="Test User",
        committee="UNDP",
        allotment="India",
        email="hk0987123456@gmail.com"
    )
]

print("[DEBUG] Recipients created:", recipients)

# ---------------- Mailer Setup ----------------
mailer = SmartMailer(
    sender_email="hk19hari@gmail.com",
    password="ceom dair ffet saio",   # App password
    provider="gmail",
    session_name="test-session"
)

print("[DEBUG] SmartMailer initialized")

# ---------------- Send Mail ----------------
print("[DEBUG] Attempting to send email...")

try:
    mailer.send_emails(
        recipients=recipients,
        email_field="email",
        template=template
    )
    print("[DEBUG] Email sent successfully!")
except Exception as e:
    print("[ERROR] Failed to send email")
    print("[ERROR]", type(e).__name__, ":", e)
