from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def get_rifugio() -> list[Rifugio] | None:

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM rifugio"""
        try:
            cursor.execute(query)
            for row in cursor:
                rifugio = Rifugio(
                    id=row["id"],
                    nome=row["nome"],
                    localita=row["localita"],
                    altitudine=row["altitudine"],
                    capienza=row["capienza"],
                    aperto=row["aperto"]
                )
                result.append(rifugio)
        except Exception as e:
            print(f"Errore durante la query get_rifugio: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_connessione(anno) -> list[Connessione] | None:

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        # La query unifica le direzioni (A-B e B-A diventano la stessa riga grazie a LEAST/GREATEST)
        query = """SELECT LEAST(id_rifugio1,id_rifugio2) AS r1,
                                GREATEST(id_rifugio1,id_rifugio2) AS r2, 
                                anno, distanza, difficolta
                        FROM connessione c, rifugio r
                        WHERE anno <= %s and (r.id = c.id_rifugio1 or r.id = c.id_rifugio2)
                        GROUP BY r1,r2"""
        try:
            cursor.execute(query, (anno,))
            for row in cursor:
                connessione = Connessione(
                    r1=row["r1"],
                    r2=row["r2"],
                    anno=row["anno"],
                    distanza = row["distanza"],
                    difficolta = row["difficolta"]
                )
                result.append(connessione)
        except Exception as e:
            print(f"Errore durante la query get_connessione: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
    # TODO
