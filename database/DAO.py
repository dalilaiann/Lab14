from database.DB_connect import DBConnect
from model.arco import Arco
from model.order import Order


class DAO():

    @staticmethod
    def getAllStores():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select store_id
                   from stores"""

        cursor.execute(query)

        res = []

        for row in cursor:
            res.append(row["store_id"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllNodes(store_id):
            cnx=DBConnect.get_connection()
            cursor=cnx.cursor(dictionary=True)

            query="""select *
                     from orders 
                     where store_id =%s"""

            cursor.execute(query, (store_id,))

            res=[]

            for row in cursor:
                res.append(Order(**row))

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getAllEdges(store_id, idMap):
            cnx=DBConnect.get_connection()
            cursor=cnx.cursor(dictionary=True)

            query="""select o1.order_id as n1, o2.order_id as n2, SUM(oi.quantity)+SUM(oi2.quantity) as tot
                    from orders o1, orders o2, order_items oi, order_items oi2 
                    where o1.order_id !=o2.order_id
                    and oi.order_id =o1.order_id 
                    and oi2.order_id =o2.order_id 
                    and datediff(o1.order_date,o2.order_date)<5
                    and datediff(o1.order_date,o2.order_date)>0
                    and oi.item_id!=oi2.item_id 
                    and o1.store_id =%s
                    and o1.store_id =o2.store_id 
                    group by o1.order_id, o2.order_id """

            cursor.execute(query, (store_id,))

            res=[]

            for row in cursor:
                res.append(Arco(idMap[row["n1"]], idMap[row["n2"]], row["tot"]))

            cursor.close()
            cnx.close()
            return res

if __name__ == '__main__':
    print(len(DAO.getAllNodes(1)))
