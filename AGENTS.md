# Item attachments

Use dedicated, named sockets on the active character skeletal mesh or skeleton for all held and stowed items. The user wants to edit attachment placement visually in Unreal's mesh/skeleton editor.

Keep placement and orientation in socket transforms. Attach components with Snap to Target; do not override socket placement with item-specific Blueprint relative-location or relative-rotation offsets. Geometry sizing for placeholder meshes may remain separate.

Current character mesh: `/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin`.
Current mesh sockets: `PistolGrip_R`, `PistolHolster`, `LongGunGrip_R`, `PrimaryHolster`, `SecondaryHolster`. Add appropriate sockets when introducing additional attached items.

Do not rerun historical attachment-generation scripts in MigrationStaging without updating them to preserve the current socket-based implementation and the user's socket edits.
