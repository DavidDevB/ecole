# -*- coding: utf-8 -*-

"""
Classe Dao[Address]
"""

from models.address import Address
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional
from typing import List


@dataclass
class AddressDao(Dao[Address]):
    def create(self, address: Address) -> int:
        """Crée en BD l'entité Address correspondant au cours address

        :param address: à créer sous forme d'entité Address en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué).
        """
        with Dao.connection.cursor() as cursor:
            sql = f"INSERT IGNORE INTO address (id_address, street, city, postal_code) VALUES (%s)"
            cursor.execute(sql, (address.id, address.street, address.street, address.postal_code))

            Dao.connection.commit()

            if cursor.rowcount > 0:
                return cursor.lastrowid
            else:
                return 0

    def read(self, id_address: int) -> Optional[Address]:
        """Renvoie l'adresse correspondante à l'entité dont l'id est id_address
           (ou None s'il n'a pu être trouvé)"""
        address: Optional[Address]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address WHERE id_address=%s"
            cursor.execute(sql, (id_address,))
            record = cursor.fetchone()
        if record is not None:
            address = Address(record['street'], record['city'], record['postal_code'])
            address.id = record['id_address']
        else:
            address = None

        return address

    def read_all(self):
        """ Renvoie tous les cours """

        addresses: List[Address] = []
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address"
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            address = Address(
                street=record["street"],
                city=record["city"],
                postal_code=record["postal_code"]
            )
            address.id = record["id_address"]
            addresses.append(address)
        return addresses


    def update(self, address: Address) -> bool:
        """Met à jour en BD l'entité Address correspondant à address, pour y correspondre

        :param address: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, address: Address) -> bool:
        """Supprime en BD l'entité Address correspondant à address

        :param address: cours dont l'entité Address correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
