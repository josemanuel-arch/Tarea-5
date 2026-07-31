"""Estado persistente para no repetir alertas.

Guarda, por producto, el último estado conocido ('in' / 'out'). Así solo
avisamos cuando algo pasa de agotado (o desconocido) a disponible, no en
cada revisión mientras siga en stock.
"""

import json
import os
import tempfile


class Store:
    def __init__(self, path):
        self.path = path
        self._data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as fh:
                    self._data = json.load(fh)
            except (json.JSONDecodeError, OSError):
                self._data = {}

    def _save(self):
        # Escritura atómica: primero a un archivo temporal, luego reemplaza.
        directory = os.path.dirname(os.path.abspath(self.path)) or "."
        fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(self._data, fh, ensure_ascii=False, indent=2)
            os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

    def get_state(self, key):
        entry = self._data.get(key)
        return entry.get("state") if entry else None

    def set_state(self, key, state):
        self._data[key] = {"state": state}
        self._save()
