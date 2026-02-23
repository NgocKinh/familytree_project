import { useEffect, useMemo, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getFamilyTree } from "../api/treeApi";
import { formatName } from "../utils/formatName";
import {
  getAvatarURL,
  fallbackAvatar,
  handleAvatarError,
} from "../utils/avatarEngine";

// --------------------------------------------------
// Helpers
// --------------------------------------------------

const sortByBirthYearAsc = (list = []) =>
  list
    .slice()
    .sort((a, b) => {
      const ay = Number(a?.birth_year) || 9999;
      const by = Number(b?.birth_year) || 9999;
      return ay - by;
    });

const heartIcon = (status) => {
  switch (status) {
    case "married":
      return "❤️";
    case "cohabitation":
      return "💛";
    case "separated":
      return "💚";
    case "divorced":
      return "💔";
    case "widowed":
      return "🖤";
    default:
      return "➕";
  }
};

function Avatar({ person, size = 80, onClick }) {
  const src = useMemo(() => {
    if (!person) return fallbackAvatar();
    return person.id
      ? getAvatarURL(person.id, person.gender)
      : fallbackAvatar(person.gender);
  }, [person]);

  if (!person) return null;

  const onError = (e) => {
    handleAvatarError(e, person?.id, person?.gender);
  };

  return (
    <img
      src={src}
      onError={onError}
      className="rounded-full shadow-md cursor-pointer bg-white"
      style={{ width: size, height: size, objectFit: "cover" }}
      onClick={onClick}
      alt=""
    />
  );
}

// --------------------------------------------------
// Page
// --------------------------------------------------
export default function TreePage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [tree, setTree] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;

    (async () => {
      setLoading(true);
      try {
        const data = await getFamilyTree(id);
        if (!alive) return;
        setTree(data);
      } catch (err) {
        console.error("Failed to load tree:", err);
        if (alive) setTree({ error: true });
      } finally {
        if (alive) setLoading(false);
      }
    })();

    return () => {
      alive = false;
    };
  }, [id]);

  const go = (pid) => {
    if (!pid) return;
    navigate(`/tree/${pid}`);
  };

  const renderPerson = (person, size = 80) => {
    if (!person) return null;

  let displayName = 'Không rõ';

  if (person.name && person.name !== '?') {
    displayName = person.name;
  } else if (person.full_name) {
    displayName = person.full_name;
  } else {
    const fn = formatName(person, 'full');
    if (fn && fn !== '?') displayName = fn;
  }

  return (
    <div
      key={person.id || displayName}
      className="flex flex-col items-center w-[220px] select-none"
    >
      <Avatar
        person={person}
        size={size}
        onClick={
          person?.isFake ? undefined : () => go(person.id)
        }
      />

      <p className="mt-2 font-medium text-center w-full whitespace-normal">
        {displayName}
      </p>

      <p className="text-sm text-gray-500 text-center">
        {person.birth_year ?? '?'} – {person.death_year ?? ''}
      </p>
    </div>
  );
};

const renderChild = (child) => {
  if (!child) return null;

  const genderIcon =
    child.gender === "male"
      ? "👦"
      : child.gender === "female"
      ? "👧"
      : "🧑";

  const displayName = formatName(child, "full");

  return (
    <div
      key={child.id || displayName}
      className="flex flex-col items-center w-[140px] select-none"
    >
      <Avatar person={child} size={80} onClick={() => go(child.id)} />

      <div className="flex items-center gap-1 mt-2 font-medium text-sm text-center">
        <span>{genderIcon}</span>
        <span>{displayName}</span>
      </div>

      <p className="text-sm text-gray-500 mt-1">
        {child.birth_year ?? "?"} – {child.death_year ?? ""}
      </p>
    </div>
  );
};

const getDisplayCouple = (center, spouse) => {
  // không có center thì thôi
  if (!center) return null;

  const gender = center.gender || "other";

  const hasRealSpouse = !!spouse;

  // tạo spouse giả nếu cần
  const fakeSpouse = {
    id: null,
    gender: "other",
    name: "",
    isFake: true,
  };

  const displaySpouse = hasRealSpouse ? spouse : fakeSpouse;

  // quy ước vị trí
  // male + other => coi như chồng (bên trái)
  // female => vợ (bên phải)
  if (gender === "female") {
    return {
      left: displaySpouse,
      right: center,
    };
  }

  // male hoặc other
  return {
    left: center,
    right: displaySpouse,
  };
};

  if (loading) return <p className="p-5 text-center">Đang tải dữ liệu…</p>;
  // FIX CỨNG: nếu tree không hợp lệ thì dừng toàn bộ
if (!tree) {
  return null;
}

  const {
    center,
    spouse,
    marriage_status,
    father_parents = [],
    mother_parents = [],
    children_common = [],
    children_father_separate = [],
    children_mother_separate = [],
  } = tree;
// FIX 2 – chuẩn hóa hôn nhân & giới tính
const normalizedGender =
  center?.gender === "female" ? "female" : "male";

const hasMarriage =
  marriage_status &&
  marriage_status !== "unknown" &&
  marriage_status !== "single";

const fakeSpouse = {
  id: null,
  name: "",
  gender: "other",
  isFake: true,
};

  const displaySpouse =
  hasMarriage && spouse ? spouse : fakeSpouse;

// FIX 2.3 – gán left / right
let leftPerson = null;
let rightPerson = null;

if (normalizedGender === "female") {
  leftPerson = displaySpouse;
  rightPerson = center;
} else {
  // male + other
  leftPerson = center;
  rightPerson = displaySpouse;
}

return (

    <div className="w-full flex flex-col items-center py-10 select-none">
      <div className="flex justify-between w-full px-32">
        <div className="flex flex-col items-center w-1/2">
          <p className="text-blue-700 font-medium mb-3 text-lg">
            Cha mẹ bên Nam
          </p>
          <div className="flex gap-10">
            {father_parents.map((p) => renderPerson(p))}
          </div>
        </div>

        <div className="flex flex-col items-center w-1/2">
          <p className="text-pink-700 font-medium mb-3 text-lg">
            Cha mẹ bên Nữ
          </p>
          <div className="flex gap-10">
            {mother_parents.map((p) => renderPerson(p))}
          </div>
        </div>
      </div>

      <div className="flex items-center justify-center mt-14 gap-20">
        {renderPerson(leftPerson, 140)}
        <div className="text-6xl">{heartIcon(marriage_status)}</div>
        {renderPerson(rightPerson, 140)}
      </div>

      {children_common.length > 0 && (
        <>
          <h3 className="mt-16 text-lg font-semibold">Con chung</h3>
          <div className="flex flex-wrap justify-center gap-10 mt-8">
            {sortByBirthYearAsc(children_common)
              .map((c) => renderChild(c))}

          </div>
        </>
      )}

      {(children_father_separate.length > 0 ||
        children_mother_separate.length > 0) && (
        <>
          <h3 className="mt-16 text-xl font-semibold">Con riêng</h3>

          <div className="relative w-full mt-10">
            {/* ĐƯỜNG KẺ CHÍNH GIỮA – LUÔN HIỆN */}
            <div className="absolute left-1/2 top-0 bottom-0 w-px bg-gray-300" />

            <div className="flex w-full">
              {/* CON RIÊNG CỦA CHỒNG */}
              <div className="flex flex-col items-center w-1/2 px-10 min-h-[150px]">
                <p className="text-gray-700 mb-4 text-lg">
                  Con riêng của Chồng
                </p>
                <div className="flex flex-wrap justify-center gap-10">
                  {sortByBirthYearAsc(children_father_separate)
                    .map((c) => renderChild(c))}
                </div>
              </div>

              {/* CON RIÊNG CỦA VỢ */}
              <div className="flex flex-col items-center w-1/2 px-10 min-h-[150px]">
                <p className="text-gray-700 mb-4 text-lg">
                  Con riêng của Vợ
                </p>
                <div className="flex flex-wrap justify-center gap-10">
                  {sortByBirthYearAsc(children_mother_separate)
                    .map((c) => renderChild(c))}
                </div>
              </div>
            </div>
          </div>
        </>
      )}

    </div>
  );
}
