# Recovered work status — 2026-10-17

Recovered the canonical checkpoint version 6 after the local working directories disappeared. The later native Pokédex/detail work described in conversation notes was not present in that saved archive; it must not be represented as recovered or delivered.

Restored all 18 uploaded raw archives (28,569 bundle files), the 12 converted asset archives, and the imported metadata subtree from the existing v04 patch. Raw and converted model assets are excluded from the checkpoint and remain recoverable from the uploads.

Changes recovered/reimplemented in this run:
- Starter ball interaction range now derives from original NPC 1180102 CRange (2400 -> 38.4 scene units). Automatic walking uses this arrival range.
- Quest navigation to the invisible source starter NPC now walks to the actual source scene ball and opens the selection preview. No partner is granted by navigation.
- Reimplemented the original Dialogue/Dialogue_MiniWindow binding for non-combat story dialogue, including Mom and the professor. Original English talk records supply text. Explicit source window controls and Enter advance its paragraphs.
- Shared source windows now reset pivot-aligned bounds on resize and clean up registered listeners on replacement/close. Source text binding recognizes native lb_desc/lb_name/lb_title children.
- Main menu membership/order uses FunctionConfig.Pos/PosRank; IsShow=0 does not suppress core native entries. Unbound actions remain disabled. Gate helper is tested but no new menu backend is claimed.

Validation:
- 51 Node tests passed, zero failed. Includes actual scene polygon navigation for stairs/Mom/exit and laboratory starter approach, the invisible quest target binding, and original menu membership/quest/level/VIP/guild gates.
- Syntax checks passed for changed browser modules.
- Browser story test passed the actual upstairs -> stairs -> Mom -> house exit -> exterior -> laboratory door -> professor -> starter ball approach -> preview sequence. Native Mom and professor windows were visually reviewed. Preview did not grant a partner; zero page errors. See SOURCE_STORY_VALIDATION.json (2026-10-17).
- Native dialogue bounds/resize/Enter checks passed. Map/HUD/main quest regression passed: 204 markers, Back/Escape, world-input blocking, old bottom button absent, and source Go starts a 13-point path. English dialogue text bounds fit the native widget. See the newly dated validation JSON files; older checkpoint evidence remains historical.
- Verified CRC and dimensions for 9,046 exported source sprite PNGs; zero missing files. This verifies assets, not every component's behavior.
- A cumulative source UI update is split into independent ZIPs (maximum 36 MiB input content per part), excluding existing imported models/textures/animations and all account/save databases. All parts must be overlaid on the v04 project root; preserve saves and imported models. Detailed installation/scope in INSTALL_SOURCE_UPDATE_AR.md.

Not complete:
- Native Pokédex/details must be reimplemented; the post-v6 local work was lost.
- Full original battles, source move effect interpreter, other native menu backends, quest categories, water/jump connections and all-scene play testing remain incomplete or unverified.
- This is a work checkpoint, not a full original game release. Saves are not included, modified or deleted. No push or deployment performed.

Current paths: active-project and build-tools in the conversation workspace. The checkpoint maps these back to pokemon-j and fairy-work. Source package PNGs are reproducible using export-fgui-runtime-assets.py and export-ui-images.py after restoring the raw uploads. Dialogue is required in addition to the previous nine packages.
