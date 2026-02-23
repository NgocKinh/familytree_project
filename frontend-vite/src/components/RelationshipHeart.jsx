const MAP = {
  married: "❤️",
  separated: "💙",
  cohabitation: "💛",
  divorced: "💔",
  widowed: "🖤",
  null: "➕",
};

export default function RelationshipHeart({ status }) {
  const icon = MAP[status ?? "null"];

  return (
    <span
      className="text-6xl select-none"
      title={status ?? "Chưa có quan hệ hôn nhân"}
    >
      {icon}
    </span>
  );
}
