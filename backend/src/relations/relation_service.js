// backend/src/relations/relation_service.js

const { inferRelation } = require("./engine");
const { resolveLabel } = require("./label_engine");

function getRelation(input, locale = "vi") {
  const inference = inferRelation(input);
  const label = resolveLabel(inference, locale);

  return {
    ...inference,
    label,
  };
}

module.exports = { getRelation };
