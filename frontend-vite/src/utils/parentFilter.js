import { getDescendants } from './familyTraversal'

/**
 * Trả về danh sách người hợp lệ để làm cha / mẹ
 * @param {Object} child - người đang chọn cha/mẹ
 * @param {Array} people - toàn bộ danh sách người
 * @param {'male' | 'female'} gender - giới tính cha/mẹ
 */
export function getValidParents(child, people, gender) {
  const descendants = getDescendants(child.id, people)

  return people.filter(p =>
    p.gender === gender &&                 // đúng giới tính
    p.id !== child.id &&                   // không phải chính nó
    !descendants.includes(p.id) &&         // không phải con/cháu
    (p.generation ?? 0) < (child.generation ?? 0) // lớn hơn 1 thế hệ
  )
}
