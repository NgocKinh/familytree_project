// backend/src/relations/label_rules.js

const LABEL_RULES = [
  {
    generation: 1,
    role: "ancestor",
    gender: "female",
    label: "mẹ",
  },
  {
    generation: 1,
    role: "ancestor",
    gender: "male",
    label: "cha",
  },
  {
    generation: 2,
    role: "ancestor",
    gender: "male",
    side: "PATERNAL",
    label: "ông nội",
  },
  {
    generation: 2,
    role: "ancestor",
    gender: "male",
    side: "MATERNAL",
    label: "ông ngoại",
  },
  {
    generation: 2,
    role: "ancestor",
    gender: "other",
    label: "ông/bà",
  },
];

module.exports = { LABEL_RULES };
