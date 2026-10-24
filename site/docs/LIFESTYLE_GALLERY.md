# Lifestyle gallery v3

Seven concept scenes replace the unrelated generic tablet and foldable-device images.

Source of truth: `assets/story/lifestyle-scenes.json`. Run `python3 scripts/build-lifestyle.py`, then `python3 scripts/sync-site.py` after changing copy. Image assets must also be mirrored to `site/assets/`.

Images are generated with the built-in ImageGen tool, using each linked product CAD render and official device appearance references. These are illustrative scenes, not fit-test evidence or manufacturing drawings. The actual CAD remains available on every card.

## Device references

- BOOX Go 6 (Gen II): https://shop.boox.com/products/go6gen2 — ribbed Custard rear, no rear camera.
- iPhone 17: https://www.apple.com/uk/iphone-17/ — standard two-camera device.
- iPhone Duo: https://www.apple.com/iphone-duo/ — exterior camera half and outer-display half.

## Prompt specification

Create photorealistic warm natural-light lifestyle product scenes. Preserve the referenced CAD holder's ring, sheath or clip silhouette and placement; use the official device rear appearance. Show the entire pen and holder. AERIS: smooth central long sheath on BOOX in transit. VERTEX: faceted central long sheath on BOOX in a cafe. ZEPHYR: short central split clamp on BOOX at a reading desk. AURA: ring with side bridge and sheath on BOOX. ECLIPSE MINI: short ring clamp on a standard iPhone, shown as storage only. AXIS: standalone pencil clip beside the iPhone, not a phone mount. AURA DUO: extended side arm and sheath, pencil parallel to the phone with visible edge clearance, unfolded device with two horizontal cameras on one half and an outer display on the other. Never substitute a generic iPad or add unsupported Pencil writing on iPhone.

Final precise-object edits for ECLIPSE MINI and AXIS: preserve the whole scene and holder geometry; replace the flat lower end of the white pencil with a conical Apple Pencil nib, leaving the upper cap unchanged.

Final image paths: `assets/photos/gallery-v3/{aeris,vertex,zephyr,eclipse,aura,axis,duo}.png`.

## Fit correction v4

AERIS and AURA DUO now use `assets/photos/gallery-v4/aeris.png` and `duo.png`. AURA DUO references the closer v3 STL. AERIS shows the calculated protruding pen. See [AURA_DUO_V3.md](AURA_DUO_V3.md) for the exact dimensions, assumptions and edit prompts. The final AERIS refinement extends the sheath to within3 mm of the case bottom and sizes the ring to68 mm while preserving the21.54 mm cap overhang. Built-in ImageGen was used for both edits.

## Centering correction v5

AERIS, VERTEX and ZEPHYR final images use `assets/photos/gallery-v5/`. Their circular bases and axial pen holders align with the device's transverse center, matching CAD X=0. ImageGen precise-object-edit prompts preserve all geometry, axial position, overhang, case, background and lighting; move the complete ring/sheath/clamp/pen assembly left as one unit to the perspective longitudinal midline. AERIS correction is approximately47px left at ring height; VERTEX40px; ZEPHYR30px. The CAD/STLs already have X=0 registration and do not need a geometry shift.
