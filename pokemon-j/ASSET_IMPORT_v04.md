# Pokémon J v04 — imported graphics

This update keeps version 0.4.0 and existing save files.

## Install

1. Extract `Pokemon_J_v04_patch.zip` over the root of the existing project. Replace matching files.
2. Extract every `Pokemon_J_v04_assets_XX.zip` into that same root. These are independent ZIPs, not multipart archives.
3. Keep `.glb.gz` and `.json.gz` filenames unchanged. The updated Node server serves their normal URLs with gzip decoding.
4. Commit the changed files and new asset folders to the existing GitHub repository, then deploy the latest commit on Render.
5. Keep the existing start command `npm start`. No new environment variables or npm packages are required.
6. Refresh the game after deployment.

The patch includes the models needed for the starting town, indoor furniture, player and NPCs, and initial encounter species. The additional packs contain the rest of the converted library. Extract all packs for the full library.

## Changed folders

| Path | Purpose |
| --- | --- |
| `public/scene.js` | Imported buildings, trees, furniture, animated 3D characters, follow camera, walking fixes |
| `public/asset-runtime.js` | GLB and animation loading, skeleton cloning, normalized placement |
| `public/pokemon-3d.js` | Battle models and rotatable Pokédex model viewer |
| `public/app.js`, `public/ui.js`, `public/index.html` | Connect the 3D views to existing screens |
| `public/vendor/` | Matching Three.js loaders and skeleton helpers |
| `public/assets/imported/` | Converted models, textures, animations and catalog |
| `server/index.mjs` | GLB MIME types and precompressed asset serving |
| `asset-source-index.json` | Index of all 28,569 source bundles and their source archive |
| `tools/asset-import/` | Reproducible conversion scripts |

## What was imported

- All 18 uploaded archives indexed, 28,569 distinct source bundle filenames.
- 8,015 prefab models converted into GLB, including buildings, terrain pieces, furniture, player/NPC characters and Pokémon variants.
- Legacy transform animation curves exported from 11,520 bundles. They use linear vector interpolation and quaternion interpolation; this does not preserve every Unity tangent or shader behavior.
- Material textures exported, RGB mask color variants baked for the web renderer.
- 596 prefab bundles contain no renderable mesh; most are effect/camera objects. They remain recorded in the source index, rather than being counted as working 3D models.
- Unity default materials were recovered from the uploaded main APK and the 16 affected models were reconverted. The final conversion catalog has no unresolved material dependencies.

Models are loaded on demand. The current v04 patch now renders the first overworld from MapConfig/1000001: 42,256 placements, 33 terrain pieces and a shared water plane. It replaces the old procedural outdoor maps. Walking uses the extracted navigation polygons, and the minimap uses world placement data. See WORLD_REBUILD_v04.md for the current implementation and limits. Indoor room layouts still use our own arrangement of extracted furniture. The complete regional story, guilds, online battles and events are not implemented.

The Pokédex retains the existing species data. Base species with a matching imported model gain `View in 3D`. Alternate Pokédex forms without an explicit model mapping retain their images. Unsupported models fall back to existing battle images.

## Validation

- Existing 27 server tests passed.
- All 8,015 GLB files checked for accessor lengths. 690 short bone-weight/joint accessors were padded to the four-influence format required by glTF.
- Browser tests verified 3D player/NPC loading, changing leg bone poses during walking, camera movement, imported building/furniture rendering, 3D wild battle and rotatable Pokémon viewer.
- Connected-area browser tests also passed for auto-navigation, quest rewards, trainer retreat energy and wild encounter energy.
- Individual models outside the tested scenes have not all been visually reviewed.

## Reimport from the original archives

Keep your 18 `FairyAssets_XX.zip` source archives. They contain UI textures, audio, map configuration and Unity effects not all implemented by this web renderer. They are not copied into `public`, because the browser cannot run Unity bundles directly.

With Python installed, install `tools/asset-import/requirements.txt`, then run:

```text
python tools/asset-import/prepare.py "PATH_TO_THE_18_ARCHIVES" "PATH_TO_Fairy_Tamer-1.1166.apk"
python tools/asset-import/batch.py
python tools/asset-import/animations.py
```

The source index and original archives allow later work to find and convert additional content without requesting those files again.
