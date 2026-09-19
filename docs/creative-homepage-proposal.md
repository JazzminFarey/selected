# Creative portfolio correction — 19 September 2026

Starting commit: ec67e3728c4d29719a69c6bef2c1c5452e5b1262. Existing PR #2 only; draft and unmerged.

The first repository portfolio (8ca42b8) supplies the visual benchmark: confident sans-serif typography, asymmetric image grid, short captions and a black typographic growth tile. The corrected homepage retains this language, gives the reel the full content width and moves the short introduction below it. Money Your Way uses the original Image Project Cover; Flex uses the complete Lose interest in paying interest campaign. Feed now shows three creator executions. The four earlier-work cards show ten source executions instead of four.

The Drive root, Images and all four image subfolders, and Zip Material were inventoried through the connector. All 38 source images and both motion files were inspected using the previously downloaded originals after fresh streamed downloads returned HTTP 403. Cached file IDs and sizes match the inventory. The two portfolio decks and HTML source were read for context. Money Your Way Logo.jpg and the Creative Moodboard are restored within the case page; neither is used as invented campaign artwork. No changes were made for rights reasons.

The 30-second reel is 900 frames at 30fps, with 30 cuts, no voiceover and no explanatory overlays. Zip receives 13.7 seconds and the earlier work 16.3 seconds. Full timeline: reel-timeline.json. The existing source set substantiates Barnardos Buddies; no separate Barnardos body of work was established, so none was invented. Only the seven established approved bodies of work appear.

Rebuild from this checkout with `python scripts/reel/build.py` then `python scripts/reel/sound.py`. Intermediates live in .recovery-qa, excluded from Git. The original synthesized audio bed is retained; the player starts muted with native playback controls.

Local verification: all 117 relative file references resolve; all local raster assets decode; the reel has 900 H.264 video frames, AAC audio and a 30.000-second duration. Hosted visual and playback verification is performed against the pushed commit before delivery.
