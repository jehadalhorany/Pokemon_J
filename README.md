# Pokémon J — prototype 0.1
Run with Node 22.13+ (recommended Node 24): `npm start`, open http://localhost:3000. Run rules checks: `npm test`.
This is a playable vertical slice, not the full game. Original temporary geometric graphics. Three starters, keyboard/touch movement, two wild zones, one fixed level-8 boss, badges, server-side battle/capture, six-member team and excess storage, release, stars, energy, SQLite saves, auto mode.
No Google sign-in, verified owner account, payments, multiplayer, guild, events, awakening, shiny, or full maps yet. Cookie identifies a guest save. Not suitable for a public launch. Demo gems are granted for testing. Starter names are reference placeholders.
Temporary choices: 100 energy per refill, capture ball costs 100 coins, SSR stars 3–6 cost 50/100/175/250, early prototype level cap 13. These are not final approved balance values. Battle currently uses simple physical formulas; status effects, priority moves, and full type table remain for later work. Auto runs while the page is open. Captures and battle health restore after each encounter.
Render: create Node web service, build `npm install`, start `npm start`, attach a persistent disk at `/var/data` and set DATA_DIR=/var/data. PORT is supplied by Render. Without persistent storage saves may be lost. Database is single-instance only. No owner credentials are embedded.
Next: approve art direction, full type/stat/priority engine, inventory capture balls, complete training/evolution/stars/awakening, owner Google authentication, daily progression, map gates, server identity and multiplayer.

## Pokédex import
`public/data/pokedex.json` contains 1025 National Pokédex species, 1261 entries including alternate forms, English names, dual types, base stats, source links and external AVIF icon links extracted from the supplied PokemonDB HTML. It is available at `/data/pokedex.json`. Image bytes, moves, rarity, evolution and spawn tables are not included. Importing the catalog does not enable every species as a starter or make it spawn everywhere. Existing trial battles and graphics are unchanged.
Rebuild using `python3 scripts/import-pokedex.py /path/to/saved.html`.
