# Original data rebuild checkpoint

Latest continuation: read RECOVERY_STATUS_2026-10-17.md first. The workspace was recovered from version 6; post-version-6 native Dex work did not survive. Current changes and dated validation files distinguish reimplemented work from historical notes below.

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


Continuation 2026-10-15
- Restored checkpoint after previous scratch workspace disappeared. Applied starter-binding patch; this remains a PARTIAL implementation, not original visual UI.
- Restored all 18 FairyAssets archives. Extracted all 2322 UI package bundles with source archive/member/hash provenance in fairy-work/ui-bundle-provenance.json. Raw bundles and archives are outside checkpoint.
- Recovered native package binaries. Decoder reports 57 package metadata files, 1462 components and zero decode errors. This decodes only dimensions and base child positions/source references, NOT controllers, gears, relations, transitions or extension behavior. No runtime menus switched to this data.
- Exact original opening components found in Eudemon package: EudemonGen_MiniWindow, EudemonGenChooseButton, EudemonSelect_MiniWindow, EudemonSelectItem. Selection uses model widget, list_eudemon, btn_sure, btn_close, text_gen. Previously shipped portrait UI is not this layout.
- Next: decode pivot/scale, controllers/gears and list templates, then recover atlases and resolve images before native menu rendering.
- No new installation package released. User saves untouched. assets/imported not yet restored in current workspace; full catalog model tests and browser validation cannot run yet.

## Active rebuild — 2026-10-15 native opening and texture coordinates

Current local working tree is /workspace/scratch/d0f01ad50e6b/active-project. Recovered source/model archives are in packs and restored-current/fairy-work/raw. Some previously restored files reverted while work ran; a separate copy with new file identities was used for active edits. Checkpoint packaging now maps active-project to pokemon-j inside the archive. Always verify active paths and do not edit the old restored copy.

Changes in this continuation
- Recovered57 package binaries,1462 component geometries. Enhanced decoder reads pivot,scale,visibility,loader URL,text. Controllers/gears/relations/transitions remain unresolved.
- Native opening-source.json contains11 source components and39 atlas images for generation/partner windows. Exact source geometry and original artwork render with JavaScript interaction bindings. English labels translated locally. Not original executable code.
- Generation1..9 selection uses uploaded SelectEudemonConfig and3 corresponding starters. Preview never grants a creature. Explicit Confirm submits generation/species. Back returns to generation list.
- Fixed an async race that closed the starter window when scene loading finished. Opening now awaits the3D module. Models expose ready/error status for tests.
- Recovered source shader parameters for2298 Eudmon prefab models,zero extraction errors. PokemonBase Vulkan subprogram revealed U-fold mapping discarded by the earlier importer. native-material-runtime.js applies recovered MainTex scale/offset, DoubleTex, NeedMoveUV and FlipMask1 to PokemonDate/Eye materials only. Other shaders and full original lighting remain unsupported.
- Inspected an actual browser render of generation cards and generation4 Turtwig/Chimchar/Piplup. Textures now align with faces/bodies. See NATIVE_UV_EVIDENCE.md for source math. No screenshots stored as deliverables.
- Removed unused experimental building/character/NPC sprite sheets and external portrait folder from active tree after checking for runtime references. Do NOT ask the user to delete saves or source imported assets.

Validation recorded in OPENING_VALIDATION.json and HTTP smoke script.45 server tests passed after model catalog restore. HTTP smoke passes opening quest order, invalid generation rejection without granting a partner, explicit generation4 Turtwig selection, source Route1 pool, invalid field rejection and source trainer roster/retreat cost. Browser checks are separate and limited to opening; do not claim exhaustive game testing.

Still NOT COMPLETE
- Original map/menu/battle replacements are not fully implemented. Details from opening still uses the existing custom Pokédex detail window.
- Old battle/move rules, reference/training menu metadata and other prototype systems remain as documented above. Do not claim all prototype code removed.
- Home floor/stairs/Mom/lab/source portals have prior data/path/HTTP evidence but have NOT all been played through in this run's browser.
- Full source quest rewards/gating, all NPCs, swimming/jumps, all portals, online/auth/subscriptions/guilds/events remain unfinished or unverified.
- The new native-opening patch is a bounded partial installation update. It does not convert the full game to the original client.
- User saves unchanged. No push/deploy performed. Full imported models excluded from checkpoint; restore12 converted packs and imported subtree of original v04 patch when needed.18 raw FairyAssets archives remain authoritative.

Continuation 2026-10-15 — IN PROGRESS, not an installation release
- Expanded source UI search to UIActivity directories:93 native packages,3043 components,0 decode errors. Main package was missing previously.
- Extracted9 original FairyGUI packages, atlas provenance and9039 unrotated/untrimmed sprite PNGs. Engine adapter uses lazy original textures, preserves source controllers/gears/relations. Third-party FairyGUI-three engine license included; all game artwork remains uploaded source.
- Recovered8 source camera prefabs and applied MapArea.Camera settings in source-camera.js. Actual game camera still needs browser verification.
- source-map.js creates uploaded ShowMap_Window +ShowFiestMap +204 source markers. Original MapMini.Point/area lists bind player and destinations. Browser screenshot confirms source illustrated map/frame/sidebar, corrected clipping. Travel/locking/resize still require integration tests.
- scene.js now delegates map opening to source-map.js and removes old rendered-room overhead map implementation. Mini-map image rasterized directly from45 Common/BigMapCom source sprites with source transforms. Removed Inspect Poké Ball bottom button; click/Enter interaction remains.
- IMPORTANT: Main HUD, custom quests, Pokédex and battles still not replaced. Do not claim complete original client. Do not distribute this WIP checkpoint as tested installer.
- Rebuild excluded reproducible package PNGs via export-fgui-runtime-assets.py/export-ui-images.py (requires raw bundles). Retains .fui, manifests, configs, adapters and scripts.

Validated source-UI partial delivery before requested pause
- source-hud.js now renders Main/Main_Bg; old profile/toolbar/quest/minimap HTML hidden after successful native initialization. Old original-ui.js no longer loaded. Unbound native menu actions disabled, not connected to prototype popup handlers.
- source-quests.js renders Assignment/TaskCenter_Window, current source main chapter, current objective, source item icons/qualities/counts, source Back and Go. Side/Daily/Bounty tracking remains UNBOUND and tabs disabled.
- Browser integration latest check-integrated-hud.cjs passed native HUD creation,204 map markers,current region,Back/Escape,UI blocking,old bottom button removal,source quest UI and actual Go click. Go starts13-point path toward home stairs. Does NOT prove whole walk/Mom completion.
- Fixed upstream FairyGUI-three nine-slice tile row integer division (`row=pi/3` ->Math.floor). Last browser geometry diagnostic reported [] instead of two NaN meshes. Back English label explicitly uses source LanguageClient.ComBack.
- Native main menu closes visually via source BagState binding. Menu backends, Pokédex, native dialogue/battles, all quest categories and mobile joystick remain incomplete. Original HUD task objective text visibility needs follow-up, current chapter label displays.
- Full release install guide INSTALL_SOURCE_UI_AR.md explicitly describes partial scope. No saves packaged or removed. User requested pause and continuation at20:30 Asia/Amman today.
- Further raw extraction currently blocked by missing UnityPy Python dependency.9 extracted UI packages and all raw packs remain local; Eudemon/Bag/Dialogue/Battle extraction was attempted but not completed. Do NOT claim those packages restored.

Continuation 2026-10-17 — six reported defects, work in progress
- This section supersedes older missing-dependency and disabled-menu notes. UnityPy and raw source packs are restored locally. No installation patch from this six-defect pass has been delivered yet.
- Server resources now bind LevelUp.PowerMax/FatigueMax, GlobalValue.PowerReply/FatigueReply/NeedFatigue, source trainer NeedPower, PowAndFatBuy, Vip and ItemGift. Separate persisted Energy and Zip; preserve account/partners. Server save ordering fixed so migrations persist on GET.
- Native menu routes for Backpack, Gold shop and Pokédex plus both native resource refill windows are connected. Other menu services remain incomplete and report unavailable instead of opening prototype popups. Four native windows opened/closed in browser with zero page errors; item transactions and all physical controls still need additional tests.
- Exported Bag,Shop,Gather,Pve plus other source packages. Runtime currently registers baseline packages plus Bag/Shop/Gather/Pve only. Checkpoint excludes all package PNGs; restore source UI patch or reproduce exports from raw packs before running.
- FieldEudemonConfig contains BoxId, Step ranges (e.g.15..30), weighted trainerMonster and per-field records. source-field-steps.js binds source-unit walking distance to these records and group5 scene cells; Enter no longer initiates wild battles. Source-unit interpretation is an adapter reconstruction, not recovered executable logic. Actual walking encounter browser test is currently running; do not claim validated until SOURCE_WALKING_CATCH_VALIDATION.json exists with success.
- Blue stripe reproduced in world screenshot with HUD hidden. It is synthetic water navmesh rendering from OriginalWorld.addWater, not a source scene asset. Removed call; native water models/navigation remain. Post-fix screenshot still pending.
- Preview/battle renderer dispose previously retained WebGL contexts. Added forceContextLoss after disposal. Actual route renderer survived20 source-model preview creations/disposals with contextLost=false. This is bounded evidence; user blank-screen cause is plausible context exhaustion, not proven exclusive cause.
- 58 Node tests passed at this point, including5 source resource tests and2 source field-step tests. Native inventory module and latest changes need further tests.
- Top activities remain incomplete: assets and6 ActivityWindow catalogue records exist, but active-event calendar/server eligibility records have not been located. Do not turn source promotional records into invented live events or rewards.
- Local base restored floor models currently render white (terrain material texture not bound in imported base packs); user screenshot had textured ground. Do not ship those restored base models over user's working terrain. Further original material extraction may be needed for representative world QA.
- User's correct Windows root is C:\Users\User\Documents\GitHub\Pokemon_J. They previously ran Desktop\pokemon by mistake; current screenshots use correct native HUD. Do not delete saves/imported assets. No push/deploy.

Validated incremental repair delivery — 2026-10-17
- SOURCE_WALKING_CATCH_VALIDATION.json now exists: actual keyboard walking on source field120101 triggered Pidgey without Enter; stationary position did not trigger;3Zip consumed, Energy unchanged, retreat preserved world context,zero page errors. Early failed attempts did not walk far enough on the software renderer (13.6source units versus source threshold20); final test waits for actual displacement instead of assuming real-time keyboard duration equals distance.
- SOURCE_RESOURCES_HTTP_VALIDATION.json passes exact68/68 level5limits,invalidfield nocharge,source3Zip cost,50gem refill,separatepurchasecounters,fullrefill nocharge,trainerretreat nocharge and persistence.
- SOURCE_BINDINGS_VALIDATION.json includes an actual physical click from Main menu to Bag and opening/Escape closing all4 native windows with no page errors. Portrait in Gather's offscreen placeholder is centered on its native model target; template UR rarity is replaced by actual source rarity text. Recycled dex cells no longer accumulate old click closures.
- Walking speed now uses GlobalValue.BaseSpeed fixed-point value divided by10000 times source world scale, replacing85. Navigation VM tests receive the same source speed record.
- Synthetic water material/method removed, not just hidden. Original scene objects and water navigation retained. Post-fix walking screenshot has no horizontal blue navmesh surface.
- Prepared Pokemon_J_v04_resource_walking_update.zip:133replacement files,about5.2MB. No saves or imported geometry/textures overwritten. Install directly into C:\Users\User\Documents\GitHub\Pokemon_J with replacement. Guide INSTALL_RESOURCE_WALKING_UPDATE_AR.md explicitly distinguishes completed/partial/unavailable behavior.
- Final installer was extracted over prior cumulative source update in delivery-validation; native windows/main-menu Bag click pass there. Final Node test run after navigation harness source-speed update passes61of61,zero failures.
- This does NOT finish all6 defects. Resource and wild-walking bindings plus synthetic-stripe removal are verified; renderer context fix has20preview survival evidence,not proof of every blank-screen cause. Only Backpack,Gold shop andPokédex main services are bound; other menu services remain unavailable. Top live activities still unbound because active-event/eligibility records and service executable behavior have not been located. Never claim all original prototype code removed or full original client restored.


Continuation 2026-10-17 menu/dex and source client recovery (partial)
- Workspace had been cleared. Restored canonical v10, all18 raw archives (28,569 bundles) and latest source UI archives; restored package artwork and native model catalogue. No user saves present or modified.
- Fixed source-dex-records.js: Gather catalogue rows must reference EudemonId, not row Id. All9 generation source membership/order tested; browser physically clicked generations2/3/5/9 with127/135/158/120 records and no page errors.
- Bound original Main img_menu close tab. Physical open/close clicks passed. SOURCE_MENU_DEX_VALIDATION.json records current evidence.
- Resource HUD now shows actual independent balances; if backend lacks resource state, displays unknown plus source level capacity and requests restarting the updated backend, rather than silently blank/fabricating balance. Values260/260 and267/260 and stale-backend cases tested. This is diagnostics, not proof of fixing the user's running server.
- All65 Node tests passed after restoring imported/catalog.json. Browser native Bag/Shop/Gather/resource window open/Escape checks passed; SOURCE_BINDINGS_VALIDATION.json updated.
- IMPORTANT newly recovered original executable client code: Hotfix.dll and Model.dll plus complete type/method indexes, original147 activity config categories, decoded70 ActivityDefaultBase,107 ActivityDelegation and72 ActivityTemplate records. Research preserved recursively in checkpoint. Original assembly source raw bundle names10bf5a811ee6452184a01b2b004033c8 and13f197e3032e0c2f2b37d8e604c99e23; activity bundle7b5a6511828c5adf75b7dec93d491a2e.
- dump-client-il.py resolves generic native window names; recovered original FunctionJump54580, activity Jump74877, CheckFunctionCondition43007, GetActivityBaseByType43005. This supersedes older notes claiming no activity/code records available.
- Source routes: function161 opens Gather(all species),202 opens Eudemon(owned creatures). Current HUD incorrectly aliases202 to Gather; correction/owned Eudemon window binding still pending.
- Original activity501(Welfare) opens Activity/ActivityUI_Window;502(Events) opens Activity/ActivityDailyUI_Window;317 opens RechargeShop/RechargeShopAll_Window. CheckFunctionCondition501/502 requires actual active instances at positions12/11 respectively. Do not show historical events or fabricate live rewards.89 of107 delegation records use old absolute timestamp windows;13 permanent,4 relative to server opening,1 relative to role creation. Server eligibility/live-instance services still unresolved. Top activity strip remains incomplete, not delivered as working.
- Source Activity and RechargeShop atlases exported from raw assets, sprites exported; not yet runtime registered or validated. Current package PNGs remain excluded from checkpoint, reproducible via export scripts.
- Next: inspect original ActivityComponentSystem3057/3059/3067 and runtime message schema for real active-instance/gating; then wire strip and native activity panels with source-backed services. Preserve saves, no push/deploy.

- Follow-up original code3057/3059/3067/3068/3069 recovered after first save: active activities come from PlayerActivityInfoList and component info, not merely catalogue rows. Client checks level/quest gates plus service-specific state (funds, gifts, completed offers). No original server namespace exists in recovered Hotfix code. Preserve this distinction; local activity service still requires implementation.
- Activity/RechargeShop atlas and image exports completed:1481/252 sprites. Runtime not registered yet.
- Prepared bounded incremental Pokemon_J_v04_menu_dex_update.zip with only3runtime files plus Arabic instructions. It does not implement the activity strip or all menu services. Existing saves/assets preserved. Physical HUD resource text68/68,68/68 checked in browser, alongside menu close and later-generation checks.

2026-10-18 recovery checkpoint — WIP, not installer
- Maintenance cleared scratch before Oct18 continuation. Restored remotev12. Prior unsaved Oct17 player/ledge/water edits were lost and are being reconstructed from recorded source evidence. Do not claim previous transient test results apply to current files.
- Reapplied separate-resource over-cap regeneration preservation, localized function OpenDes keys, hidden menu entries above source level cap, original RoleCenter/owned Eudemon window adapters and corrected function161/202 routes. Player views not yet browser-tested in current tree.
- Reapplied directional TileType71..74 ledges (1.2source-unit landing probes, up to6 attempts), original Boy Jump animation, automatic-navigation waypoint continuity, source-only portal labels. Code checks and resource/navigation tests pass where noted; physical checks pending model/art restore.
- Restoring original18raw packs,12converted packs and prior UI archives in packs using current transfer helper. Do not ship untested player UI yet.
- Top activity service and downward-facing head issue remain unresolved. Water material colour binding must be reproduced using original SampleWater._WaterColor [0.1411764770746231,0.2549019753932953,0.5647059082984924]; original model e1476ae351dec682f4304a23e87ad1a7. Raw shared material ae65c719f3f4998cbc93a9fa20bb54b7.bundle.

2026-10-18 validated reconstructed bindings
- Current tree, not prior lost edits: 68/68 Node tests pass. Separate HTTP resource persistence/regeneration/refill checks pass. SOURCE_RESOURCES_HTTP_VALIDATION.json.
- SOURCE_PLAYER_VALIDATION.json: physical head click opens RoleCenter; physical function202 opens owned Eudemon; two source creature cards select correctly; four tabs clicked and data row counts checked; Escape closes; no JS page errors. Source English strings explicitly selected for ambiguous Chinese labels. Move names matched against original SkillConfig; source PP and type bound. Unsupported training/mutation controls hidden/disabled.
- SOURCE_LEDGE_WATER_VALIDATION.json: actual ArrowDown on source Viridian type72 enters Jump clip and lands south. Reverse condition covered by Node real-scene test. Actual loaded SampleWater RGB equals original _WaterColor. This is material colour only, not the Unity water shader.
- SOURCE_GAIT_VALIDATION.json: actual quest auto-navigation walks multiple path waypoints with Run and varying calf bone poses. Fixed reached-waypoint idle frames. No claim of identical original pathfinding.
- Player face when facing down remains unresolved. Top live-event strip remains unbound: recovered client requires server PlayerActivityInfoList and service state; do not fabricate from historical catalogues. No full prototype removal claimed.
- Portal labels now source Name only, no destination-name inference. This removes unproven labels, not a complete original sign system.
- Incremental delivery: Pokemon_J_v04_source_bindings_update.zip, Arabic guide INSTALL_SOURCE_BINDINGS_AR.md. Includes backend resources plus original Eudemon/Role artwork, runtime changes, Jump clip and ONLY changed water model. No saves/deploy/push. Keep v04. Read installer manifest for exact files.

2026-10-18 new seven-issue pass — bounded partial, not seven complete
- User confirmed resources, automatic quest gait and RoleCenter worked; new requests: native battle, absent building names, flat grey water, four quest tabs, downward Run face, all shop categories, bottom Friends/Assistance/Chat/mount bar.
- New screenshot inputs actually opened from upload. Face issue has concrete conversion cause: source avatar e711... renderer4134019437585199084 face has one Head bone and one bindpose,241vertices, but Unity omits explicit weights. Previous convert.py required nonempty weights, emitted static face. bind-source-rigid-face.py adds implicit weight1, original inversebind and original Head joint to avatar GLB. convert.py fixed for future implicit rigid skins. SOURCE_FACE_SKIN_BINDING.json preserves exact matrix.
- Original face mesh dependency CAB-dcbbcd3f441cdcca697abe05ed4e669d was found via raw binary match: bundles28aa1af281d2a31f9b4066b2c3613ee0 and245350332180f026b3e660b99a55b847. Scripts load these directly; no global CAB index needed.
- Water now full original GLES fragment extracted from shader2891417073959985199 Pokemon/SampleWater in98011065... +materialae65... +normaltexturebundle98e8.... export-source-water-runtime.py extracts source uniforms/pass state and textures. Source-water.js adapts world handedness/scale, camera depth prepass and existing Three lighting. Source forward pass zWrite0,SrcAlpha/OneMinusSrcAlpha. Do not claim exact Unity lighting parity. SOURCE_LEDGE_WATER_VALIDATION now records runtimeWater.depthFrames, faceSkinned Head, actual down Run and zero shader/page errors.
- source-building-labels.js uses portal NPC name or original linked interior MapArea name,Type2only. Source destination-name fallback is now explicit mapping requested by user; do not describe its screen position as recovered original billboard behavior. Two source-record tests +physical Viridian centre render pass. SOURCE_BUILDING_NAMES_VALIDATION.json.
- source-quests.js tabs respond with original FunctionConfig unlock messages instead of hardcoded untouchable. Main still works. Unlocked other category instances/services remain unbound, reported explicitly. SOURCE_QUEST_GATES_VALIDATION.json is locked-start-account response only.
- Original TaskCenter23743/23747/23757 and async64303 recovered: Pos14serverfunctionlist, BranchQuest/ListQuickBranch, NewTaskBranch/TaskDaily/TaskOfferReward. Source quest side gate1000304,daily1003103,bountyLevel40. Do not populate fake quest progress/rewards from catalogue.
- Original ShopWindow7877/7880/7874/7888/async55107 recovered. Uses ShopCompoment.GetShopType and server QueryShopList shopInfo.list, not all catalogue rows. ShopType27 configs include special screens, future Level9999 privilege. Current gold-only shop unchanged; no fake rotating stock.
- Original Main lower UI: g_chat,g_mount were hidden by our adapter. Source Main15602 requires owned ListMount +function107 +scene conditions. Friend59767 routes FriendWindow. Main15619 UpdateGameHelp always hides btn_gameHelp in this client version; do not assume that is user's Assistance button. Need inspect btn_come andChatView. Bottom bar still unfinished.
- Battle original package exported (4atlas bundles,207sprites), native NormalBattle_Bg inspected; tree/screenshot only /tmp, no functional replacement. Production loader does NOT register Battle yet. Source battle art exports exist in packages but are not installer dependencies. SourceBattle prototype remains until real scene/camera/commands bound.
- Original battle scenes all in raw01fd539f979286f109329b1f300b6a38.bundle, including skyland,skylandGrass,skylandRoom etc. Camera prefabc483baf3e646f1d59aa603b179dbcb37. FieldEudemon.MapAreaId links area with FightScene,warPoint; outdoors can have empty FightScene. Need recover default selection, native placement and scene cameras instead of keeping battle-forest/circle/sphere FX.
- 70 Node tests pass. Partial installer Pokemon_J_v04_face_water_update.zip contains only verified face/water/name/tab-response files, no floors/saves. Guide explicitly lists remaining4 areas. Do not claim all7fixed or all29kassetsused.

2026-10-18 continuation after scratch cleanup — WIP
- Restored canonical v15. Unsaved previous native battle/shop continuation was lost; reimplementing, no claim prior browser evidence applies.
- Restored all18raw FairyAssets,12converted packs and11source UI packs. Current scripts in build-tools, raw in restored-current/fairy-work/raw.
- source-shop.mjs now exposes8Pos10 shop categories from original tables, server validates source prices, limits, gates, currencies. Stock grouping/weighted selection and UTC rotation are local service adapter choices inferred from config, not recovered original server code.4unit tests pass. Source frontend native Shop_Window and ShopBuy_MiniWindow bound; browser rendering passed; physical buy/refresh still pending.
- source-quests.mjs typed server events (NPC talk1/shop9/capture13/trainer3), source branch/daily records, one-time rewards.3unit tests pass. Bounty deliberately has no generated catalogue instances: original active-instance service unavailable. Native4tab rendering passed in browser with fixture. Deliver/collection/service quest types not yet bound; do not claim all quests playable.
- Battle sourceUI/scene reimplementation underway, not release-ready. Native package exported,26source scenes exporting. Original camera source c483...,25degrees, source1v1 positions from BattlePos ctor55583/GetPos4458. Native renderer newlywritten, browser battle still pending. Server selects original FieldEudemon.MapAreaId->MapArea.FightScene. Need complete old-save battle context repair, medicines, animation and tests. Do not delete saves.
- Bottom bar Friend/Chat/Mail(GameHelp) native packages exported; no working social/assistant/mount service yet. Need recover actual owned mount state/attach binding, no invented mounts.
- Current77Node tests pass, source shop/quest native rendering noJSerrors. This is WIP not installer.


2026-10-19 first-two source-index pass — validated bounded delivery
- Restored canonical v16, queried persistent source index first; no repeated global asset inventory. Recovered missing local base assets from the original bundles; those base/world/player files are NOT included in the installer.
- Native battle rendering now has 25 exported original source scenes, original camera and position records. Removed erroneous camera.rotateY(pi). Exact-source geometry buffer/mesh deduplication reduced scene gzip size from about100MiB to11MiB; original textures preserved. skylandDodge has no renderable mesh and remains explicitly unavailable.
- Actual browser test: original skyland + Battle/NormalBattle_Bg, physical attack/PP, physical retreat, physical ball menu/use/inventory decrement. No claim all scenes playtested. SOURCE_FIRST_TWO_VALIDATION.json has zero page errors in final test.
- Building names use existing original NPC/destination-area records; layer moved into world scene wrapper independently of HUD. Audit521 source exterior entrances, no unnamed records; physical Viridian centre door/return passed; centre/mart/school labels visible with original Main HUD ready. Floor materials in restored local base packs still differ; no world floor files shipped.
- Old battle save context repaired ONLY when uniquely proven from source area, trainer, or monster+field records; team, HP, PP and inventory unchanged. Three new source-context tests pass. Full80 Node tests pass.
- Incremental Pokemon_J_v04_first_two_update.zip:288 files,40,190,550bytes. Requires existing12 converted model packs and prior source UI installation. Contains native battle source files/scenes/new textures and building label relocation. tools/install-first-two-v04.mjs patches existing server/index.mjs narrowly and keeps backup; tested old shape and repeat installation. No full replacement server index in delivery, no saves, no push/deploy.
- IMPORTANT: native battle presentation is connected to the existing LOCAL combat service. Damage/capture outcome algorithms and original skill/capture effect timelines are NOT fully reconstructed. Great Ball disabled because service does not support it. Source UI does NOT imply original server equivalence. Remaining five issues unchanged; source shop/quest WIP in checkpoint is not newly delivered.
- Reference index persists as libfile_14fa0b2178608191b5132cbafafdf38c and DB libfile_834574ff89d4819181d5b3fcd8a77710. Query these before any raw archive work. Current local restored tree is rebuild-current/pokemon-j and tools rebuild-current/fairy-work.

2026-10-19 water instance repair
- User confirmed native capture UI/buttons solved. Building names exist but presentation still incorrect. Added issue8 original attack effects; do not modify these while working on water.
- Water RawShaderMaterial previously ignored instanceMatrix, while OriginalWorld renders it as InstancedMesh at source position/scale16. Added explicit SOURCE_INSTANCED material variant and original world matrix/normal transform. Fragment shader, original colour and normal maps unchanged; per-slot material replacement preserves other materials.
- Actual source water geometry GPU test at x24000 scale16: before missing water/red background, after blue pixel[41,70,149] and time5000 pixel[42,71,150], no shader/page errors. SOURCE_WATER_INSTANCE_VALIDATION.json. World appearance still requires user confirmation, not all regions playtested.
- Delivery Pokemon_J_v04_water_update.zip only8 files; no saves/backend changes. Fast-work reference now has8 issues and current state.

2026-10-19 quest tab repair
- User confirmed water solved. Native capture UI remains solved, building-name presentation remains open, move effects tracked as issue8.
- Source quest four tabs now exclusive, return Main hides other panels; locked tabs show original unlock condition without granting access. Unlocked branch/daily source records rendered. Daily complete progress corrected to required instead of0; claim stays one-time. Recycled cell/bonus click handlers removed before rebinding.
- Native branch Go passes selected source target8110103; source service Link uses existing supported native panels with error handling; unsupported services remain explicit, no fake progress.
- Original category gates preserved. Bounty has no fabricated active instances; original service and many quest action types remain incomplete. Do not call entire quest system restored.
- Physical locked/unlocked four-tab cycles, Main return, native records, branch Go and zero page errors verified in SOURCE_QUEST_TABS_VALIDATION.json with separate fixture. Five quest unit tests and existing opening tests pass.
- Pokemon_J_v04_quests_update.zip uses tools/install-quests-v04.mjs to narrowly integrate source quest categories/events/claims into user's existing backend, backed up and repeat-install tested. No replacement server index or save files.

2026-10-19 face model recheck and user correction
- User says quest issue4 remains unresolved; wait for video before new quest edits. Add issue9 HP growth per creature level and creature-detail tabs. Do not treat either as fixed.
- Current local source avatar visually correct in Idle/Run facing down/camera. Verified face241 vertices, allHeadweight1, singleBip001 Head joint and inverse bind matches original Unity mesh. No runtime code changed, no reproduced local rendering fault.
- Delivered small verified-source avatar+textures replacement Pokemon_J_v04_face_model_update.zip to rule out older model installed on user's machine. USER CONFIRMATION PENDING; never claim this proves issue5 fixed. SOURCE_FACE_RECHECK_VALIDATION.json.
- This checkpoint explicitly includes the small source avatar and its two textures so future restores retain verified model. No user saves or backend changes.

2026-10-19 shop category repair
- User confirmed face issue5 already solved; no need to install face recheck package. Quests remain unresolved pending user's video.
- Bound8regular source ShopType categories (Pos10,originalLevel<=100) using original Shop/ShopBuy UI. Source27types include specialized modes and Level9999privilege; do not merge/fabricate those into regular shop.
- Narrow installer patches existing server state/buy/refresh and only HUD shop route, preserving other fixes with backups/idempotence. No whole server/HUD replacement in delivery.
- Recovered missing Shop atlas/sprites from original raw bundle; included native files to avoid missing texture failures.
- Actual browser gold buy: gems500->490,coins1000->11000, confirmed original BuyItem/ShopItem; physical navigation all8 tabs passed in separate unlocked fixture, no page errors. SOURCE_SHOP_PURCHASE_VALIDATION.json. Source shop/inventory unit checks pass.
- Stock group selection/UTC rotation remain local config-driven adapters, not recovered original server. Multi-quantity buy and specialized shop services not implemented. Never claim all source shop features restored.
- Delivery Pokemon_J_v04_shop_update.zip, native config tables+art+scoped adapters. User saves intact, no push/deploy.

2026-10-19 bottom bar recovery and partial source navigation
- Scratch was pruned. Restored checkpoint21, fast kit4, full source index+search DB. Indexes are persistent and were not lost. Restored9 source UI packs and5 raw packs only for current work. UnityPy and test Chromium reinstalled.
- User reports shop6 still unbound and postponed it. Do not call shop solved.
- Source bottom UI navigation WIP in public/source-bottom.js and a scoped installer. Native Friend/Chat/Mail packages and all their sprites/atlases restored from original raw. Main chat group explicitly hidden in old HUD, now restored.
- Native source GameHelpListConfig names exported to bottom.json.gz, Function135 gate/icon used. Mount ownership not invented.
- Services NOT connected: social requests/chat sending/assistant execution and mount ownership. Disabled controls and explicit unavailable-service text. This is not a complete issue7 solution.
- Check SOURCE_BOTTOM_NAVIGATION_VALIDATION.json only if present for actual tested scope. Diagnostic script must never write the validation report.

- RELEASE BLOCKED: full physical navigation test failed returning from Chat to Assistant. Direct native Assistant window creation succeeded. Only Friend4-tab clicks and Chat opening passed. Do not ship this as a solved issue.
- Restored the3 active UI runtime files from verified checkpoint21. Unreleased candidate moved to fairy-work/wip-bottom. Keep that candidate separate until navigation and service requirements are resolved. Source assets and configs retained for quick continuation.
