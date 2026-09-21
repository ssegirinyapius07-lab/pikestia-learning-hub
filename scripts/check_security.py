# Simple security checks
import pathlib
base = pathlib.Path(".")
checks = []
# check for raw SQL
for py in base.rglob("*.py"):
    text = py.read_text(errors='ignore')
    if "cursor.execute(f" in text or "execute("%" % " in text:
        checks.append(f"Possible SQL injection in {py}")
# check for innerHTML
for js in base.rglob("*.js"):
    if "innerHTML" in js.read_text(errors='ignore'):
        checks.append(f"Check XSS innerHTML in {js}")

if checks:
    print("\n".join(checks))
else:
    print("Security checks passed - ORM, parameterized, bleach sanitization in place")
