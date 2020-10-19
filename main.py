import pymysql.cursors
import os
import sys
import re
from pprint import pprint
import inquirer
from inquirer.themes import GreenPassion
import json 

sys.path.append(os.path.realpath('.'))

questions = [
    inquirer.List('operation',
                  message="Which operation do you need?",
                  choices=['Create Table','INSERT', 'READ', 'UPDATE', 'DELETE'],
              ),
]

operation = inquirer.prompt(questions)
pprint(operation)
if operation.get('operation') in ['INSERT', 'READ', 'UPDATE', 'DELETE']:

    questions = [
        inquirer.List('table',
                    message="Choose table",
                    choices=['Users', 'Companies'],
                ),
    ]

    table = inquirer.prompt(questions)
    table_name = table.get('table')
    pprint(table)
# Connect to the database
connection = pymysql.connect(host='localhost',
                             port = 3307,
                             user='sara',
                             password='ouHQkltWnPhf0KVP',
                             db='crud_operations',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new table
        if operation.get('operation') == 'Create Table':
            questions = [
                    inquirer.Text('table',
                                message="Enter table name"),
                ]

            new_table_name = inquirer.prompt(questions)
            pprint(new_table_name)
            questions = [
            inquirer.Text('fields',
                        message='Enter fields name'),
            ]

            selected_fields = inquirer.prompt(questions)
            separated_fields = selected_fields.get('fields').split(' ')
            print(separated_fields)
            concatinate_query = ''
            query = ''
            for field in separated_fields:
                print(field)
                questions = [
                    inquirer.Text('choosed_fields',
                                    message=f"WHich fields in {field}",
                                    # choices=['Int(10)', 'Varchar(50)', 'Text(200)', 'Date', 'AUTO_INCREMENT', 'PRIMARY KEY','NULL'],
                    )]

                choosed_fields = inquirer.prompt(questions)
                pprint(choosed_fields)
                concatinate_fields = choosed_fields.get('choosed_fields').replace(',' , " ")
                concatinate_query += field + ' ' + concatinate_fields + ','

            sql = f"CREATE TABLE {new_table_name.get('table')} ({concatinate_query[:-1]})"

            print(sql)
        
        # Insert to table
        if operation.get('operation') == 'INSERT':
            if table_name == 'Users':
                questions = [
                    inquirer.Text('fullname',
                                message="What's fullname?"),
                    inquirer.Text('age',
                                message="What's your age, {fullname}?"),
                    inquirer.Text('profession',
                                message="What's your profession?",
                                )
                ]

                users_fields = inquirer.prompt(questions)
                pprint(users_fields)

                sql = f"INSERT INTO `{table_name}` (`fullname`, `age`, `profession`) VALUES ('{users_fields.get('fullname')}', '{users_fields.get('age')}','{users_fields.get('profession')}')"
            elif table_name == 'Companies':
                questions = [
                    inquirer.Text('name',
                                message="What's Company name?"),
                    inquirer.Text('location',
                                message="What's location?",
                                )
                ]

                companies_fields = inquirer.prompt(questions)
                pprint(companies_fields)
                sql = f"INSERT INTO `{table_name}` (`name`, `location`) VALUES ('{companies_fields.get('name')}', '{companies_fields.get('location')}')"
        #  READ table fields
        if operation.get('operation') == 'READ':
            questions = [
                inquirer.List('size',
                message="How many do you need?",
                choices=['All', 'For Current Id'],
            ),
            ]

            size = inquirer.prompt(questions)
            pprint(size)
            if size.get('size') == 'All':
                sql = f"SELECT * FROM `{table_name}` "
                cursor.execute(sql,)
                result = cursor.fetchall()
                pprint(result)
            elif size.get('size') == 'For Current Id':
                
                questions = [
                    inquirer.Text('id',
                                message="Enter an id?"),
                ]
                field_id = inquirer.prompt(questions)

                if table_name == 'Users':
                
                    sql = f"SELECT fullname,age, profession FROM `{table_name}` WHERE id = '{field_id.get('id')}' "
                
                elif table_name == 'Companies':
                    sql = f"SELECT name,location FROM `{table_name}` WHERE id = '{field_id.get('id')}' "

                cursor.execute(sql,)
                result = cursor.fetchone()
                pprint(result)

        # UPDATE Table field
        elif operation.get('operation') == 'UPDATE':
            if table_name == 'Users':
                questions = [
                    inquirer.Text('id',
                                message="Enter an id?"),
                ]

                field_id = inquirer.prompt(questions)

                questions = [
                    inquirer.Text('fullname',
                                message="What's fullname?"),
                    inquirer.Text('age',
                                message="What's your age, {fullname}?"),
                    inquirer.Text('profession',
                                message="What's your profession?",
                                )
                ]

                UPDATEd_fields = inquirer.prompt(questions)
                pprint(UPDATEd_fields)

                sql = f"UPDATE `{table_name}` SET fullname = '{UPDATEd_fields.get('fullname')}', age = '{UPDATEd_fields.get('age')}',profession = '{UPDATEd_fields.get('profession')}' WHERE id = '{field_id.get('id')}'"
            
            elif table_name == 'Companies':
                
                questions = [
                    inquirer.Text('id',
                                message="Enter an id?"),
                ]

                field_id = inquirer.prompt(questions)

                questions = [
                    inquirer.Text('name',
                                message="What's Company name?"),
                    inquirer.Text('location',
                                message="What's location?",
                                )
                ]

                UPDATEd_companies_fields = inquirer.prompt(questions)
                pprint(UPDATEd_companies_fields)
                sql = f"UPDATE `{table_name}` SET name = '{UPDATEd_companies_fields.get('name')}', location = '{UPDATEd_companies_fields.get('location')}' WHERE id = '{field_id.get('id')}'"
        #  DELETE table field
        elif operation.get('operation') == 'DELETE':
            questions = [
                inquirer.Text('id',
                            message="Enter an id?"),
            ]

            field_id = inquirer.prompt(questions)
            sql = f"DELETE FROM `{table_name}` WHERE id = '{field_id.get('id')}'"
         
        cursor.execute(sql,)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # READ a single record
        sql = "SELECT * FROM Users"
        cursor.execute(sql,)
        result = cursor.fetchall()
        out_file = open("dumpdata.json", "w") 
  
        json.dump(result, out_file, indent = 6) 
        
        out_file.close() 
finally:
    connection.close()
