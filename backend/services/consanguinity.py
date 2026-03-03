def are_related(conn, id1: int, id2: int) -> bool:

    if id1 == id2:
        return True

    query = """
    WITH RECURSIVE ancestors_1 AS (
        SELECT parent_id
        FROM parent_child
        WHERE child_id = %s

        UNION ALL

        SELECT pc.parent_id
        FROM parent_child pc
        JOIN ancestors_1 a ON pc.child_id = a.parent_id
    ),
    ancestors_2 AS (
        SELECT parent_id
        FROM parent_child
        WHERE child_id = %s

        UNION ALL

        SELECT pc.parent_id
        FROM parent_child pc
        JOIN ancestors_2 a ON pc.child_id = a.parent_id
    )

    SELECT 1
    FROM ancestors_1 a1
    JOIN ancestors_2 a2
        ON a1.parent_id = a2.parent_id

    UNION

    SELECT 1
    FROM parent_child
    WHERE (parent_id = %s AND child_id = %s)
       OR (parent_id = %s AND child_id = %s)

    LIMIT 1;
    """

    cur = conn.cursor()
    cur.execute(query, (id1, id2, id1, id2, id2, id1))
    result = cur.fetchone()

    return result is not None