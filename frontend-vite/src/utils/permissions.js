export function hasKey(userKeys, key) {
  if (!Array.isArray(userKeys)) return false;
  return userKeys.includes("ALL_KEYS") || userKeys.includes(key);
}
