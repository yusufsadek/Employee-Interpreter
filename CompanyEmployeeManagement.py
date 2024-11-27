import cmd      #cmd module for command processor base class (interactive shells & command interperters) read: command processing -> creating an interpreter class 
import os       #file handling for import/export (directory access)
import csv      #file formatting for import/export (MS_excel format: RFC 4180)


class CompanyEmployees(cmd.Cmd):    #interpreter(s) class using the base class with do_ keyword for interpreting and .Cmd argument to add "help" (dependent topmost aggregation)

    prompt = '[Company] Management>> '                                                                             #Shell Prompt (name)
    intro  = 'Welcome to the Employee Data Management System. Type "help" for a list of Avaliable commands.'       #landing prompt (display)

    def __init__(self):
        
        super().__init__()                              #interpreter inherets all methods and properties from parent argument (cmd module) (super = self.name abstraction)
        self.current_directory = os.getcwd()            #initialize current access directory for import/export to current working directory 
        self.manager = Manager()                        #initialize a Manager instance through the top most class for proper data propagation and validation
        self.manager.Load_Employees()                   #Automatic loading of employees from the default file (Current_list) through the Manager Class(encapsulation)
        pass

    def do_Menu(self, arguments):                       #+interpreter can receive serial arguments ! and parses through them on its own! 
        #abstracted instruction for displaying command menu
        print(f"\t \t MAIN MENU \n>Employees(1) \n>List(2) \n>Update(3) \n>Find(4) \n>Quit(0)\n")
        opcode = int(input("Selection....:"))
        
        #Function Call look-up table 
        if  opcode == 1:
            self.do_Display_All(arguments)
        elif opcode == 2:
            file_name = (input("List Name....:"))
            self.do_Load(file_name)
        elif opcode == 3:
            uindex = (input("Employee ID....:"))
            self.do_Modify(uindex)
        elif opcode == 4:
            uindex = (input("Employee ID....:"))
            self.do_Find(uindex)
        elif opcode == 0:
            self.do_Quit()
        else:
            print(f"ERROR:Invalid Option, Expected Options are: [1|2|3|4|0]")
        pass
#+"about" is redundant to a find function hence uneeded
#+do_xx methods naming convention is also redundant, changed for better user experience *(Update_Old -> Modify) help_xxx methods: brackets removed due to automatic parsing of class

    def do_Add(self, arguments):
        """Appends a new Employee to the list. \n~Use the command followed by the Employee's ID; Add <ID>~"""

        if not arguments.strip():                                                #+strip uneeded whitespace from parsing 
            print(f"ERROR: No ID has been entered. \n~Please Refer to <help Add_New>~")
            return                                                               #+returning from conditions provides better time complexity as well (pass but for conditions)
        try:
            #+Manager Already Iinitialized 
            uindex = int(arguments.strip())                                      #+Ensure ID is in proper format (Validation)
            #+Serialization can be handeled in Save Employees method to offer better readability since it will be needed for all do_ methods that Incorporate CSV 
            #+as well as the writing (saving) and confirmation ultimately cleaning up the code entirely here :)
            self.manager.Add_Employee(uindex)
            self.manager.Save_Employees()                            
        except ValueError as e:
            print(e)
        pass

    def do_Delete(self, arguments):
        """Removes an old Employee from the list. \n~Use the command followed by the Employee's unique index in brackets; Delete <ID>~"""

        if not arguments.strip():                                                
            print(f"ERROR: No ID has been entered. \n~Please Refer to <help Delete_Old>~")
            return
        try:
            #+again removing the clutter and redundancy of saving :)
            uindex = int(arguments.strip())
            self.manager.Remove_Employee(uindex)
            self.manager.Save_Employees()           
        except ValueError as e:
            print(e)
        pass

    def do_Modify(self, arguments):
        """Replaces Employee Old Data field with new one. \n~Use the command followed by the Employee's unique index; Modify <ID>~"""

        if not arguments.strip():
            print(f"ERROR: No ID has been entered. \n~Please Refer to <help Modify>~")
            return
        try:
            uindex = int(arguments.strip())
            self.manager.Modify_Data(uindex)
            self.manager.Save_Employees()
        except ValueError as e:
            print(e)
        pass
    
    def do_Display_All(self, arguments):
        """Displays the list of all Employees Currently Loaded."""

        if not self.manager.employees:              #+validation for initialized list of employees for error handling... <- learned the hard way (bool syntaxed)
            print("No Employees Loaded in the system. \n~Please Refer to <help Load>")
        else:
            print("Current Employee(s) Data:")
            for employee in self.manager.employees:
                print(employee.Employee_Data())     #using the getter defined in the Generalization Employee 
        pass

    def do_Load(self, file_name = 'Current_list.csv'):
        """Reads data from a file in the directory. \n~Use the command followed by the File name; Load_List(Current list)~"""

        #+Functionality here was considered wrongly as Loading of the employees into the list and printing can be split into: (Load, Display_All) ! merging is a bad consideration. 
        try:
            self.manager.Load_Employees(file_name)
            print("DONE:Employee list loaded successfully!")
        except FileNotFoundError:
            print(f"ERROR: File '{file_name}' is not Found.") 
        #+all of the manager intizilations & loading is cleaned up through initializing it in the Interperter class ! 
        pass

    def do_Create_Empty(self, file_name):
        """Creates a file in the current directory. \n~Use the command followed by the File name; Create <file name>~"""

        file_path = os.path.join(self.current_directory, file_name)     
        try:
            with open(file_name,'w') as new_file:                          
                print(f"File '{file_name}' has been created in {self.current_directory}")                           
        except FileNotFoundError:
            print(f"ERROR: File '{file_name}' is not Found.") 
        pass
    #+Update_Old replaced with Modify and moved for better structure

    def do_Find(self, arguments):
        """Finds an Employee in the Loaded List. \n~Use the command followed by the Employee's ID; Find <ID>"""

        if not arguments.strip():
            print("ERROR: No ID provided. Usage: Find <ID>")
            return
        try:
            uindex = int(arguments.strip())         
            employee = self.manager.Find_Employee(uindex)               #+Moved function to Manager class for better readability
            if employee:                                                #Boolean syntax used to check for employee validity in list (optimization)
                print(employee.Employee_Data())
            else: 
                print(f"ERROR: Employee with ID {uindex} not found.")
        except:
             print(f"ERROR: Employee with ID {uindex} not found.")
        pass

    def do_Quit(self, arguments):
        """Exits the Program."""
        print("Exiting the Company Management System. Goodbye!")
        return True
        pass

    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability of cmd console 
        return stop

class Employee:                     #parent class (generalization) 

    def __init__(self, uindex, full_name, role, salary, email):

        self.uindex   = uindex                                                 #employee unique identifier 
        self.name     = full_name                                              #employee full name
        self.position = role                                                   #employee job position 
        self.salary   = salary                                                 #monthly  salary 
        self.email    = email                                                  #electronic mail contact 
        
        pass

    def Employee_Data(self):
        #returns all employee data for various methods to use(encapsulated) 
        return (f"Employee ,'{self.uindex}', Data:\n"
         f"Full Name: '{self.name}' \n"
         f"Position: '{self.position}' \n"
         f"Salary: '${self.salary}' \n"
         f"E-mail: '{self.email}'")
#+Manager class does not need to inherit the attributes of employees     

class Manager:            #+ cannot be a dependent/child class! 

    def __init__(self): 

        #super().__init__()          #Every Manager must be an Employee, but this is unnecessary as the inhertiance is initialized in the interperter class definition
        self.employees = []          #Every Manager manages a list of Employees 
        pass

    def Load_Employees(self, file_name = 'Current_list.csv'):
        #Loads Employees from an existing list to the manager class
        try:
            with open(file_name, 'r') as existing_file:
                #initialize a CSV reader object
                csv_reader = csv.reader(existing_file)
                next(csv_reader, None)                                                             #skipping header row if one exists
                self.employees = [
                    Employee(int(row[0]), row[1], row[2], float(row[3]), row[4])
                    for row in csv_reader if len(row) == 5
                ]                                                                                   #assignment of each row of employee to an initialized list (LOTS OF BUGS) 
        except FileNotFoundError:
            print(f"File '{file_name}' was not found. Starting with an Empty Employee List")
        pass

    def Save_Employees(self, file_name = 'Current_list.csv'):
        #Commits and reflects changes to the file
        with open(file_name, 'w', newline='') as existing_file:
            csv_writer = csv.writer(existing_file)
            csv_writer.writerow(["ID", "Name", "Position", "Salary", "Email"])                                #Write header for list
            for employee in self.employees:
                csv_writer.writerow([employee.uindex, employee.name, employee.position, employee.salary, employee.email])
        pass

    def Add_Employee(self, uindex):
        #adds a new Employee by taking the data from the user directly and not through the code 
        if not isinstance(uindex, int):                                             #verification of correct object type & integer ID
            raise ValueError("ERROR: Employee ID Must be an integer.")              
        if uindex in [employee.uindex for employee in self.employees]:              #Checking for existing ID(debug)
            raise ValueError("ERROR: Employee ID already exists!")
        name   = input("Employee's Full name: ")                            #inputting the data from user to protect user data  (encapsulation)

        role   = input("Employee Work Position: ")

        salary = self.Validate_Salary(float(input("Monthly Salary:")))      #+using Static methods defined below for validation of input (salary and email) 

        email  = self.Validate_email(input("eContact: "))

        self.employees.append(Employee(uindex, name, role, salary, email))  #assignment of employee data to index & employee data to a new employee 

        print(f"DONE:Employee with ID {uindex} added successfully!")        #confirmation for debugging 
        pass

    def Remove_Employee(self, uindex):
        #removes an Employee by their unique index  
        for employee in self.employees:
            if employee.uindex == uindex:
                self.employees.remove(employee)                                    #+built in remove to simplify everything (next method might have been causing issues) 
                print(f"DONE:Employee with ID {uindex} removed successfully!")
        pass

    def Modify_Data(self, uindex):
        #+using the cleanly defined Find method mentioned below and similar structuring to adding an employee
        #;Employee validation is much more simple. ORing the values is a beautiful method i found during fixing this to clean up much of the clutter. 
        employee = self.Find_Employee(uindex)
        if not employee: 
            raise ValueError(f"ERROR: Employee with ID {uindex} not found.")
        print("Leave Fields Blank to keep Current Values")
        #+similarly the validated data can be exception handled only through out if conditions and DOES NOT NEED TRY/EXCEPT/FINALLY
        n_name   = input(f"New Name (current: {employee.name}): ") or employee.name

        n_role   = input(f"New Position (current: {employee.position}): ") or employee.position

        n_salary = input(f"New Salary (current: {employee.salary}): ")
        n_salary = self.Validate_salary(n_salary) if n_salary else employee.salary

        n_email  = input(f"New Email (current: {employee.email}): ")
        n_email  = self.Validate_email(n_email) if n_email else employee.email
        #assign new updated values(normally; since the employee is defined as a call to the method and not an instance)
        employee.name     = n_name
        employee.position = n_role
        employee.salary   = n_salary
        employee.email    = n_email
        print(f"DONE:Employee with ID {uindex} updated successfully!")
        pass

    def Find_Employee(self, uindex):
    #+moved method for integration in other classes.
        for employee in self.employees:
            if employee.uindex == uindex:
                return employee
        return None                         #secondary operatation -> no employee found = None ~ False for bool checking 

    @staticmethod                           #+Method that does not depend on instance!!! (doesnt need a self argument/parameter) (read: singletrons and multithreading)
    def Validate_salary(salary):
        #Static method (independent of self) to validate salary in valid number form
        try:
            salary = float(salary)
            if salary <= 0:
                raise ValueError("ERROR: Salary must be a positive number.")
            return salary
        except:
            print(f"ERROR: Salary must be a valid number.")
        pass

    @staticmethod
    def Validate_email(email):
        if "@" not in email or "." not in email:
            raise ValueError("ERROR: Invalid email address.")
        return email

#Command Line Interface Driver
if __name__ == '__main__':
    CompanyEmployees().cmdloop()

