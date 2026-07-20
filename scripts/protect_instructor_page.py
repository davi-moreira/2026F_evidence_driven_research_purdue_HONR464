#!/usr/bin/env python3
"""protect_instructor_page.py — encrypt docs/instructor.html behind a password.

Runs as the Quarto post-render step (_quarto.yml project.post-render), so the
published GitHub Pages site never contains the instructor page in cleartext.
The whole rendered page is AES-GCM encrypted with a key derived from the
password (PBKDF2-HMAC-SHA256); a small self-contained gate page decrypts it
in the browser via WebCrypto. Idempotent: an already-encrypted page is left
alone.

This is a courtesy lock so casual visitors cannot read the page. The real
protection for instructor material is the PRIVATE GitHub repo the page links
to (Colab/GitHub require the instructor's login).

Password: env HONR_INSTRUCTOR_PASSWORD, default "eureka".

Usage: python3 scripts/protect_instructor_page.py [path-to-html]
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
TARGET = REPO / "docs" / "instructor.html"
MARKER = "<!-- honr-encrypted -->"
ITERATIONS = 600_000

GATE = """<!DOCTYPE html>
<html lang="en">
{marker}
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Instructor — HONR 46400</title>
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
  <h1>Instructor material</h1>
  <p>HONR 46400 — Evidence-Driven Research. Enter the instructor password.</p>
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


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else TARGET
    if not target.exists():
        print(f"protect_instructor_page: {target} not found (nothing to do)")
        return
    html = target.read_text()
    if MARKER in html:
        print(f"✓ {target.relative_to(REPO)} already encrypted (skipped)")
        return

    password = os.environ.get("HONR_INSTRUCTOR_PASSWORD", "eureka").encode()
    salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                     iterations=ITERATIONS)
    key = kdf.derive(password)
    iv = secrets.token_bytes(12)
    cipher = AESGCM(key).encrypt(iv, html.encode(), None)

    page = GATE.format(
        marker=MARKER,
        salt=base64.b64encode(salt).decode(),
        iv=base64.b64encode(iv).decode(),
        data=base64.b64encode(cipher).decode(),
        iterations=ITERATIONS,
    )
    target.write_text(page)
    print(f"✓ encrypted {target.relative_to(REPO)} "
          f"({len(cipher) // 1024} KB ciphertext)")


if __name__ == "__main__":
    main()
