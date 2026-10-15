# Original data rebuild checkpoint

This is a work checkpoint, not an installation release. The last released v04 patch remains separate.

User scope: replace experimental content/layout/UI/data with the existing Fairy Tamer source archives and supplied videos. Do not introduce outside data or experimental buttons. Keep v04, deliver replacement files only after testing. User authorizes autonomous fixes and broad testing. User also asks to resume after a five-hour usage window without waiting for another message.

Completed source extraction:
- 214 original scenes, all entity positions, navigation and water polygons, indoor furniture placement.
- 374 configuration tables decoded from MemoryPack using field metadata. Two tables have schema version mismatches and must be corrected.
- Original MapArea, MapPoint, MapMini, Npc and Model tables linked. 15,711 NPC/spawn records, 1,098 region records, portal destinations from BirthId.
- English labels and dialogue extracted from original language data.
- Original Main/Map/Role/Common/Base FairyGUI atlas data extracted. 197 interface sprites cropped with separate alpha channels.
- Original click, door and Pallet music audio exported.

Current code:
- public/original-world.js is the generic scene loader. It mirrors mesh geometry with corrected winding, loads actual scene cells, uses original NPC positions, portal destinations and navigation.
- public/scene.js was rewritten around original areas and interiors. Camera now faces the front of houses; controls correspond to that view. Old procedural rooms and region lists are gone from this renderer.
- public/original-ui.js and original-ui.css replace the test sidebars and controls with original icons.
- server/original-adventure.mjs implements original quest IDs, links and area state alongside the battle engine.
- server/index.mjs adds /api/create and worldVisit/worldTalk/worldEvent actions, preserves saves.

Testing in progress, not yet release-ready:
- fairy-work/original-smoke.cjs tests home 2F -> stairs -> Mom -> house exit -> lab -> professor. Latest run ongoing.
- First smoke found and fixed the removed water-test listener leaving ui.js partially initialized.
- Also fixed early-ready status before initial original quest update finished.
- Need inspect screenshots and fix navigation/portal/door placement issues.
- Need migrate remaining outside Pokedex/move/learnset/evolution/reference data to original config sources and remove all external image URLs.
- Need connect original species portraits from EudemonIcon FGUI package, original dialogue/quest flow and wild pools.
- Need expand test coverage to each exposed feature. Do not claim all 214 scenes or 2 GB of assets have been manually played.
- Need update source package/install docs, save a cumulative v04 replacement and show accurate scope.

Useful source workspace paths:
- fairy-work/raw: original UnityFS bundles from 18 uploads.
- fairy-work/inventory.json, cab-index.json, Model.dll metadata for interpreting data. Do not ship proprietary DLLs or transplant client code; use schemas and assets/data.
- fairy-work/memorypack.py, config-schema.py, export-worlds.py, augment-original.py, fui.py, crop-native-ui.py are extraction tools.
- fairy-work/rebuild-original-materials.py rebuilds original terrain shader textures, currently running or just completing.
- public/assets/imported contains the existing 8,015 converted model library and textures. Reuse it; do not discard full asset packs.

Browser test environment: Playwright installed under /opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright. Chromium at /tmp/pokemon-browser/chrome-headless-shell-linux64/chrome-headless-shell. Start server and browser in the same exec process due network namespaces.

Latest user repository path: C:\Users\User\Documents\GitHub\Pokemon_J.

## Follow-up checkpoint — 2026-10-15

Current source is /workspace/scratch/eedb2c2efe29/restored. Restored all twelve v04 converted asset packs and the imported-assets subtree of the existing v04 patch. Old scratch had an older partial project.

Changes and evidence
- Fixed navmesh coordinate conversion. Source navigation X is opposite to scene/NPC X. Converted polygon X once before indexing, height queries and water rendering.
- Executed actual pathTo/updateNavigation against original room data. Upstairs stairs, downstairs Mom and downstairs exit all reached interaction range in Node simulation. This is not browser play testing.
- Validated 214 scenes and 2,943 portals. All portals have nearby navigation, all destination scenes resolve and all referenced static model files exist after restoring assets. Exact results in fairy-work/original-navigation-results.json.
- Seven tower links have spawn scene 2520008 but area scene 2500001. Client changeArea and server originalVisit now prefer the native destination spawn scene, then region scene, then area scene. sourceDestination preserves the native scene.
- Replaced rectangle minimap drawing with overhead rendering of loaded original geometry. Syntax checked only.
- Added navigation diagnostics to getVisualStatus.
- Fixed Playwright waitForFunction options argument placement. POKEMON_TEST_CHROMIUM can override executable path.
- Added six server tests for original quest order, duplicate rewards, explicit starter event, travel constraints, return spawns and tower destination. All 33 npm tests passed.

Visual verification blocked
Previous Chromium executable is absent. Playwright browser installation failed repeatedly because download responses were not valid ZIP archives. No browser screenshots or play testing occurred in this follow-up. Do not mark this checkpoint release-ready or replace the released patch with it.

Still unfinished
- Original species/move/reference conversion and source portraits.
- Full original battle, field pool and menu bindings.
- Two source config schema mismatches.
- Browser verification of stairs, doors, collision, lab dialogue, starter preview/confirmation, minimap, jumps/water and menus.

No saves changed. No push/deploy. Checkpoint excludes large imported assets. Restore those from twelve v04 asset archives plus only public/assets/imported from the existing v04 patch.

## Continued work — active metadata and original encounter bindings

Source archives restored under fairy-work/raw (28,569 files), not included in this checkpoint. All eighteen FairyAssets archives remain in Library. Recovered English language table (59,992 entries) and fast inventory. Source UnityFS files have a 32-byte zero prefix; new recovery tools strip up to the UnityFS signature before UnityPy loads them.

The two config errors are fixed. PveBossCopyConfig and TeraRaidBattleCopyConfig have a nonserialized trailing multiDicDess cache. Removed that field from decoder schemas. decode-all-configs.py now reports 374 tables and zero errors.

Active changes
- public/data/pokedex.json, abilities.json and type-chart.json now derive from original configs and English strings. No legacy statistics copied. Existing identifiers were used solely for save identity matching.
- Catalog has 1,235 non-shiny forms and 1,027 unique numbers, including two original custom species beyond number 1025. Shiny copies map to normal species IDs and retain shiny state.
- Exported and cropped 1,232 original portrait files. Verified starter portraits visually. Fixed packing rotation from ROTATE_90 to ROTATE_270. Most forms have local portraits. MEGA Zeraora original ID16807 has no pm6807 portrait in source atlas, explicitly null imageUrl rather than substituting a wrong picture. Its exact native 3D model exists.
- Corrected 75 previously rotated native UI icons. fix-native-ui-rotation.py is a one-time migration with ui-rotation-fixes.json guard.
- pokemon-3d.js now uses original ModelConfig.Prefabs and all manifest.models. The old manifest.pokemon map excluded 261 forms. All 1,235 active source forms now resolve to exact model names.
- app.js uses only catalog local portrait URLs. Removed hardcoded external Pokémon image fallbacks.
- server/original-encounters.mjs uses original field pools, validates field scene/area, retains species/monster identity, fixed levels and stars.
- Road trainers use PveTrainer -> TrainerMonster -> EudemonMonster teams. Gym/Elite challenge binding uses source PveFight group with first rank only. No difficulty selector yet. Existing starter placeholders removed from encounter endpoint. Unsupported NPC battle bindings return errors instead of inventing opponents.
- Multi-opponent battles preserve player health, PP and status between opponents. Finish/reward/energy deduction occurs only after the last enemy.
- Fixed loss recovery ordering: clear battle before originalVisit so recovery is not rejected as battle still in progress.
- Fixed zero spawn lookup in client and server. source spawns['0'] is unrelated battle content and must never be selected for absent spawn IDs. This was caught by HTTP integration testing.
- Removed unused public/world-runtime.js and unused experimental worldModels definitions, retaining source player model.

Validation
- npm --prefix pokemon-j test passes 43 tests.
- fairy-work/check-navigation.mjs passes actual pathfinding simulation for stairs, Mom, house exit.
- fairy-work/original-api-smoke.mjs passes live HTTP account creation, source quest sequence, explicit starter confirmation, fixed source Route1 pool, invalid-field rejection without energy charge, native trainer roster and retreat energy.
- Catalog test verifies source statistics/abilities, exact model links and local portrait presence with the one explicit missing image.
- Syntax checks passed for changed JS modules.
- Source navigation validation from previous checkpoint still records 214 scenes, 2,943 portals, zero unresolved destinations/static models.
- Browser play testing remains blocked. Local Playwright browser download failed. Cloud Browser also returned ERR_CONNECTION_REFUSED for localhost:3110. No full-game visual validation claimed.

Still unfinished — do not mark complete
- Derived source moves (3,869), learnsets, evolution records and pools are in public/data/original/derived. Moves/learnsets/evolution remain STAGED, not activated in battle rules. Source effect interpreter and evolution cost handling still need implementation.
- Active reference endpoint, tutors, training item shop and some mechanics still use old metadata. Do not claim outside-data removal is finished.
- Full original FairyGUI hierarchy/layout, all menu bindings, source quest battle rewards/EXP, quest visibility/gating, all NPC story interactions and boss difficulty selection remain pending.
- Owner account/authentication, online multiplayer, guilds, events, subscriptions and server systems are not complete.
- Current checkpoint is a work snapshot only. Do not publish, deploy or replace the released installation patch before browser verification and remaining bindings are done.
