# Webapp design

The webapp is the face of the demo. It must feel like a finished product built for the people in the story, not like a notebook or a generic dashboard.

## Two rules that pull in different directions

1. **Visual identity is fixed.** Reuse the look described below.
2. **Structure is free.** Never copy a screen layout from a previous demo. Decide the layout from the use case: who is using it, what decision they make, and what they need to see to make it. The reference design happened to be a ranked list with filters and a detail panel; another use case might call for a map of the plant, a timeline of interventions, a work-order board, a conversation with the agent next to evidence cards, or a single guided workflow. Choose what gives that persona the best experience.

Start by writing three lines before any code: the persona, the decision they take, and the one thing the first screen must make obvious.

## Visual identity (the "editorial decision tool" look)

- **Tone**: calm, confident, editorial. It looks like a briefing from a good analyst, not a BI tool full of widgets.
- **Typography**: a high-contrast serif for large headlines and key numbers (Georgia-like or a refined serif from a web font), a clean neutral sans-serif for body and controls, and small uppercase labels with generous letter-spacing for section kickers and field labels. Big headline in two short sentences that state the value ("Prioritise renewals. Protect fleet value."), translated to the use case.
- **Layout feel**: wide margins, lots of white space, thin 1px borders instead of shadows, square or barely rounded corners, a thick dark rule at the top of the main working panel.
- **Background**: an off-white with a slight warm tint rather than pure white, with white cards on top.
- **Colour**: one deep accent colour (default deep teal-green) for primary actions, bars and kickers; one warm secondary (amber/orange) for "attention" and one muted red tint for risk badges; near-black for text and the top rule; light grey for tracks and dividers. Never more than the accent plus two supporting hues.
- **Numbers**: KPI cards with a small coloured tick above an uppercase label, a large serif number, and a one-line plain-language caption.
- **Charts**: simple horizontal bars with direct value labels, light grey track, no gridline clutter, no legends when direct labels work, clear units. Colour carries meaning (accent = normal, warm = needs attention).
- **Tables**: light header band in small uppercase, thin row separators, a highlighted selected row, risk shown as a tinted pill with a short bar.
- **Detail panels**: label–value pairs with small uppercase labels, one clear next-step sentence, one primary action button in the accent colour.
- **Honesty line**: a small, always-visible notice that the data is strictly synthetic and the scores are illustrative.

## Changing the accent colour
The user can ask for another colour ("blue webapp"). Derive the palette from it instead of swapping a single hex: define CSS variables for accent, accent-dark (headlines/rules), accent-tint (hover, selected row), warm-attention, risk-tint, surface and border. Choose the attention colour so it contrasts with the accent (for a blue accent, amber stays good; for a teal or green accent, amber or terracotta). Check contrast of text on accent buttons (WCAG AA) and keep neutrals warm or cool to match the accent. Expose the accent as a project variable or a single CSS variables block at the top of the file so it can be changed later.

## Building it in Dataiku
- Prefer a standard webapp (HTML/JS/CSS + Python backend) that reads the project's datasets through the Dataiku API; avoid hard-coded numbers. Cache queries so it opens fast.
- Connect to the data the story needs: typically the scored dataset, the prepared reference data, and the agent if there is a conversation. Filters and actions must really work.
- Show real signals from data quality or prepared data where useful (for example a flag "data corrected during preparation").
- If a button triggers the agent (for example "Generate account brief" or "Ask the copilot"), call the project agent and render its answer in the page.
- Keep fonts self-contained or use a safe system stack with a serif fallback, since the demo may run without internet.
- Make it responsive enough for a laptop projector at 1280–1440 px wide.
- Language follows the demo language.

## Quality bar
Open it, resize it, click everything. Check: numbers come from the data; empty and loading states look intentional; no text overflows; the first screen answers "what should I look at now?" within five seconds; the synthetic-data notice is visible; the accent matches the request.
