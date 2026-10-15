# v04 world rebuild

Replaced the procedural outdoor test maps with MapConfig/1000001 placements. The importer resolves all 300 placement model names and 33 terrain prefabs; a shared water plane is also loaded. Prefab root translations are replaced by placement coordinates, while child transforms are preserved.

Runtime uses positive instance transforms with mirrored geometry and corrected winding. Repeated objects share geometry through InstancedMesh. Nearby cells load incrementally. Terrain shader masks were baked with their original tiling and texture layers. Cutout materials now use alpha masking.

Walk boundaries use 6,745 Detour navigation polygons from the extracted configuration, with interpolated surface heights. Swimming regions use the separate water navigation polygons. The minimap and map overview use the same world placement data. Existing starter confirmation, battle rules, storage, progression and save persistence remain in place.

Two extracted battle environments replace the earlier plain battle disc. The initial forest export was too large and was replaced by a smaller scene; no 82 MB background is required in the patch.

Not complete: original indoor layouts, all regional gameplay, online multiplayer, guilds, monthly servers and the full event/subscription design. Do not describe this patch as a complete clone.
