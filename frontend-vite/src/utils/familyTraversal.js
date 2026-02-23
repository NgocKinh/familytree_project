/**
 * Lấy toàn bộ con + cháu + chắt của một người
 * dùng để chặn vòng lặp gia phả
 */
export function getDescendants(personId, people) {
  const result = new Set()

  function dfs(id) {
    people.forEach(p => {
      if (p.fatherId === id || p.motherId === id) {
        if (!result.has(p.id)) {
          result.add(p.id)
          dfs(p.id)
        }
      }
    })
  }

  dfs(personId)
  return Array.from(result)
}
