# Harvested From The App Plan

The essence of the earlier standalone-app plan, kept as direction and potential. Nothing here is a specification.

## Delivery Shape

A recommendation and a potential, not a requirement: a static, client-only web application with no server and no accounts. All project data stays in the browser, projects are imported and exported as files, and the application works offline after its first load.

## Portable Project File

A project can embed its reference underlay, so one file carries both the model and the plan it was drawn over. Embedding can be declined for large underlays, in which case the underlay is referenced by file name.

## Scale Calibration

The zoning author sets the scale by marking two points on the reference underlay and giving the real distance between them.

## Route Test

The zoning author picks two zones and sees the resulting route, as a check on the model.

## Live Validation

A panel lists problems in the model (gaps, overlaps, portals off their boundary, unreachable zones) and jumps to each one when clicked.

## Open Existing Outputs

The editor can load an existing connectivity graph and its zone SVG, which is the path from the BFW review into the module.

## Automatic Changes Shown First

Any automatic tidy-up shows what it would change before applying it.

## BFW EG Underlay Registration

The 2018 Lageplan PDF is stored rotated by 180 degrees. On the half-size render, SVG coordinates equal scan pixels minus (40, 77); the full-size render is 3507 x 2480.
