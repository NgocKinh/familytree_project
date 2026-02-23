// ======================================================
// ParentDropdown.jsx
// CV3.4 – FINAL
// Rule:
// - Chọn Child trước
// - Cha/Mẹ = generation - 1
// - Đúng giới tính
// - Khóa dropdown sau khi chọn
// ======================================================

export default function ParentDropdown({
  child,
  people,
  gender,
  selectedParentId,
  onSelect
}) {
  if (!child || !people?.length) return null;

  const options = people.filter((p) => {
    if (!p.gender || typeof p.generation !== "number") return false;
    if (p.gender !== gender) return false;
    if (p.generation !== child.generation - 1) return false;
    if (p.id === child.id) return false;
    return true;
  });

  return (
    <select
      value={selectedParentId || ""}
      disabled={options.length === 0 || !!selectedParentId}
      onChange={(e) => onSelect(e.target.value)}
      className="border p-2 rounded"
    >
      <option value="">
        {options.length === 0
          ? `Không có ${gender === "male" ? "Cha" : "Mẹ"} hợp lệ`
          : `-- Chọn ${gender === "male" ? "Cha" : "Mẹ"} --`}
      </option>

      {options.map((p) => (
        <option key={p.id} value={p.id}>
          {p.id} - {p.sur_name} {p.first_name}
        </option>
      ))}
    </select>
  );
}


