# ForgeKit Brand Colors

| Token      | Hex       | Use                                  |
|------------|-----------|---------------------------------------|
| bg         | `#0B0F14` | App background, page background       |
| surface    | `#141B24` | Cards, panels, code blocks            |
| text       | `#E8EEF4` | Body text, headings                   |
| accent     | `#F5B942` | Buttons, links, highlights, prices    |
| success    | `#3DDC97` | Confirmations, "done" states, checks  |

## Fonts
- **Headings / UI:** Inter
- **Code / numbers / prices:** JetBrains Mono

## Usage rules
- `bg` is always the outermost background. Never put `surface` directly on `bg` without at least 1px border or 8px radius separation.
- `accent` is for one primary action per screen. Don't tint more than ~20% of a screen with it.
- `success` is reserved for completed/positive states only — not decoration.
- Text on `bg`/`surface` is always `text` (#E8EEF4) or a muted variant (`#9BA8B4`) for secondary copy. Never pure white.
- Minimum contrast: `text` on `bg`/`surface` passes WCAG AA. `accent` (#F5B942) on `bg` also passes AA for large text/UI elements.

## CSS variables (drop-in)
```css
:root {
  --fk-bg: #0B0F14;
  --fk-surface: #141B24;
  --fk-text: #E8EEF4;
  --fk-text-muted: #9BA8B4;
  --fk-accent: #F5B942;
  --fk-success: #3DDC97;
  --fk-font-ui: 'Inter', system-ui, sans-serif;
  --fk-font-mono: 'JetBrains Mono', 'Courier New', monospace;
}
```
