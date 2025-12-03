# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""

from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional
from typing import List


@dataclass
class TeacherDao(Dao[Teacher]):
    def create(self, teacher: Teacher) -> int:
        """Crée en BD l'entité Teacher correspondant au cours teacher

        :param teacher: à créer sous forme d'entité Teacher en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué).
        """
        ...
        return 0

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Renvoie le cours correspondant à l'entité dont l'id est id_teacher
           (ou None s'il n'a pu être trouvé)"""
        teacher: Optional[Teacher]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM teacher WHERE id_teacher=%s"
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()
        if record is not None:
            teacher = Teacher(record['hiring_date'])
            teacher.id = record['id_teacher']
        else:
            teacher = None

        return teacher

    def read_all(self):
        """ Renvoie tous les enseignants """

        teachers: List[Teacher] = []
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM teacher"
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            teacher = Teacher(hiring_date=record["hiring_date"])
            teacher.id = record["id_teacher"]
            teachers.append(teacher)
        return teachers

    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité Teacher correspondant à teacher, pour y correspondre

        :param teacher: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher

        :param teacher: cours dont l'entité Teacher correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
