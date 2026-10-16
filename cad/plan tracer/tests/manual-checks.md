# Plan tracer: checks by hand

Checks that a script cannot judge. Each states what to look at.

## Looking at the screen

1. Dark and light mode: every panel, field, button, the canvas, the overlays and the selection and hover colors are legible in both.
2. Collapsing panel sections: they look right collapsed and open.
3. Layout at the real window sizes, including a small laptop screen: nothing overflows or overlaps (panel, Ortho and Map buttons, info box, status bar, rulers, scale bar, minimap, Help window).
4. The snap markers for end, midpoint, intersection, extension, perpendicular and parallel are told apart at a glance, and the guide lines and the angle label are readable.
5. The nine symbols look like what they are named: stairs, rack, door with swing, gate, dock door, column, pallet, ramp, elevator.
6. Text: size, centering, rotation along a line (never upside down), dimension text placement.
7. The handles and the selection highlight are big enough to grab and see.
8. The smooth path curve looks natural, with no overshoot on sharp turns.
9. Underlays: brightness and contrast useful on a real scan, opacity, crop outline, how rotating looks.
10. Rulers (tick spacing and labels at several zoom levels), the scale bar's round lengths, and the minimap readable.
11. The PNG export, opened in an image viewer, matches the screen in color, thickness and text.
12. The saved plan SVG opens correctly in a browser tab and in another SVG viewer and shows the traced elements.

## Feel, by hand

13. Drawing by dragging, the rubber band, mouse wheel and trackpad zoom, panning, the zoom window: is the sensitivity right?
14. Typing a length, keyboard shortcuts, focus while typing in fields.
15. Is each undo step what is expected? A drag, a move of a line with its attached text, and a style change on several elements should each be one step.
16. The layer panel: is it clear enough to use?
17. Wording of hints, status text and toast messages (English, clear), and the Help window text matches the current tools.

## Real files and real use

18. The real file dialogs: picking one or several images, opening a plan SVG, saving (the offered name `<floor id>-plan.svg`), the PNG download, and the same without the underlay reference.
19. The browser's warning when closing or reloading with unsaved changes.
20. A real traced floor, such as the EG plan with a large scan (10 to 20 megapixels): speed while panning and drawing, with hundreds of elements, and whether autosave still works (browser storage limit).

## Outside headless Chrome

21. Other browsers (Edge, Firefox, Safari): does it open and work? Saving to a file there likely falls back to a download.
22. Touch use (phone or tablet), if it still matters after the desktop-only decision. Never tested.
23. The Artifact copy in claude.ai: the file download path and the PNG download.
