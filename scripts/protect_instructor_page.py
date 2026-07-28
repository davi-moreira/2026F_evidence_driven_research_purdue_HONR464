#!/usr/bin/env python3
"""protect_instructor_page.py — encrypt instructor-facing pages behind a password.

Runs as the Quarto post-render step of EVERY project in this repo (the site
and the three book editions), so the published GitHub Pages site never
contains an instructor page in cleartext. Protected pages (D26): the site's
docs/instructor.html and the book's For-Instructors appendix in all three
editions (docs/book*/for-instructors.html — companion-course material and the
"It is your turn" grading rubrics). Each page is AES-GCM encrypted with a key
derived from the password (PBKDF2-HMAC-SHA256); a small self-contained gate
page decrypts it in the browser via WebCrypto and tells visitors to request
the password by email. Idempotent: an already-encrypted page is left alone,
so the four projects can each run this without stepping on one another.

This is a courtesy lock so casual visitors cannot read the pages. The real
protection for instructor material is the PRIVATE GitHub repo the pages link
to (Colab/GitHub require the instructor's login).

Password (never committed): env HONR_INSTRUCTOR_PASSWORD, else the gitignored
file _production_kit/page_password.txt. The script fails hard if neither is
set — there is no default.

Usage: python3 scripts/protect_instructor_page.py [path-to-html ...]
       (no arguments: protect every registered page that exists)
"""
from __future__ import annotations

import base64
import os
import secrets
import sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

REPO = Path(__file__).resolve().parent.parent
MARKER = "<!-- honr-encrypted -->"
ITERATIONS = 600_000
PASSWORD_FILE = REPO / "_production_kit" / "page_password.txt"

EMAIL = ('<a href="mailto:dcordeir@purdue.edu">dcordeir@purdue.edu</a>')

# path (relative to repo) -> gate title, heading, message shown on the lock page
PAGES = {
    "docs/instructor.html": (
        "Instructor — HONR 46400", "Instructor material",
        "HONR 46400 — Evidence-Driven Research. Enter the instructor "
        f"password, or request it by email: {EMAIL}."),
    "docs/book/for-instructors.html": (
        "For Instructors — EDR|AI", "For Instructors",
        "This area holds the companion-course material and the grading "
        "rubrics for the “It is your turn” sections. Request the "
        f"password by email from the author: {EMAIL}."),
    "docs/book-pt/for-instructors.html": (
        "Para Instrutores — EDR|AI", "Para Instrutores",
        "Esta área reúne o material do curso companheiro e as rubricas de "
        "avaliação das seções “Agora é a sua vez”. Solicite a "
        f"senha por e-mail ao autor: {EMAIL}."),
    "docs/book-es/for-instructors.html": (
        "Para Docentes — EDR|AI", "Para Docentes",
        "Esta área reúne el material del curso de acompañamiento y las "
        "rúbricas de calificación de las secciones “Ahora te toca a "
        f"ti”. Solicita la contraseña por correo al autor: {EMAIL}."),
}

GATE = """<!DOCTYPE html>
<html lang="en">
{marker}
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
         Helvetica, Arial, sans-serif; background: #f5f6f8; margin: 0;
         display: flex; min-height: 100vh; align-items: center;
         justify-content: center; }}
  .card {{ background: #fff; border: 1px solid #e1e4e8; border-radius: 10px;
          padding: 2.2rem 2.6rem; max-width: 24rem; width: 90%;
          box-shadow: 0 4px 14px rgba(0,0,0,.06); text-align: center; }}
  h1 {{ font-size: 1.15rem; margin: 0 0 .4rem; }}
  p  {{ font-size: .9rem; color: #57606a; margin: 0 0 1.2rem; }}
  input {{ width: 100%; box-sizing: border-box; padding: .55rem .7rem;
          font-size: 1rem; border: 1px solid #d0d7de; border-radius: 6px; }}
  button {{ margin-top: .8rem; width: 100%; padding: .55rem; font-size: 1rem;
           border: 0; border-radius: 6px; background: #1a4b8b; color: #fff;
           cursor: pointer; }}
  button:hover {{ background: #143a6d; }}
  .err {{ color: #b42318; font-size: .85rem; min-height: 1.2em;
         margin-top: .7rem; }}
</style>
</head>
<body>
<div class="card">
  <h1>{heading}</h1>
  <p>{message}</p>
  <form id="f">
    <input id="pw" type="password" autocomplete="current-password"
           placeholder="Password" autofocus>
    <button type="submit">Unlock</button>
    <div class="err" id="err"></div>
  </form>
</div>
<script>
const SALT = "{salt}", IV = "{iv}", DATA = "{data}", ITER = {iterations};
const b64 = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
document.getElementById("f").addEventListener("submit", async ev => {{
  ev.preventDefault();
  const err = document.getElementById("err");
  err.textContent = "";
  try {{
    const pw = new TextEncoder().encode(document.getElementById("pw").value);
    const km = await crypto.subtle.importKey("raw", pw, "PBKDF2", false, ["deriveKey"]);
    const key = await crypto.subtle.deriveKey(
      {{ name: "PBKDF2", salt: b64(SALT), iterations: ITER, hash: "SHA-256" }},
      km, {{ name: "AES-GCM", length: 256 }}, false, ["decrypt"]);
    const plain = await crypto.subtle.decrypt(
      {{ name: "AES-GCM", iv: b64(IV) }}, key, b64(DATA));
    const html = new TextDecoder().decode(plain);
    document.open(); document.write(html); document.close();
  }} catch (e) {{
    err.textContent = "Wrong password.";
  }}
}});
</script>
</body>
</html>
"""


def get_password() -> bytes:
    env = os.environ.get("HONR_INSTRUCTOR_PASSWORD")
    if env:
        return env.encode()
    if PASSWORD_FILE.exists():
        return PASSWORD_FILE.read_text().strip().encode()
    sys.exit("✗ protect_instructor_page: no password — set "
             "HONR_INSTRUCTOR_PASSWORD or create "
             "_production_kit/page_password.txt (gitignored). "
             "The password is never committed and never defaulted.")


def protect(target: Path, password: bytes) -> None:
    rel = target.resolve().relative_to(REPO).as_posix()
    title, heading, message = PAGES.get(
        rel, ("Protected page", "Protected page",
              f"Request the password by email: {EMAIL}."))
    html = target.read_text()
    if MARKER in html:
        print(f"✓ {rel} already encrypted (skipped)")
        return

    salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                     iterations=ITERATIONS)
    key = kdf.derive(password)
    iv = secrets.token_bytes(12)
    cipher = AESGCM(key).encrypt(iv, html.encode(), None)

    page = GATE.format(
        marker=MARKER, title=title, heading=heading, message=message,
        salt=base64.b64encode(salt).decode(),
        iv=base64.b64encode(iv).decode(),
        data=base64.b64encode(cipher).decode(),
        iterations=ITERATIONS,
    )
    target.write_text(page)
    print(f"✓ encrypted {rel} ({len(cipher) // 1024} KB ciphertext)")


def main() -> None:
    password = get_password()
    if len(sys.argv) > 1:
        targets = [Path(a) for a in sys.argv[1:]]
    else:
        targets = [REPO / rel for rel in PAGES]
    for target in targets:
        if target.exists():
            protect(target, password)
        else:
            print(f"protect_instructor_page: {target} not found (nothing to do)")


if __name__ == "__main__":
    main()
