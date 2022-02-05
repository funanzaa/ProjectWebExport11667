import psycopg2
import psycopg2.extras

class Database:

    def __init__(self):
        self.DB_HOST = "localhost"
        self.DB_NAME = "imed_db"
        self.DB_USER = "postgres"
        self.DB_PASS = 'postgres'

    def get_db_connection(self):
        conn = psycopg2.connect(dbname = self.DB_NAME, user = self.DB_USER, password = self.DB_PASS, host = self.DB_HOST)
        return conn

    def selectPlan(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = """
        select plan.plan_id,plan.plan_code,plan.description
        ,case when optype.description is null then 'ไม่ได้จับคู่' else optype.description end as optype_description
        ,optype.id
        from plan 
        left join optype on plan.map_optype::int = optype.id
        where plan.active = '1'
        """
        cur.execute(s) # Execute the SQL
        list_Plan = cur.fetchall()
        return list_Plan

    