import AssignParentForm from "../components/clean/AssignParentForm";

export default function FamilySetupPage() {
  return (
    <div className="max-w-6xl mx-auto p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold text-center text-green-600 mb-4">
        🧠 Thiết lập Quan hệ Gia đình
      </h2>

      <AssignParentForm />
    </div>
  );
}
