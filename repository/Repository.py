import mysql.connector
from mysql.connector import errorcode
from typing import List, Tuple, Any


class Repository:
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: str = "3306",
        user: str = "root",
        password: str = "your_new_password",
        database: str = "ehr_records",
    ):
        try:
            self.cnx = mysql.connector.connect(
                host=host, port=port, user=user, password=password, database=database
            )
            self.cursor = self.cnx.cursor(dictionary=True)
            print("Successfully connected to database!")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            raise

    def retrieve_info(self, query: str) -> List[dict]:
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            raise

    def retrieve_one(self, query: str) -> dict:
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            raise

    def execute_query(self, query: str, params: Tuple = None) -> None:
        try:
            self.cursor.execute(query, params)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            self.cnx.rollback()
            raise

    def __del__(self):
        if hasattr(self, "cursor") and self.cursor:
            self.cursor.close()
        if hasattr(self, "cnx") and self.cnx:
            self.cnx.close()


# if __name__ == "__main__":
#     try:
#         repo = Repository()
#         # Example queries
#         drug_routes = repo.retrieve_info(
#             "SELECT DISTINCT drugs.route FROM drugs WHERE drugs.drug = 'methimazole';"
#         )
#         print("Drug routes:", drug_routes)

#         # Example with single result
#         single_drug = repo.retrieve_one(
#             "SELECT * FROM drugs WHERE drug = 'methimazole' LIMIT 1;"
#         )
#         print("Single drug info:", single_drug)

#     except Exception as e:
#         print(f"An error occurred: {e}")
