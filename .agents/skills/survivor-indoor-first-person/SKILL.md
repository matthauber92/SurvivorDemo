---
name: survivor-indoor-first-person
description: Use when adding or tuning automatic first-person building interiors, first-person gun presentation, or indoor aim-down-sights (ADS) in SurvivorDemo.
---

# Indoor first person

Use the working pistol in `/Game/Survivor/Maps/Lvl_IndoorCameraTest` as the reference. Inspect `BP_InteriorCameraZone` and `BP_InteriorSurvivor` under `/Game/Survivor/Interior`. Trace `CheckIndoorView`, `IndoorView`, `InteriorCamera`, and `UpdateIndoorPistol` in the current graphs. Check which pawn the target map actually spawns before extending the test setup to another building.

Drive perspective from the player's presence inside a building. Cover the playable interior with camera zones so crossing the threshold switches to first person even with empty hands. Stay in first person while any interior zone overlaps the player. Restore the normal outdoor camera and rotation behavior on leaving the last zone.

Resolve the ready pose and sights from the currently equipped gun. Re-evaluate on entry, equip, slot swap, and aim input changes. Use the pistol as the reference for input and transitions, and use each gun's own sight line for alignment. Holding aim indoors should bring the equipped iron sights or optic to the center of the first-person view. Releasing aim should return to that gun's indoor ready pose. Keep held and holstered items snapped to the mannequin's named sockets and keep placement edits in those sockets.

## Verify in Play In Editor

Enter unarmed, equip the pistol, then switch through the playable firearms from the inventory. Current item definitions include the pistol, revolver, AR4, KA47, and shotgun. For each gun, aim at a fixed target, check sight alignment and shot placement, then release aim and check the ready pose. Cross the threshold with aim held, move between overlapping zones, and leave the building. Verify the outdoor camera and aim behavior resume. Report which guns and transitions were exercised.
