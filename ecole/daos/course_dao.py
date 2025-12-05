# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""
from tkinter.font import names

from fontTools.varLib.interpolatableTestContourOrder import test_contour_order

from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional
from typing import List
from models.teacher import Teacher


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué).
        """
        with Dao.connection.cursor() as cursor:
            sql = """
                    INSERT IGNORE INTO course (id_course, name, start_date, end_date)
                    VALUES (%s)
                  """
            cursor.execute(sql, (course.id, course.name, course.start_date, course.end_date))

            Dao.connection.commit()

            if cursor.rowcount > 0:
                return cursor.lastrowid
            else:
                return 0

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoie le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            course = Course(record['name'], record['start_date'], record['end_date'])
            course.id = record['id_course']
        else:
            course = None

        return course

    def read_all(self):
        """ Renvoie tous les cours """

        courses: List[Course] = []
        with Dao.connection.cursor() as cursor:
            sql = """
                    SELECT c.id_course,
                            c.name,
                            c.start_date,
                            c.end_date,
                            c.id_teacher,
                            t.hiring_date,
                            t.id_person,
                            p.first_name,
                            p.last_name,
                            p.age
                    FROM course c 
                    INNER JOIN teacher t 
                    ON c.id_teacher = t.id_teacher
                    INNER JOIN person p
                    ON t.id_person = p.id_person;
                    """
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            teacher = Teacher(
                first_name=record["first_name"],
                last_name=record["last_name"],
                age=record["age"],
                hiring_date=record["hiring_date"]
            )

            course = Course(
                name=record["name"],
                start_date=record["start_date"],
                end_date=record["end_date"],
            )
            course.id_course = record["id_course"]
            course.teacher = teacher
            courses.append(course)
        return courses

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                        UPDATE course
                        SET course_name = %s,
                            start_date = %s,
                            end_date = %s
                        WHERE id_course = %s
                      """
                cursor.execute(sql, (course.name, course.start_date, course.end_date, course.id,))
                Dao.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return False

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                        DELETE FROM course WHERE id_course=%s
                      """
                cursor.execute(sql, (course.id,))
                Dao.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
