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


# Map LabFu

    def selectItemMapLapFu(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        select item_code, common_name, item_id,case when item.map_labfu is not null then map_labfu.id||' | '||map_labfu.name else 'False' end as map_labfu 
        from item 
        left join map_labfu on item.map_labfu = map_labfu.id
        where  active = '1'
        """
        cur.execute(sql) # Execute the SQL
        list_Item = cur.fetchall()
        cur.close()
        conn.close()
        return list_Item

    def selectItemNhsoLabFu(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
            select * from map_labfu
        """
        cur.execute(sql) # Execute the SQL
        list_Item = cur.fetchall()
        cur.close()
        conn.close()
        return list_Item
    
    def editNhsoLabFu(self, id):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
            select item_code, common_name, item_id,map_labfu from item where item_id = '{}'
        """.format(id)
        cur.execute(sql) # Execute the SQL
        list_editNhsoLabFu = cur.fetchall()
        cur.close()
        conn.close()
        return list_editNhsoLabFu

    def updateNhsoLabFu(self, item_id, id):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
            update item set map_labfu = '{}' where item_id = '{}'
        """.format(id, item_id)
        cur.execute(sql) # Execute the SQL
        conn.commit()
        print("updateNhsoLabFu OK ")
        cur.close()
        conn.close()

# Free Schedule

    def ListFeeSchedule(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        select pcp_item_code, pcp_item_desc, pcp_cdg_opd, pcp_cdg_opd_price,pcp_item_rn
        from pcp_item 
        order by pcp_item_code 
        """
        cur.execute(sql) # Execute the SQL
        ListFeeSchedule = cur.fetchall()
        cur.close()
        conn.close()
        return ListFeeSchedule

    
    def ListIsMatchFeeSchedule(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        -- Is match
        select item_code,common_name,pcp_item.pcp_item_code,pcp_item.pcp_item_desc,pcp_item.pcp_cdg_opd_price,item_id
        from item 
        left join pcp_item on item.pcp_item_rn = pcp_item.pcp_item_rn
        where item.pcp_item_rn is not null and item.active = '1'
        """
        cur.execute(sql) # Execute the SQL
        ListIsMatchFeeSchedule = cur.fetchall()
        cur.close()
        conn.close()
        return ListIsMatchFeeSchedule

    def ListNotMatchFeeSchedule(self):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
        -- Not match
        select item_code,common_name,item_id 
        from item 
        where item.pcp_item_rn is null and item.active = '1'
        """
        cur.execute(sql) # Execute the SQL
        ListIsMatchFeeSchedule = cur.fetchall()
        cur.close()
        conn.close()
        return ListIsMatchFeeSchedule

    def GetCommonNameItem(self, item_id):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
            select common_name,item_code,item_id from item where item_id = '{}'
        """.format(item_id)
        cur.execute(sql) # Execute the SQL
        GetCommonNameItem = cur.fetchall()
        cur.close()
        conn.close()
        return GetCommonNameItem

    def UpdateMatchFeeSchedule(self, pcp_item_rn, item_id):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
            update item set pcp_item_rn = '{}', pcp_item_update_date = now() where item_id = '{}'
        """.format(pcp_item_rn, item_id)
        cur.execute(sql) # Execute the SQL
        conn.commit()
        print("UpdateMatchFeeSchedule OK ")
        cur.close()
        conn.close()

    def DeleteMatchFeeSchedule(self, item_id):
        conn = self.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
            update item set pcp_item_rn = null, pcp_item_update_date = null where item_id = '{}'
        """.format(item_id)
        cur.execute(sql) # Execute the SQL
        conn.commit()
        print("DeleteMatchFeeSchedule OK ")
        cur.close()
        conn.close()


