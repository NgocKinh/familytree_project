// backend/src/relations/label_engine.js

const LABEL_MAP_VI = {
  SIBLING_FULL: "anh/chị/em ruột",
  SIBLING_SAME_FATHER: "anh/chị/em cùng cha",
  SIBLING_SAME_MOTHER: "anh/chị/em cùng mẹ",
  SIBLING_DIRECT: "anh/chị/em trực hệ",
  SIBLING_COLLATERAL: "anh/chị/em bàng hệ",
  KIN_DIRECT: "bà con trực hệ",
  KIN_COLLATERAL: "bà con bàng hệ",
  UNDETERMINED: "chưa xác định",
  NOT_FOUND: "không tìm ra mối quan hệ",
};

function resolveLabel(result, locale = "vi") {
  if (locale !== "vi") {
    throw new Error("Locale not supported yet");
  }

  return LABEL_MAP_VI[result.relationship] ?? "chưa xác định";
}

module.exports = { resolveLabel };
