CREATE OR REPLACE FUNCTION get_family_path(
    p_source_id BIGINT,
    p_target_id BIGINT
)
RETURNS TABLE (
    direction_path TEXT[],
    gender_path TEXT[],
    depth INT
)
LANGUAGE sql
AS $$
WITH RECURSIVE family_path AS (

    -- Anchor
    SELECT
        p.id AS current_id,
        ARRAY[p.id] AS path_ids,
        ARRAY[]::TEXT[] AS direction_path,
        ARRAY[]::TEXT[] AS gender_path,
        0 AS depth
    FROM person p
    WHERE p.id = p_source_id

    UNION ALL

    -- GO UP (child → parent)
    SELECT
        pc.parent_id,
        fp.path_ids || pc.parent_id,
        fp.direction_path || 'UP',
        fp.gender_path || parent.gender,
        fp.depth + 1
    FROM family_path fp
    JOIN parent_child pc
        ON pc.child_id = fp.current_id
    JOIN person parent
        ON parent.id = pc.parent_id
    WHERE NOT pc.parent_id = ANY(fp.path_ids)
      AND fp.depth < 4

    UNION ALL

    -- GO DOWN (parent → child)
    SELECT
        pc.child_id,
        fp.path_ids || pc.child_id,
        fp.direction_path || 'DOWN',
        fp.gender_path || child.gender,
        fp.depth + 1
    FROM family_path fp
    JOIN parent_child pc
        ON pc.parent_id = fp.current_id
    JOIN person child
        ON child.id = pc.child_id
    WHERE NOT pc.child_id = ANY(fp.path_ids)
      AND fp.depth < 4
)

SELECT direction_path, gender_path, depth
FROM family_path
WHERE current_id = p_target_id
ORDER BY depth
LIMIT 1;
$$;
