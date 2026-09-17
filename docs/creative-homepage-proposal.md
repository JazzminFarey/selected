# Creative-led homepage — first review

Draft proposal only. No deployment or merge authorised in this pass.

## Page sequence

| Position | Treatment | Content |
| --- | --- | --- |
| 1. Hero | Large left-aligned name, compact introduction | Jazz Farey / Selected Brand + Creative Work / I connect brand, creative and growth. |
| 2. Reel | Wide 16:9 black stage immediately below the hero | Portfolio-original HTML/CSS title card: Ideas. In motion. One entrance animation, reduced-motion support. Clearly labelled as a preview; no fake play button. |
| 3. Selected Work | Existing asymmetric four-case grid; fewer supporting words | Money Your Way, That’s A Flex, Built for Feed, Finding Winners Faster, in that order. |
| 4. Earlier work | Compact four-column strip; two columns on mobile | allHearts, Barnardos Buddies, Give with Heart Day, Walk Your Way. Names and disciplines only; not clickable, no campaign media. |
| 5. How I think | Dark full-width section; three short statements | Ideas / Systems / Economics. |
| 6. Better. | Small secondary section | What I’m building now; link to existing Better. page. |
| 7. Contact | Email and LinkedIn | Existing leadership/ownership disclaimer retained. Cutting Room available as a secondary link. |

## Navigation

Work · How I think · Better. · Contact. All link to homepage sections consistently across the eight pages. Beliefs remains accessible at its existing URL to preserve its material and inbound links, but is no longer in primary navigation. Cutting Room remains available through the homepage secondary link.

## How I think

- **Ideas.** Give people a reason to care and a point of view to remember.
- **Systems.** Build ideas that travel, with room for teams to make great work.
- **Economics.** Connect creative decisions to customer behaviour and commercial value.

## Reel handoff

The motion slot supports a later video or Vimeo iframe through scoped responsive styles. The current title card is portfolio-original and is not a showreel or a reconstruction of any campaign. A 20–30 second finished edit needs approved source material before insertion. Keep controls, an accessible player title, a stable aspect ratio and attribution beside the finished reel. No third-party player requests are introduced by this proposal.

## Earlier work handoff

The four named slots sit immediately after the Zip cases, before How I think. Once media rights are confirmed, replace these name-only slots with visual case entries. Preserve collaborator credits, including Megan Pope (allHearts) and Alana Indratheb (Barnardos Buddies), subject to checking the final source assets. No older assets or metrics have been imported.

## Checks and limits

- Local HTML and CSS references plus internal fragment destinations checked across all eight pages.
- JavaScript syntax passes; no media references in JavaScript.
- All eight pages retain neutral social-preview metadata.
- Only `Assets/social-preview.png` remains in the media directory; no new media files.
- Existing case external links/embeds, leadership copy, and every footer are unchanged.
- Non-homepage changes are limited to primary navigation.
- Whitespace check passes with existing CRLF line endings recognised.
- Rendered desktop/mobile QA is blocked: the browser rejects the local preview with `ERR_BLOCKED_BY_CLIENT`. Responsive CSS is present, but visual fit and interaction need browser review before merge.
