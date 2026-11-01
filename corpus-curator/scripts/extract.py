#!/usr/bin/env python3
"""Deterministically extract text from source documents for corpus-curator.

Usage:
    python3 extract.py INPUT WORKDIR

INPUT is one file or a folder (top level only). For each supported file a
subfolder of WORKDIR receives:

    extract.txt    plain text taken from the file itself (PDF pages separated by \\f)
    structure.md   GFM conversion keeping headings, emphasis and notes (pandoc formats, MD)
    pages/         PNG images of image-only PDF pages, or the page image itself
    info.json      format, tool used, page counts, text/image page numbers, classification hint

WORKDIR/manifest.json lists every input with its status. Standard library plus
external tools: pdftotext/pdfinfo/pdftoppm (poppler), pandoc, and on macOS
textutil and sips for .doc and TIFF/HEIC.

Exit status: 0 on success, 3 when a required tool is missing (nothing is
extracted for that run), 2 on usage error.
"""

import json
import os
import re
import shutil
import subprocess
import sys

PANDOC_FORMATS = {".docx": "docx", ".odt": "odt", ".rtf": "rtf", ".epub": "epub",
                  ".html": "html", ".htm": "html"}
IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic"}
TEXT_FORMATS = {".txt", ".md"}
SUPPORTED = set(PANDOC_FORMATS) | IMAGE_FORMATS | TEXT_FORMATS | {".pdf", ".doc"}
MIN_PAGE_CHARS = 25

INSTALL = {
    "pdftotext": "poppler (macOS: brew install poppler; Debian/Ubuntu: apt install poppler-utils)",
    "pdfinfo": "poppler (macOS: brew install poppler; Debian/Ubuntu: apt install poppler-utils)",
    "pdftoppm": "poppler (macOS: brew install poppler; Debian/Ubuntu: apt install poppler-utils)",
    "pandoc": "pandoc (macOS: brew install pandoc; Debian/Ubuntu: apt install pandoc)",
    "textutil": "textutil (macOS built-in) or LibreOffice for .doc files",
    "sips": "sips (macOS built-in) or ImageMagick (magick) for TIFF/HEIC images",
}


class MissingTool(Exception):
    pass


def tools_for(ext):
    if ext == ".pdf":
        return ["pdftotext", "pdfinfo", "pdftoppm"]
    if ext in PANDOC_FORMATS:
        return ["pandoc"]
    if ext == ".doc":
        return ["textutil", "pandoc"]
    if ext in (".tif", ".tiff", ".heic"):
        return ["sips"]
    return []


def require(tool):
    if tool == "sips" and not shutil.which("sips") and shutil.which("magick"):
        return "magick"
    if not shutil.which(tool):
        raise MissingTool(tool)
    return tool


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True).stdout


def write(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(data)


def decode_text(raw):
    for enc in ("utf-8-sig", "utf-8"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            pass
    return raw.decode("cp1252", errors="replace"), "cp1252 (guessed; verify characters)"


def extract_pdf(src, out, info):
    pages_dir = os.path.join(out, "pages")
    meta = run(["pdfinfo", src]).decode("utf-8", "replace")
    m = re.search(r"^Pages:\s+(\d+)", meta, re.M)
    count = int(m.group(1)) if m else 0
    text = run(["pdftotext", "-enc", "UTF-8", src, "-"]).decode("utf-8", "replace")
    pages = text.split("\f")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]
    text_pages, image_pages = [], []
    for i, page in enumerate(pages, start=1):
        (text_pages if len(page.strip()) >= MIN_PAGE_CHARS else image_pages).append(i)
    for i in range(len(pages) + 1, count + 1):
        image_pages.append(i)
    if image_pages:
        os.makedirs(pages_dir, exist_ok=True)
        for i in image_pages:
            run(["pdftoppm", "-f", str(i), "-l", str(i), "-r", "200", "-png",
                 src, os.path.join(pages_dir, f"p{i:04d}")])
    write(os.path.join(out, "extract.txt"), "\f".join(pages))
    info.update(tool="pdftotext", pages=count, text_pages=text_pages, image_pages=image_pages)
    if not image_pages:
        info["hint"] = "text-layer"
    elif not text_pages:
        info["hint"] = "scan"
    else:
        info["hint"] = "mixed"


def extract_pandoc(src, fmt, out, info):
    plain = run(["pandoc", "-f", fmt, "-t", "plain", "--wrap=none", src]).decode("utf-8")
    gfm = run(["pandoc", "-f", fmt, "-t", "gfm", "--wrap=none", src]).decode("utf-8")
    write(os.path.join(out, "extract.txt"), plain)
    write(os.path.join(out, "structure.md"), gfm)
    info.update(tool="pandoc", hint="text-layer")


def extract_doc(src, out, info):
    tmp = os.path.join(out, "converted.docx")
    run(["textutil", "-convert", "docx", "-output", tmp, src])
    extract_pandoc(tmp, "docx", out, info)
    os.remove(tmp)
    info["tool"] = "textutil + pandoc"


def extract_image(src, ext, out, info):
    pages_dir = os.path.join(out, "pages")
    os.makedirs(pages_dir, exist_ok=True)
    target = os.path.join(pages_dir, "p0001.png" if ext in (".tif", ".tiff", ".heic") else "p0001" + ext)
    if ext in (".tif", ".tiff", ".heic"):
        tool = require("sips")
        if tool == "sips":
            run(["sips", "-s", "format", "png", src, "--out", target])
        else:
            run(["magick", src, target])
    else:
        shutil.copyfile(src, target)
    write(os.path.join(out, "extract.txt"), "")
    info.update(tool="image", pages=1, text_pages=[], image_pages=[1], hint="scan")


def extract_text(src, ext, out, info):
    with open(src, "rb") as fh:
        text, enc = decode_text(fh.read())
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    write(os.path.join(out, "extract.txt"), text)
    if ext == ".md":
        write(os.path.join(out, "structure.md"), text)
    info.update(tool="read", encoding=enc, hint="text-layer")


def slot_name(path, used):
    base = re.sub(r"[^\w.-]+", "_", os.path.basename(path)) or "input"
    name, n = base, 2
    while name in used:
        name, n = f"{base}_{n}", n + 1
    used.add(name)
    return name


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    src, workdir = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    if os.path.isdir(src):
        inputs = [os.path.join(src, f) for f in sorted(os.listdir(src)) if not f.startswith(".")]
    elif os.path.isfile(src):
        inputs = [src]
    else:
        print(f"input not found: {src}", file=sys.stderr)
        return 2

    supported = [p for p in inputs if os.path.isfile(p) and os.path.splitext(p)[1].lower() in SUPPORTED]
    missing = sorted({t for p in supported for t in tools_for(os.path.splitext(p)[1].lower())
                      if not shutil.which(t) and not (t == "sips" and shutil.which("magick"))})
    if missing:
        print("Missing required tools; nothing was extracted:", file=sys.stderr)
        for t in missing:
            print(f"  {t}: install {INSTALL[t]}", file=sys.stderr)
        return 3

    os.makedirs(workdir, exist_ok=True)
    manifest, used = [], set()
    for path in inputs:
        ext = os.path.splitext(path)[1].lower()
        entry = {"input": path}
        if os.path.isdir(path):
            entry.update(status="skipped", reason="subfolder (only top-level files are read)")
        elif ext not in SUPPORTED:
            entry.update(status="skipped", reason=f"unsupported format '{ext or 'none'}'")
        else:
            out = os.path.join(workdir, slot_name(path, used))
            os.makedirs(out, exist_ok=True)
            info = {"input": path, "format": ext.lstrip(".")}
            try:
                if ext == ".pdf":
                    extract_pdf(path, out, info)
                elif ext in PANDOC_FORMATS:
                    extract_pandoc(path, PANDOC_FORMATS[ext], out, info)
                elif ext == ".doc":
                    extract_doc(path, out, info)
                elif ext in IMAGE_FORMATS:
                    extract_image(path, ext, out, info)
                else:
                    extract_text(path, ext, out, info)
                entry.update(status="extracted", workdir=out, hint=info.get("hint"))
            except subprocess.CalledProcessError as exc:
                msg = exc.stderr.decode("utf-8", "replace").strip() if exc.stderr else str(exc)
                entry.update(status="failed", reason=msg)
                info["error"] = msg
            with open(os.path.join(out, "info.json"), "w", encoding="utf-8") as fh:
                json.dump(info, fh, ensure_ascii=False, indent=2)
        manifest.append(entry)
        print(f"{entry['status']:9} {os.path.basename(path)}"
              + (f"  [{entry.get('hint')}]" if entry.get("hint") else "")
              + (f"  ({entry['reason']})" if entry.get("reason") else ""))

    with open(os.path.join(workdir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
