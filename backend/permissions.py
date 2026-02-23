ROLE_KEYS = {
    "viewer": [
        "person:list",
        "person:view_basic",
        "tree:view",
        "family:view_nuclear"
    ],
    "member_basic": [
        "person:list",
        "person:view_basic",
        "tree:view",
        "family:view_nuclear",
        "person:create",
        "person:edit_basic",
        "relation:find_summary"
    ],
    "member_close": [
        "person:list",
        "person:view_basic",
        "person:view_detail_near",
        "tree:view",
        "family:view_nuclear",
        "person:create",
        "person:edit_basic",
        "person:edit_detail_near",
        "person:link_near",
        "relation:create_near",
        "relation:edit_near",
        "relation:find_path_near"
    ],
    "co_operator": [
        "person:list",
        "person:view_full",
        "tree:view",
        "person:create",
        "person:edit_basic",
        "person:edit_detail",
        "person:link",
        "person:verify",
        "relation:create",
        "relation:edit",
        "relation:find_full"
    ],
    "admin": ["ALL_KEYS"]
}
