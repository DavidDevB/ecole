# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""

from models.student import Student
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional
from typing import List


@dataclass
class StudentDao(Dao[Student]):
    def create(self, student: Student) -> int:
        """Crée en BD l'entité Student correspondant au cours student

        :param student: à créer sous forme d'entité Student en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué).
        """
        with Dao.connection.cursor() as cursor:
            sql = f"INSERT IGNORE INTO student (student_nbr) VALUES (%s)"
            cursor.execute(sql, (student.student_nbr,))

            Dao.connection.commit()

            if cursor.rowcount > 0:
                return cursor.lastrowid
            else:
                return 0


    def read(self, id_student: int) -> Optional[Student]:
        """Renvoie le cours correspondant à l'entité dont l'id est id_student
           (ou None s'il n'a pu être trouvé)"""
        student: Optional[Student]

        with Dao.connection.cursor() as cursor:
            sql = """
                    SELECT s.*, p.* 
                    FROM student s INNER JOIN person p ON s.id_person = p.id_person
                    WHERE id_student=%s
                  """
            cursor.execute(sql, (id_student,))
            record = cursor.fetchone()
        if record is not None:
            student = Student(record['student_nbr'])
            student.id = record['student_nbr']
        else:
            student = None

        return student

    def read_all(self):
        """ Renvoie tous les étudiants """

        students: List[Student] = []
        with Dao.connection.cursor() as cursor:
            sql = """
                    SELECT s.*, p.* 
                    FROM student s INNER JOIN person p ON s.id_person = p.id_person
                  """
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            student = Student(record["student_nbr"])
            student.id = record["student_nbr"]
            students.append(student)
        return students


    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité Student correspondant à student, pour y correspondre

        :param student: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, student: Student) -> bool:
        """Supprime en BD l'entité Student correspondant à student

        :param student: cours dont l'entité Student correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
