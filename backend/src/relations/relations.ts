export const RELATIONS = {
  MOTHER: {
    key: "MOTHER",
    generation_delta: -1,
    lineage: "direct",
    gender: "female",
    labels: {
      central: "Má",
      north: "Mẹ",
      south: "Má",
    },
  },

  FATHER: {
    key: "FATHER",
    generation_delta: -1,
    lineage: "direct",
    gender: "male",
    labels: {
      central: "Ba",
      north: "Bố",
      south: "Ba",
    },
  },

  uncle_maternal: {
    key: "uncle_maternal",
    generation_delta: -1,
    lineage: "maternal",
    gender: "male",
    labels: {
      central: "Cậu",
      north: "Cậu",
      south: "Cậu",
    },
  },
};
