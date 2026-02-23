// backend/src/relations/engine.test.js

const { inferRelation, AxisState } = require("./engine");

describe("Genealogy Inference Engine (Tầng 1 – Huyết thống)", () => {

  test("SIBLING_DIRECT: cùng cha, mẹ chưa biết", () => {
    const result = inferRelation({
      pathLength: 1,
      fatherAxis: AxisState.SAME,
      motherAxis: AxisState.UNKNOWN,
    });

    expect(result).toEqual({
      relationship: "SIBLING_DIRECT",
      confidence: "MEDIUM",
    });
  });

  test("SIBLING_FULL: anh em ruột", () => {
    const result = inferRelation({
      pathLength: 1,
      fatherAxis: AxisState.SAME,
      motherAxis: AxisState.SAME,
    });

    expect(result).toEqual({
      relationship: "SIBLING_FULL",
      confidence: "HIGH",
    });
  });

  test("SIBLING_COLLATERAL: cùng mẹ, cha chưa biết", () => {
    const result = inferRelation({
      pathLength: 1,
      fatherAxis: AxisState.UNKNOWN,
      motherAxis: AxisState.SAME,
    });

    expect(result).toEqual({
      relationship: "SIBLING_COLLATERAL",
      confidence: "MEDIUM",
    });
  });

  test("UNDETERMINED: không đủ dữ liệu tổ tiên", () => {
    const result = inferRelation({
      pathLength: null,
      fatherAxis: AxisState.UNKNOWN,
      motherAxis: AxisState.UNKNOWN,
    });

    expect(result).toEqual({
      relationship: "UNDETERMINED",
      confidence: "UNKNOWN",
    });
  });

  test("KIN_COLLATERAL: bà con bàng hệ (pathLength >= 2)", () => {
    const result = inferRelation({
      pathLength: 2,
      isDirectLine: false,
    });

    expect(result).toEqual({
      relationship: "KIN_COLLATERAL",
      confidence: "MEDIUM",
    });
  });

});

