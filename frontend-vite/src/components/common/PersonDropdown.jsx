import React from "react";

export default function PersonDropdown({
    label,
    value,
    onChange,
    persons = [],
    placeholder = "-- Chọn --",
    filterFn = null,
    disabled = false,
}) {
    const list = filterFn ? persons.filter(filterFn) : persons;

    const sortedPersons = [...list].sort((a, b) => {
    const nameA = (a.full_name_vn || "").toString();
    const nameB = (b.full_name_vn || "").toString();

    if (!a.birth_date && !b.birth_date) {
        return nameA.localeCompare(nameB, "vi");
    }

    if (!a.birth_date) return 1;
    if (!b.birth_date) return -1;

    if (a.birth_date !== b.birth_date) {
        return new Date(b.birth_date) - new Date(a.birth_date);
    }

    return nameA.localeCompare(nameB, "vi");
});

    return (
        <div>
            {label && (
                <label className="block font-medium text-gray-700 mb-1">
                    {label}
                </label>
            )}

            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                disabled={disabled}
                className="w-full border rounded-lg p-2"
            >
                <option value="">{placeholder}</option>

                {sortedPersons.map((p) => {
                    const birthYear = p.birth_date
                        ? new Date(p.birth_date).getFullYear()
                        : "";

                    const genderLabel =
                        p.gender === "male"
                            ? "Nam"
                            : p.gender === "female"
                                ? "Nữ"
                                : "Khác";

                    const display =
                        `${p.full_name_vn || ""} — ${genderLabel} (${birthYear})`;

                    return (
                        <option
                            key={`${p.person_id}-${p.full_name_vn || "noname"}`}
                            value={p.person_id}
                        >
                            {display}
                        </option>
                    );
                })}
            </select>
        </div>
    );
}