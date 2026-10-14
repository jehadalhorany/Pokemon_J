# Pokémon J · Version 0.4 work status

Work resumed at the user's request after the saved pause checkpoint.
Current source, assets and data are included in the archive. 24 unit tests and API/UI integration checks pass.

Resume review completed:
- PP is consumed only when a move is executed, including misses; sleep/full paralysis/flinch preventing action preserve PP.
- Stone evolution parses linked-text spacing and regional conditions. Pikachu evolves to ordinary Raichu in Kanto; Alolan evolution is gated by its region.
- Item evolution confirmation and Rare Candy player-level caps are checked.

See README.md for the implemented features and explicit remaining scope. This archive is the current version 0.4, not an external deployment. Keep the same filename and root layout for replacement updates.
