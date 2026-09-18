# Selected-work reel — correction edit

30.000 seconds · 1280 × 720 · 30 fps · H.264/AAC. No title cards, no voiceover. Starts and ends on actual Money Your Way artwork. The final seven seconds return only to the named projects.

## Sources and collaborators

| Project | Assets used | Credits |
|---|---|---|
| Money Your Way | Original repo `Assets/Money Your Way/Hero.png`, `1000131099 (1).png`, `1000131103.png` | Zip Co. and campaign teams |
| That’s A Flex | Original repo `Ad 1.jpg`, `Ad 2.jpg`; full Robert campaign motion | Zip Co.; VML Australia; motion design and animation: Robert Pregardt-Paur |
| Built for Feed | Original repo `Assets/Feed/1.jpg`, `2.jpg`, `4.jpg` | Zip Co. and the featured creators |
| allHearts | Original Squarespace shirt, mugs and tote photography | Heart Foundation; creative: Megan Pope |
| Barnardos Buddies | Original Squarespace posters, social and children’s T-shirt photography | Barnardos Australia; creative: Alana Indratheb |
| Jump Rope for Heart | Original Squarespace book cover, spread and animated GIF | Heart Foundation; Jazz supported creative direction and production |
| Walk Your Way | Original Squarespace phone campaign compositions | Heart Foundation campaign team |

The source portfolio lists Barnardos Buddies only. No separate Barnardos body of work was found; none has been invented.

Earlier imagery is stored in `Assets/earlier/`. Original Zip media is restored from commit `acbbcf2`. Robert’s full original motion is `Assets/work/flex-campaign.mp4`; the homepage cover uses the complete original Ad 1. The case-page motion poster is the deliberate 6-second brand/product reveal.

Each foreground asset in the reel retains its whole source frame. Artwork is arranged in explicit two-up, three-up and large/small compositions. Defocused colours from the same work or matching campaign fields fill space around complete artwork; no black letterboxing. Genuine motion appears only in Robert’s Flex piece and the original Jump Rope GIF. No campaign artwork is generated or redrawn.

The original synthesized instrumental bed is retained. Frame-accurate cuts and project timings are in `reel-timeline.json`. Rebuild with `python scripts/reel/build.py` then `python scripts/reel/sound.py` (Pillow and FFmpeg required).
