// Display names come only from the original portal NPC and destination area records.
export function sourceBuildingName(portal,areas){const destination=areas.get(portal?.target?.area);if(destination?.Type!==2)return '';return portal.config?.name||destination.name||'';}
