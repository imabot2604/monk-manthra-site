#!/usr/bin/env python3
"""
Instagram carousel publisher — shared by every carousel folder in this
directory (golden-milk-photo-carousel, golden-milk, monk-manthra-intro,
monk-manthra-photo-carousel, ...).

Wraps the same three-step Graph API flow used to publish the Golden Milk
photo carousel by hand:
  1. one media container per image (is_carousel_item=true)
  2. one parent container (media_type=CAROUSEL, children=[...])
  3. publish the parent container

Uses the `composio` CLI under the hood — the same one already connected
to @monkmanthra in this environment. Images must be JPEGs (Instagram's
Graph API requires it); PNGs are not converted here, run them through
`sips -s format jpeg in.png --out out.jpg` first (every carousel's
build script's png/ output needs this once before publishing — see
each folder's jpg/ for the converted copies).

Usage:
    python3 publish_carousel.py <folder-of-jpgs> --caption-file caption.txt [--dry-run]
    python3 publish_carousel.py <folder-of-jpgs> --caption "Text here"

    <folder-of-jpgs>   directory containing 2-10 .jpg files, published in
                       alphabetical order — name them slide-1-*.jpg,
                       slide-2-*.jpg, etc. to control ordering.
    --dry-run          create the item containers + parent container but
                       do NOT call publish — leaves an inspectable draft
                       container that expires in ~24h unused, same as a
                       manual dry run.

Prints the container ids at each step and, once published, the live
permalink.
"""
import argparse
import glob
import json
import os
import subprocess
import sys


def run_composio(slug, data):
    payload = json.dumps(data)
    r = subprocess.run(
        ["composio", "execute", slug, "-d", payload],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"FAILED {slug}: {r.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        parsed = json.loads(r.stdout)
    except json.JSONDecodeError:
        print(f"Could not parse composio output for {slug}:\n{r.stdout}", file=sys.stderr)
        sys.exit(1)
    if not parsed.get("successful"):
        print(f"FAILED {slug}: {parsed}", file=sys.stderr)
        sys.exit(1)
    return parsed["data"]


def upload_item(jpg_path, alt_text=None):
    data = {
        "ig_user_id": "me",
        "is_carousel_item": True,
        "image_file": jpg_path,
    }
    if alt_text:
        data["alt_text"] = alt_text
    result = run_composio("INSTAGRAM_POST_IG_USER_MEDIA", data)
    return result["id"]


def create_parent(children_ids, caption):
    data = {
        "ig_user_id": "me",
        "media_type": "CAROUSEL",
        "children": children_ids,
        "caption": caption,
    }
    result = run_composio("INSTAGRAM_POST_IG_USER_MEDIA", data)
    return result["id"]


def publish(creation_id):
    result = run_composio("INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH", {
        "ig_user_id": "me",
        "creation_id": creation_id,
    })
    return result["id"]


def get_permalink(media_id):
    result = run_composio("INSTAGRAM_GET_IG_MEDIA", {
        "ig_media_id": media_id,
        "fields": "permalink",
    })
    return result.get("permalink")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", help="Directory of .jpg slides, published in alphabetical order")
    parser.add_argument("--caption", help="Caption text (inline)")
    parser.add_argument("--caption-file", help="Path to a text file containing the caption")
    parser.add_argument("--dry-run", action="store_true", help="Build containers but do not publish")
    args = parser.parse_args()

    if not args.caption and not args.caption_file:
        parser.error("pass --caption or --caption-file")
    caption = args.caption or open(args.caption_file).read().strip()

    jpgs = sorted(glob.glob(os.path.join(args.folder, "*.jpg")))
    if not (2 <= len(jpgs) <= 10):
        parser.error(f"found {len(jpgs)} jpgs in {args.folder} — Instagram carousels need 2-10")

    print(f"Publishing {len(jpgs)} slides from {args.folder}:")
    for j in jpgs:
        print(f"  {os.path.basename(j)}")

    children = []
    for jpg in jpgs:
        cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(jpg)) or ".")
        try:
            item_id = upload_item(os.path.basename(jpg))
        finally:
            os.chdir(cwd)
        print(f"  container {os.path.basename(jpg)} -> {item_id}")
        children.append(item_id)

    parent_id = create_parent(children, caption)
    print(f"parent carousel container -> {parent_id}")

    if args.dry_run:
        print("--dry-run: not publishing. Container will expire in ~24h unused.")
        return

    media_id = publish(parent_id)
    print(f"published -> media id {media_id}")
    permalink = get_permalink(media_id)
    if permalink:
        print(f"live: {permalink}")


if __name__ == "__main__":
    main()
