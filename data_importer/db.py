import psycopg2
import json
from data_importer.logger import Logger

class Database:
    def __init__(self):
        import yaml

        with open("config/config.yaml", "r") as file:
            config = yaml.safe_load(file)["database"]

        self.connection = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            database=config["name"],
            user=config["user"],
            password=config["password"],
        )
        self.cursor = self.connection.cursor()
        self.logger = Logger()

    def insert_phone_data(self, phone_id, phone_name, phone_data):
        try:
            # Convert phone_data (dict) to JSON string
            phone_data_json = json.dumps(phone_data)
            query = """
                INSERT INTO phone (phoneid, phone_name, phone_data)
                VALUES (%s, %s, %s)
                ON CONFLICT (phoneid) DO NOTHING;
            """
            self.cursor.execute(query, (phone_id, phone_name, phone_data_json))
            self.connection.commit()
        except Exception as e:
            self.logger.log(f"Error inserting phone data: {e}", level="error")
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()
