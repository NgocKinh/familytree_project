"""
DEPRECATED MODULE

File này được giữ lại để:
- Không làm vỡ các import cũ trong backend/api
- Đóng vai trò BRIDGE sang core

⚠️ KHÔNG thêm logic mới vào đây
⚠️ KHÔNG sửa thuật toán trong file này

Toàn bộ logic PATH đã được chuyển sang:
    backend/core/relation_path_utils.py
"""

from core.relation_path_utils import *
