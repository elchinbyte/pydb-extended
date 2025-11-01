import psycopg2

class DatabaseConnector:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

class DepartmentCRUD(DatabaseConnector):
    def add_department(self, title):
        self.cursor.execute("INSERT INTO departament (title) VALUES (%s)", (title,))
        self.commit()
        print("Department added successfully")

    def view_departments(self):
        self.cursor.execute("SELECT * FROM departament ORDER BY id")
        for dep in self.cursor.fetchall():
            print(f"ID: {dep[0]}, Title: {dep[1]}")

    def update_department(self, dep_id, new_title):
        self.cursor.execute("UPDATE departament SET title=%s WHERE id=%s", (new_title, dep_id))
        self.commit()
        print("Department updated")

    def delete_department(self, dep_id):
        self.cursor.execute("DELETE FROM departament WHERE id=%s", (dep_id,))
        self.commit()
        print("Department deleted")

class CountryCRUD(DatabaseConnector):
    def add_country(self, title, country_type):
        self.cursor.execute("INSERT INTO country (title, country_type) VALUES (%s, %s)", (title, country_type))
        self.commit()
        print("Country added")

    def view_countries(self):
        self.cursor.execute("SELECT * FROM country ORDER BY id")
        for c in self.cursor.fetchall():
            print(f"ID: {c[0]}, Title: {c[1]}, Type: {c[2]}")

    def update_country(self, country_id, new_title, new_type):
        self.cursor.execute("UPDATE country SET title=%s, country_type=%s WHERE id=%s",
                            (new_title, new_type, country_id))
        self.commit()
        print("Country updated")

    def delete_country(self, country_id):
        self.cursor.execute("DELETE FROM country WHERE id=%s", (country_id,))
        self.commit()
        print("Country deleted")

class EmployeeCRUD(DatabaseConnector):
    def add_employee(self, name, last_name, country_id, departament_id, salary, email, phone):
        self.cursor.execute("""
            INSERT INTO employee (name, last_name, country_id, departament_id, salary, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, last_name, country_id, departament_id, salary, email, phone))
        self.commit()
        print("Employee added")

    def view_employees(self):
        self.cursor.execute("""
            SELECT e.id, e.name, e.last_name, c.title AS country, d.title AS departament, e.salary, e.email, e.phone
            FROM employee e
            JOIN country c ON e.country_id = c.id
            JOIN departament d ON e.departament_id = d.id
            ORDER BY e.id
        """)
        for emp in self.cursor.fetchall():
            print(f"{emp[0]}. {emp[1]} {emp[2]} | {emp[3]} | {emp[4]} | Salary: {emp[5]} | Email: {emp[6]} | Phone: {emp[7]}")

    def update_employee(self, emp_id, salary=None, email=None, phone=None):
        updates = []
        params = []

        if salary:
            updates.append("salary=%s")
            params.append(salary)
        if email:
            updates.append("email=%s")
            params.append(email)
        if phone:
            updates.append("phone=%s")
            params.append(phone)

        if updates:
            params.append(emp_id)
            query = f"UPDATE employee SET {', '.join(updates)} WHERE id=%s"
            self.cursor.execute(query, tuple(params))
            self.commit()
            print("Employee updated")

    def delete_employee(self, emp_id):
        self.cursor.execute("DELETE FROM employee WHERE id=%s", (emp_id,))
        self.commit()
        print("Employee deleted")

    def search_by_country_and_department(self, country_title, department_title):
        self.cursor.execute("""
            SELECT e.name, e.last_name, c.title AS country, d.title AS departament
            FROM employee e
            JOIN country c ON e.country_id = c.id
            JOIN departament d ON e.departament_id = d.id
            WHERE c.title ILIKE %s AND d.title ILIKE %s
        """, (f"%{country_title}%", f"%{department_title}%"))
        results = self.cursor.fetchall()

        if not results:
            print("No employees found.")
        else:
            for r in results:
                print(f"{r[0]} {r[1]} | {r[2]} | {r[3]}")

def main():
    dbname = "pydb"
    user = "postgres"
    password = "1234"

    emp = EmployeeCRUD(dbname, user, password)
    dep = DepartmentCRUD(dbname, user, password)
    country = CountryCRUD(dbname, user, password)

    while True:
        print("\nMAIN MENU")
        print("1. Department CRUD")
        print("2. Country CRUD")
        print("3. Employee CRUD")
        print("4. Search Employee by Country & Department")
        print("5. Exit")

        choice = input("Choice: ")

        if choice == "1":
            print("\nDepartment CRUD")
            print("1) Add  2) View  3) Update  4) Delete")
            sub = input("Choose: ")
            if sub == "1":
                dep.add_department(input("Title: "))
            elif sub == "2":
                dep.view_departments()
            elif sub == "3":
                dep.update_department(input("ID: "), input("New title: "))
            elif sub == "4":
                dep.delete_department(input("ID: "))

        elif choice == "2":
            print("\nCountry CRUD")
            print("1) Add  2) View  3) Update  4) Delete")
            sub = input("Choose: ")
            if sub == "1":
                country.add_country(input("Title: "), input("Type: "))
            elif sub == "2":
                country.view_countries()
            elif sub == "3":
                country.update_country(input("ID: "), input("New title: "), input("New type: "))
            elif sub == "4":
                country.delete_country(input("ID: "))

        elif choice == "3":
            print("\nEmployee CRUD")
            print("1) Add  2) View  3) Update  4) Delete")
            sub = input("Choose: ")
            if sub == "1":
                emp.add_employee(
                    input("Name: "),
                    input("Last name: "),
                    input("Country ID: "),
                    input("Department ID: "),
                    input("Salary: "),
                    input("Email: "),
                    input("Phone: ")
                )
            elif sub == "2":
                emp.view_employees()
            elif sub == "3":
                emp.update_employee(
                    input("Employee ID: "),
                    input("New salary (blank to skip): ") or None,
                    input("New email (blank to skip): ") or None,
                    input("New phone (blank to skip): ") or None
                )
            elif sub == "4":
                emp.delete_employee(input("Employee ID: "))

        elif choice == "4":
            c = input("Enter country title: ")
            d = input("Enter department title: ")
            emp.search_by_country_and_department(c, d)

        elif choice == "5":
            emp.close()
            dep.close()
            country.close()
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
