# Screen products — flat-base-down print orientation

AURA SCREEN v4, NEXUS SCREEN v2 and AURA DUO SCREEN v3 are supplied as
*_BED_DOWN.stl. Each is rigidly rotated 180 degrees about X and moved to Z=0.
No scaling, mirroring, wall, bore, tip-seat or dimensional changes were made.

The broad flat backing lies on the build plate; the holder opening faces up.
The long pen axis lies horizontally. These are the files selected by the
product page. The original assembly-coordinate files remain available in
older packs and source assets.

Use 100% scale and preserve the supplied rotation. Move/center the part on the
plate as needed. Review the layer preview and support settings separately;
this pack does not specify a printer profile or guarantee support-free printing.

checks.json and the per-model orientation JSON files record the source/output
hashes, rigid transform, Z bounds, unchanged volume/dimensions and bed contact.
Rebuild: .venv/bin/python scripts/build-print-orientation.py
