---
name: survivor-first-person-weapons
description: Set up first-person weapon meshes and action animations in SurvivorDemo, including draw, holster, fire, reload, and weapon swaps.
---

# First-person weapons and animations

Start with the pawn spawned by the target map. For the indoor setup, open `BP_InteriorSurvivor` in `/Game/Survivor/Interior` and trace one working weapon from the equipped item to the visible arms, weapon mesh, and animation instances. For changes to camera zones or sight alignment, use the [indoor first-person skill](../survivor-indoor-first-person/SKILL.md).

## Select the clips and playback targets

In `/Game/Fab/KINEMATION/TacticalShooterPack/Animations/UE5/<weapon>`, inspect the `Character`, `Weapon`, and `Camera` folders available for that weapon. For example, the Herrington 11-87 character draw montage is `AM_FP_Herrington_11-87_Draw`. Search for both Draw and Equip when locating an equip action.

Inspect the montage's skeleton, slot, sequence, and notifies. Confirm the receiving mesh uses a compatible skeleton and its active AnimGraph evaluates that slot. Play the arms track on the first-person character or arms instance. When the action includes animated weapon parts, pair it with the corresponding track on the weapon instance and start both from the same action event. Use a camera track only when the current camera setup supports it and the action calls for it.

## Integrate with the equipped item

Route the animation through the existing inventory or weapon action. Check where the equipped item changes and when each mesh becomes visible. On a swap, resolve the outgoing holster from the old item and the incoming draw from the new one. Inspect notify-driven effects before wiring playback so a second track cannot apply ammo changes or trigger the same effect twice. When a swap interrupts a montage, guard late callbacks against changing the newly equipped item.

Attach held and stowed items with Snap to Target on the active character's dedicated named sockets. Keep placement and orientation editable in the socket transforms. Preserve existing socket edits when adding support for another weapon.

## Verify in Play In Editor

Use the inventory and weapon inputs in the target map. Watch the requested action from the player camera and check hand contact, moving weapon parts, and the return to ready or ADS. For equip changes, swap in both directions and interrupt one draw with another supported action. Confirm the visible weapon matches the equipped item. If the pawn switches perspective, check the outdoor held and stowed meshes after leaving first person.
