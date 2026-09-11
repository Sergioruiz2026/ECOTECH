#archivo para definir el contrato general de los repositorios

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from database.database import Database


class RepositorioBase(ABC):
    """Clase base abstracta que define las operaciones CRUD genéricas."""

    def __init__(self, db: Database):
        self.db = db

    @abstractmethod
    def crear(self, entidad: Any) -> Any:
        """Inserta un nuevo registro en la base de datos."""
        pass

    @abstractmethod
    def obtener_por_id(self, id_entidad: int) -> Optional[Any]:
        """Obtiene un registro por su ID único."""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Any]:
        """Obtiene todos los registros de la entidad."""
        pass

    @abstractmethod
    def actualizar(self, entidad: Any) -> bool:
        """Actualiza un registro existente en la base de datos."""
        pass

    @abstractmethod
    def eliminar(self, id_entidad: int) -> bool:
        """Elimina un registro por su ID."""
        pass