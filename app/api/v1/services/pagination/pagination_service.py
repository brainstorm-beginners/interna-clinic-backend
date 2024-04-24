from typing import List, Dict, Any

from fastapi import HTTPException


class Pagination:
    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = page
        self.page_size = page_size

    @property
    def offset(self):
        return (self.page - 1) * self.page_size

    def paginate(self, data: List[Any]) -> Dict[str, Any]:
        if not data:
            raise HTTPException(status_code=404, detail="No items found")

        total = len(data)
        data = data[self.offset : self.offset + self.page_size]

        return {
            "page": self.page,
            "page_size": self.page_size,
            "total": total,
            "total_pages": total // self.page_size if total % self.page_size == 0 else total // self.page_size + 1,
            "data": data,
        }