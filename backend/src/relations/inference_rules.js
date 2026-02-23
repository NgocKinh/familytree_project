// backend/src/relations/inference_rules.js

/**
 * AxisState:
 *  - SAME: xác định và trùng
 *  - DIFFERENT: xác định và khác
 *  - UNKNOWN: null / chưa biết
 */
const AxisState = {
  SAME: "SAME",
  DIFFERENT: "DIFFERENT",
  UNKNOWN: "UNKNOWN",
};

/**
 * RelationshipType:
 *  - chỉ dành cho tầng 1 huyết thống
 */
const RelationshipType = {
  SIBLING_FULL: "SIBLING_FULL",
  SIBLING_SAME_FATHER: "SIBLING_SAME_FATHER",
  SIBLING_SAME_MOTHER: "SIBLING_SAME_MOTHER",
  SIBLING_DIRECT: "SIBLING_DIRECT",
  SIBLING_COLLATERAL: "SIBLING_COLLATERAL",
  KIN_DIRECT: "KIN_DIRECT",
  KIN_COLLATERAL: "KIN_COLLATERAL",
  UNDETERMINED: "UNDETERMINED",
  NOT_FOUND: "NOT_FOUND",
};

/**
 * InferenceConfidence:
 *  - độ tin cậy suy luận
 */
const InferenceConfidence = {
  HIGH: "HIGH",
  MEDIUM: "MEDIUM",
  LOW: "LOW",
  UNKNOWN: "UNKNOWN",
};

/**
 * Sibling inference
 * pathLength MUST = 1
 */
function inferSibling(fatherAxis, motherAxis) {
  // anh em ruột
  if (
    fatherAxis === AxisState.SAME &&
    motherAxis === AxisState.SAME
  ) {
    return {
      relationship: RelationshipType.SIBLING_FULL,
      confidence: InferenceConfidence.HIGH,
    };
  }

  // cùng cha khác mẹ
  if (
    fatherAxis === AxisState.SAME &&
    motherAxis === AxisState.DIFFERENT
  ) {
    return {
      relationship: RelationshipType.SIBLING_SAME_FATHER,
      confidence: InferenceConfidence.HIGH,
    };
  }

  // cùng mẹ khác cha
  if (
    fatherAxis === AxisState.DIFFERENT &&
    motherAxis === AxisState.SAME
  ) {
    return {
      relationship: RelationshipType.SIBLING_SAME_MOTHER,
      confidence: InferenceConfidence.HIGH,
    };
  }

  // cùng cha, mẹ chưa biết
  if (
    fatherAxis === AxisState.SAME &&
    motherAxis === AxisState.UNKNOWN
  ) {
    return {
      relationship: RelationshipType.SIBLING_DIRECT,
      confidence: InferenceConfidence.MEDIUM,
    };
  }

  // cùng mẹ, cha chưa biết
  if (
    fatherAxis === AxisState.UNKNOWN &&
    motherAxis === AxisState.SAME
  ) {
    return {
      relationship: RelationshipType.SIBLING_COLLATERAL,
      confidence: InferenceConfidence.MEDIUM,
    };
  }

  // cả cha và mẹ đều chưa biết
  if (
    fatherAxis === AxisState.UNKNOWN &&
    motherAxis === AxisState.UNKNOWN
  ) {
    return {
      relationship: RelationshipType.UNDETERMINED,
      confidence: InferenceConfidence.UNKNOWN,
    };
  }

  // xác định khác cả cha lẫn mẹ
  return {
    relationship: RelationshipType.NOT_FOUND,
    confidence: InferenceConfidence.LOW,
  };
}

/**
 * Kin inference
 * pathLength MUST >= 2
 *
 * @param {boolean} isDirectLine
 *   true  -> trục hệ (lineal)
 *   false -> bàng hệ (collateral)
 */
function inferKin(isDirectLine) {
  return {
    relationship: isDirectLine
      ? RelationshipType.KIN_DIRECT
      : RelationshipType.KIN_COLLATERAL,
    confidence: InferenceConfidence.MEDIUM,
  };
}

module.exports = {
  AxisState,
  RelationshipType,
  InferenceConfidence,
  inferSibling,
  inferKin,
};
