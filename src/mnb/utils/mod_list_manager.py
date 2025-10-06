import json
from typing import List, Dict, Any

class ModListManager:
    """Manages a list of mods/files for export/import and batch opening."""

    def __init__(self):
        self._mod_list: List[Dict[str, Any]] = []

    def add_mod(self, game_domain: str, mod_id: int, file_id: int, file_name: str):
        mod_info = {
            "game_domain": game_domain,
            "mod_id": mod_id,
            "file_id": file_id,
            "file_name": file_name
        }
        # Prevent duplicates based on mod_id and file_id
        if not any(m["mod_id"] == mod_id and m["file_id"] == file_id for m in self._mod_list):
            self._mod_list.append(mod_info)

    def remove_mod(self, mod_id: int, file_id: int):
        self._mod_list = [m for m in self._mod_list if not (m["mod_id"] == mod_id and m["file_id"] == file_id)]

    def update_mod_name(self, mod_id: int, file_id: int, new_name: str):
        for mod_info in self._mod_list:
            if mod_info["mod_id"] == mod_id and mod_info["file_id"] == file_id:
                mod_info["file_name"] = new_name
                break

    def clear_list(self):
        self._mod_list.clear()

    def get_mod_list(self) -> List[Dict[str, Any]]:
        return self._mod_list

    def export_to_file(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self._mod_list, f, ensure_ascii=False, indent=4)

    def import_from_file(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            self._mod_list = json.load(f)

    def __len__(self):
        return len(self._mod_list)

    def __str__(self):
        return json.dumps(self._mod_list, indent=4, ensure_ascii=False)
