// Person
export type Person = {
  id: number
  name: string
  gender: 'M' | 'F'
  birthYear?: number
  deathYear?: number
}

// Marriage
export type Marriage = {
  id: number
  husbandId?: number
  wifeId?: number
  status: 'married' | 'divorced' | 'widowed' | 'separated' | 'cohabitation'
}

// Child (gắn với marriage)
export type Child = {
  marriageId: number
  childId: number
  type: 'blood' | 'adopted'
}

// TreeNode dùng cho UI
export type TreeNode = {
  person: Person
  marriage?: Marriage
  spouse?: Person
  children: TreeNode[]
}
