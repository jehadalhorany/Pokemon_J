# Pokémon J · Preview 0.4

Use Node.js 22.13 or later. Start with `npm start`; test with `npm test`. Render build: `npm install`; start: `npm start`; health endpoint: `/health`. Keep root directory blank when uploading this archive's root layout. Render Free SQLite storage is temporary.

## Implemented in this update
- Retained approved animated player art and held-key movement inside a real Three.js 3D world. Plain house/lab/market/gym meshes have roofs, side windows, doors, lighting and shadows. Local bundled Three.js with its MIT license; no runtime CDN.
- Home, Lab, Market and Gym have cutaway 3D interiors, furniture and collision. Chibi NPC meshes have visible proximity actions and clickable interaction. Gym challenge requires entering and talking to the leader.
- Professor conversation offers an escort to the three closed starter balls. Inspection never grants a Pokémon. The separate Choose button selects a level-5 Bulbasaur, Charmander or Squirtle; Back/Close cancels inspection. Choosing a generation is deferred.
- Top-right minimap with player marker, expandable map, destination details and Back without movement. Two playable destinations only: Pallet Town and Viridian Forest; the first badge unlocks the forest. Server validates travel gates and rejects travel during battles. Free spin transition, or flight if a Flying-type partner knows Fly. Professor teaches Fly after the first badge.
- Water traversal uses a stylized 3D Water mount. Outdoor camera follows the player; interior camera stays steady. Trees sway lightly.
- Button-based Pokédex with search, Generation 1–9 filtering, individual species/forms, base stats, type defenses, evolution conditions, compatible moves, abilities and source encounter locations.
- All 1025 base species have supplemental learnsets. Catalog has 1261 entries; 1186 entries/forms have matched supplemental learnsets. Unmatched forms report unavailable data.
- Every owned/wild copy has persistent IVs, personality ID, nature, gender, characteristic, EVs and six calculated stats. Capture keeps the wild IVs/personality and reduces its level only when above player level.
- Training vitamins, EV-reducing berries, Rare Candy, evolution stones and Poké Balls in the Market. Coins/gems prices and custom rarity/star/shiny bonuses are provisional game balance values, not official reference data. Training previews actual EV/stat changes. Limits: 252 EV per stat, 510 total. Rare Candy respects player level.
- Four equipped moves. Relearn eligible level-up moves free; compatible historical tutor/TM moves cost 200 coins. Certain special tutor moves require maximum friendship.
- Battle priority, speed, physical/special stats, accuracy, core stat stages, basic ailments, PP, switching and capture. Sleep/paralysis that prevent action do not consume PP. Struggle is available if PP runs out. Auto persists until manually disabled.
- Level, simple friendship and stone evolutions retain the original UID, IVs, EVs and lock. Regional stone branches respect the current Kanto region. Item evolution asks for confirmation. Other complex evolution conditions are reference-only.
- Route 1 and forest use different real encounter pools with separately configured fixed game levels. Images for the starters and seven active wild species are bundled.
- Normal water access requires a Water-type partner with learned Swim. Professor teaches Swim after the first badge. Water test is a prototype visual bypass, not owner account authorization.

## Reference data and limitations
User-supplied Pokémon Database HTML and type chart supply catalog, generations, evolution conditions, moves, tutor offerings and location names. PokeAPI CSVs supplement learnsets, abilities, nature modifiers and original per-version encounters. Definitions include the 934 uploaded moves plus 3 supplemental moves. 627 locations have supplemental encounter tables; 813 locations are in the uploaded regional name index. These are references, not fully built playable maps. Some bespoke move mechanics and abilities remain incomplete. Other Pokédex artwork depends on external image links.

Google sign-in, Jehad-only owner privileges, complete maps/bosses, multiplayer, guilds, events, subscriptions and the full game economy are not implemented. Current progression has provisional daily limits and minimum account-age gates (90 days subscribed / 150 days free). No payment or subscription activation is wired.

## Updating the same version
Keep archive name `Pokemon_J_Visual_v04.zip`. Extract into the existing project folder and accept file replacement. Upload the resulting `public`, `server`, `scripts` folders and root package.json to GitHub, commit, and deploy the latest commit on Render. Refresh with Ctrl+F5. The archive excludes SQLite saves. No external deployment was performed by the assistant.

## Validation
24 rules/progression/battle tests pass. API tests cover references, purchases, training, saved IVs, move PP and distinct route encounters. UI/canvas integration with the real API covers copy stats, item previews, tutor compatibility, generation filtering, Pokémon move/location details and battle controls. Real headless Chromium/WebGL checks cover rendered home/town/lab/gym/forest, professor escort, preview/cancel/level-5 starter selection, map Back, locked/open server travel, Swim restrictions and traversal, Fly restriction and a 390-pixel mobile layout. Rendered desktop/mobile scenes were visually reviewed. Browser tests use local fixtures, not player saves.

Import scripts are offline data-preparation tools. The evolution/location/game-data imports require Python lxml and their saved inputs. Hosting does not require Python.
