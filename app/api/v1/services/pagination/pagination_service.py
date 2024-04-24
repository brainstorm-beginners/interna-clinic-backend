from typing import List, Any


class Pagination:
    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = page
        self.page_size = page_size

    @property
    def offset(self):
        return (self.page - 1) * self.page_size

    def paginate(self, total: int, data: List[Any]) -> dict[str, int | list[Any]]:
        if not data:
            return {
                "page": self.page,
                "page_size": self.page_size,
                "total": 0,
                "total_pages": 1,
                "data": [],
            }

        return {
            "page": self.page,
            "page_size": self.page_size,
            "total": total,
            "total_pages": total // self.page_size if total % self.page_size == 0 else total // self.page_size + 1,
            "data": data,
        }
