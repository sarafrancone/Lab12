from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    @staticmethod
    def getCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct gr.Country 
                    from go_sales.go_retailers gr 
                    order by gr.Country """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getRetailers(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct gr.*
                    from go_sales.go_retailers gr 
                    where gr.Country = %s
                    order by gr.Retailer_code """

        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdgesPesati(year, country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinctrow g.Retailer_code as r1, g2.Retailer_code as r2, count(distinct(gs.Product_number )) as peso
                    from go_sales.go_retailers g , go_sales.go_retailers g2, go_sales.go_daily_sales gs, go_sales.go_daily_sales gs2
                    where year(gs.`Date` ) = %s and year(gs2.`Date`)=%s and g.Country = %s and g2.Country = %s
                    and g.Retailer_code != g2.Retailer_code
                    and g.Retailer_code = gs.Retailer_code and g2.Retailer_code = gs2.Retailer_code 
                    and gs2.Product_number = gs.Product_number 
                    group by g.Retailer_code, g2.Retailer_code """

        cursor.execute(query, (year, year, country, country))

        for row in cursor:
            result.append( (row["r1"], row["r2"], row["peso"]) )

        cursor.close()
        conn.close()
        return result