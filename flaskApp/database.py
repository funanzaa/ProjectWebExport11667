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
        cur.close()
        conn.close()
        return list_Plan

    def selectOPTYPE(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = 'select * from optype'
        cur.execute(sql) # Execute the SQL
        list_optype = cur.fetchall()
        cur.close()
        conn.close()
        return list_optype

    def selectDescPlan(self,plan_id):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        select distinct(description),map_optype,plan_id from plan where plan_id = '{}'
        """.format(plan_id)
        cur.execute(sql) # Execute the SQL
        list_DescPlan = cur.fetchall()
        return list_DescPlan

    def updatePlan(self,id_optype,id_plan):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        update plan set map_optype = '{}' where plan_id = '{}'
        """.format(id_optype,id_plan)
        cur.execute(sql) # Execute the SQL
        conn.commit()
        print("update Plan OK")
        cur.close()
        conn.close()

    def deleteMapPlan(self,id_plan):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        update plan set map_optype = null where plan_id = '{}'
        """.format(id_plan)
        cur.execute(sql) # Execute the SQL
        conn.commit()
        print("update Plan OK")
        cur.close()
        conn.close()


    def selectItem(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
         select item_code, common_name, item_id,case when map_highcost = true then 'True' else 'False' end as map_highcost from item where  active = '1'
        """
        cur.execute(sql) # Execute the SQL
        list_Item = cur.fetchall()
        cur.close()
        conn.close()
        return list_Item

    def updateHighCost(self, id, status):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        update item set "map_highcost" = '{}' where item_id = '{}'
        """.format(status, id)
        cur.execute(sql) # Execute the SQL
        conn.commit()
        print("update updateHighCost OK")
        cur.close()
        conn.close()

    # Map billingGroup 

    def selectBillingGroupOPD(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        select base_billing_group_id,code,description_th,map_chrgitem.id
        ,case when (right(trim(map_chrgitem.id),1) is not null or right(trim(map_chrgitem.id),1) <> '') and right(trim(map_chrgitem.id),1) = '2' then map_chrgitem."name" || '(ส่วนเกิน)'  else map_chrgitem."name" end 
        ,'opd' as type_name
        from base_billing_group 
        left join map_chrgitem on base_billing_group.map_chrgitem_opd = map_chrgitem.id
        """
        cur.execute(sql) # Execute the SQL
        list_Item = cur.fetchall()
        cur.close()
        conn.close()
        return list_Item

    def selectBillingGroupIPD(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        select base_billing_group_id,code,description_th,map_chrgitem.id
        ,case when (right(trim(map_chrgitem.id),1) is not null or right(trim(map_chrgitem.id),1) <> '') and right(trim(map_chrgitem.id),1) = '2' then map_chrgitem."name" || '(ส่วนเกิน)'  else map_chrgitem."name" end 
        ,'ipd' as type_name
        from base_billing_group 
        left join map_chrgitem on base_billing_group.map_chrgitem_ipd = map_chrgitem.id
        """
        cur.execute(sql) # Execute the SQL
        list_Item = cur.fetchall()
        cur.close()
        conn.close()
        return list_Item

    def selectMapChrgitem(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        select id
        ,case when right(id,1) = '2' then "name"|| '(ส่วนเกิน)' else "name" end as "name"
        from map_chrgitem
        """
        cur.execute(sql) # Execute the SQL
        list_Item = cur.fetchall()
        cur.close()
        conn.close()
        return list_Item

    def selectBillingEdit(self, id , typename):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        if typename == 'opd':
            sql = """
            select map_chrgitem_opd,description_th from base_billing_group where base_billing_group_id = '{}'
            """.format(id)
        elif typename == 'ipd':
            sql = """
            select map_chrgitem_ipd,description_th from base_billing_group where base_billing_group_id = '{}'
            """.format(id)

        cur.execute(sql) # Execute the SQL
        list_Item = cur.fetchall()
        cur.close()
        conn.close()
        return list_Item
    
    def UpdateBillingGroup(self, chrgitem_id, base_billing_group_id, typename):
        print( chrgitem_id, base_billing_group_id, typename)
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if typename == 'opd':
            sql = """
            update base_billing_group set map_chrgitem_opd = '{}' where base_billing_group_id = '{}'
            """.format(chrgitem_id, base_billing_group_id)
            cur.execute(sql) # Execute the SQL
            conn.commit()
            print("UpdateBillingGroup OK OPD")
            cur.close()
            conn.close()
        elif typename == 'ipd':
            sql = """
            update base_billing_group set map_chrgitem_ipd = '{}' where base_billing_group_id = '{}'
            """.format(chrgitem_id, base_billing_group_id)
            cur.execute(sql) # Execute the SQL
            conn.commit()
            print("UpdateBillingGroup OK IPD")
            cur.close()
            conn.close()