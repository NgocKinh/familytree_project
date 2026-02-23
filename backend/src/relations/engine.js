// backend/src/relations/engine.js

const {
  AxisState,
  inferSibling,
  inferKin,
} = require("./inference_rules");

/**
 * Infer relationship (TẦNG 1 – HUYẾT THỐNG)
 *
 * @param {Object} input
 * @param {number|null} input.pathLength
 * @param {"SAME"|"DIFFERENT"|"UNKNOWN"} input.fatherAxis
 * @param {"SAME"|"DIFFERENT"|"UNKNOWN"} input.motherAxis
 * @param {boolean} input.isDirectLine   // dùng khi pathLength >= 2
 */
function inferRelation(input) {
  const { pathLength, fatherAxis, motherAxis, isDirectLine } = input;

  // Không đủ dữ liệu tổ tiên
  if (pathLength === null || pathLength === undefined) {
    return {
      relationship: "UNDETERMINED",
      confidence: "UNKNOWN",
    };
  }

  // Anh em (pathLength = 1)
  if (pathLength === 1) {
    return inferSibling(fatherAxis, motherAxis);
  }

  // Bà con (pathLength >= 2)
  return inferKin(!!isDirectLine);
}

module.exports = { inferRelation, AxisState };
