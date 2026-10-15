import fs from 'node:fs';
import {gunzipSync} from 'node:zlib';
const rows=JSON.parse(gunzipSync(fs.readFileSync(new URL('../public/data/original/configs/SelectEudemonConfig.json.gz',import.meta.url))));
const dex=JSON.parse(fs.readFileSync(new URL('../public/data/pokedex.json',import.meta.url))).entries;
export const starterGenerations=rows.map(r=>({id:r.Id,name:r.Name,icon:r.Icon,partners:r.eudemons.map(id=>{const p=dex.find(p=>p.originalId===id);if(!p)throw Error('Missing original starter '+id);return {id:p.id,originalId:id,name:p.name,imageUrl:p.imageUrl};})}));
export function validateStarter(generation,species){const row=starterGenerations.find(r=>r.id===Number(generation));if(!row||!row.partners.some(p=>p.id===species))throw Error('Choose a partner from the selected generation');return row;}
