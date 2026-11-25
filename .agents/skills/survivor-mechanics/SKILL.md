---
name: survivor-mechanics
description: Use when adding or tuning weapons, character animations, inventory, pickups, interactables, or doors in the SurvivorDemo Unreal Engine prototype.
---

# Survivor mechanics

Make the requested mechanic playable. Preserve the feel of existing actions outside the request. During prototyping, use an existing animation as a placeholder when it is enough to judge the mechanic.

## Weapons and animation

Trace a comparable weapon or action from its input through animation selection. Before editing a shared sequence, montage, blend space, or Animation Blueprint default, identify the other actions that use it. Reuse a clip directly when it fits. For weapon-specific timing, poses, or blending, use the narrowest existing override. Create a variant when the asset itself needs to differ.

When adding a branch to shared logic, preserve the existing selections, transitions, and fallbacks. If the requested mechanic requires retuning another action, explain which action the player would experience differently and ask before widening the change.

## Inventory and pickups

Trace a comparable item through `BP_InventoryComponent` and the inventory UI. Follow the existing rules for quantities, slots, equipment, and what happens when inventory is full. Preserve capacity, stacking, auto-equip, and slot replacement behavior unless the request changes them.

For a world pickup, start with `BP_ItemPickup`. One successful interaction transfers the item once. Remove the world pickup only when the inventory accepts it. A refused pickup stays available. For a weapon swap, account for both weapons, the equipped slot, and any ammo or attachments already tracked per weapon.

## Interactables and doors

Follow `BPI_Interactable` and `BP_InteractionComponent` for input and focus. The displayed prompt and the next interaction should resolve to the same object. Keep the object's response in its implementation so one press performs one interaction, including when a pickup is beside a door.

For door work, check the relevant armed or unarmed walk or run case. Preserve the other cases. Treat the start of door movement, the moment the player can pass through, and the return of movement control as part of the tuned behavior.

## Playtest

Exercise the requested behavior in normal gameplay, then check one existing behavior that uses the part you changed. Choose the check to match the risk. For pickup targeting, use a weapon beside a door and verify the prompt, the action, and the resulting inventory. For a change to the armed running door push, also walk through armed. Use `Lvl_PickupTest` or `Lvl_InteractionTest` when it contains the setup you need.

Report which actions you tried and what you observed. If verification ended at Blueprint compilation, identify the gameplay check still pending.
