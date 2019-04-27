# encoding: utf8
import mysql.connector

class DB:

    def abrir(self):
        conexion=mysql.connector.connect(host="localhost", 
                                              user="pi", 
                                              passwd="na", 
                                              database="circuito")
        self.cont=0 
        self.cont1=0
        #~ self.acce=StringVar()                                               
        return conexion


    def alta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into articulos(descripcion, precio) values (%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()
        
    def grabavuelta(self, datos):
                           
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into automatico(idcoche, idusuario, data) values (%s,%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()
        
    def getfvueltagrabada(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select data from automatico where idcoche=%s and idusuario= %s" 
        cursor.execute(sql, datos)
        cone.close()
        return cursor.fetchall()                      
            
    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select * from usuarios where id=" + str(datos)
        cursor.execute(sql, datos)
        cone.close()
        return cursor.fetchall()

    def recuperar_todos(self,tabla):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select * from " + tabla
        cursor.execute(sql)
        cone.close()
        return cursor.fetchall()

    def baja(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="delete from articulos where codigo=%s"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()
        return cursor.rowcount # retornamos la cantidad de filas borradas

    def modificacion(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update articulos set descripcion=%s, precio=%s where codigo=%s"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()
        return cursor.rowcount # retornamos la cantidad de filas modificadas
