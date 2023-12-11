"""
Program Name: Banking App Part 2
Author:       Emily Huynh
Date:         April 5, 2023 
Description:  This is a banking application.
"""
import replit 
import time
from colorama import Fore

class NegativeError(Exception): # when user enters a negative amount
  pass
class ImpossibleValueError(Exception): # when user tries to withdraw more than balance
  pass

def accounts_saved(): # takes saved account info from accounts file, then makes lists of items
  database=open("accounts.txt", "r")
  user_list=[]
  password_list=[]
  balance_list=[]
  for i in database: 
    a,b,c = i.split(", ") # separates items: a=usernames, b=passwords, c=balances
    b = b.strip()
    user_list.append(a) 
    password_list.append(b) 
    balance_list.append(c) 
  return user_list, password_list, balance_list

def login_exceptions(entered_username, entered_passcode, saved_accounts): # exception handling for login
  try:
    if saved_accounts[entered_username]:
      try:
        if entered_passcode == saved_accounts[entered_username]: # if entered username and password matches
          print (Fore.GREEN+"Logging in..."+Fore.WHITE)          # log in
          time.sleep(1)
          return False, False
        else:
          print(Fore.RED+"Incorrect password or username."+Fore.WHITE)
          return True, True
      except:
          print(Fore.RED+"Incorrect password or username."+Fore.WHITE)
          return True, True
    else: 
      print(Fore.RED+"Account does not exist."+Fore.WHITE)
      return True, True
  except: print(Fore.RED+"Account does not exist."+Fore.WHITE)
  return True, True

def menu(): 
  print (Fore.WHITE+"Menu"+Fore.BLUE+"\n1. Withdrawal"+Fore.MAGENTA+"\n2. Deposit"+Fore.BLACK + "\n3. View Balance"+Fore.CYAN+"\n4. Quit"+Fore.WHITE+"")

def new_bal_withdraw(initial_val): # balance calculation after withdrawal
  return (initial_val-amount)

def new_bal_deposit(initial_val): # balance calculation after deposit
  return (initial_val+amount)

def delay_and_clear(delay): # gives reader time to read text, then returns to menu
  time.sleep(delay)
  print(Fore.WHITE+"""
Returning to menu...""")
  time.sleep(1.5)

def withdraw_exceptions(): # makes sure user withdrawal is valid
  while True:
    try:
      withdrawal = float(input(Fore.WHITE+"How much would you like to withdraw?: $"))
      if withdrawal<0:
        raise NegativeError
      elif withdrawal>balance:
        raise ImpossibleValueError
    except ValueError: 
      print(Fore.RED+"Amount must be a number, please try again.\n")
      continue     
    except NegativeError:
      print(Fore.RED+"Amount must be positive, please try again.\n")
      continue     
    except ImpossibleValueError: 
      print(Fore.RED+"Sorry, your limit is $"+str(format(balance,'.2f'))+", please try again.\n")
      continue  
    return withdrawal

def deposit_exceptions(): # makes sure user deposit is valid
  while True:
    try:
      deposit = float(input(Fore.WHITE+"How much would you like to deposit?: $"))
      if deposit<0:
        raise NegativeError
    except ValueError:
      print(Fore.RED+"Amount must be a number, please try again.\n")
      continue     
    except NegativeError:
      print(Fore.RED+"Amount must be positive, please try again.\n")
      continue  
    return deposit 

while True:
  saved_users, saved_passwords, saved_balances = accounts_saved() # assigns saved account info to variables
  login = dict(zip(saved_users, saved_passwords))
  account_balances = dict(zip(saved_users, saved_balances))

  login_attempt = True
  ReturnToStart = True
  new_account = False

  while ReturnToStart:
    transactions=[]
    print("\033[1m" + "Welcome to EH Banking"+ "\033[0m") # Starting screen
    account = input("\n1-Login\n2-Create new account\n\nSelect an action: ")
    replit.clear()  

    match account:
      case "1": # user login
        print("Enter 0 to go back.")
        while login_attempt==True:
          username = input("\nUsername: ")
          if username=="0": # returns to start when 0 is entered
            replit.clear()
            break
          password = input("Password: ")
          ReturnToStart, login_attempt = login_exceptions (username, password, login)

      case "2": # user sign up
        while True: 
          print("Enter 0 to go back.")
          username = input("\nCreate username: ")
          if username=="0": # returns to start when 0 is entered
            replit.clear()
            break
          password = input("Create password: ")   
          confirm = input("Confirm password: ") 
          if username not in saved_users and password==confirm:
            print (Fore.GREEN + "New account created." + Fore.WHITE)
            new_account=True
            ReturnToStart=False
            break
          elif username not in saved_users and password!=confirm:
            print (Fore.RED + "Passwords do not match. Please try again."+Fore.WHITE)
          else:
            print (Fore.RED+"Username already exists."+Fore.WHITE)    

      case _: # tells user they must enter a valid action 
        print(Fore.RED+"Invalid action. Please select 1 or 2."+Fore.WHITE)
        time.sleep(2)
        replit.clear()

  while new_account:
    print(Fore.WHITE+ " ")  
    try:
      # take balance amount from user
      balance = float(input("What is your current balance?: $")) 
      replit.clear()  
      break
    except ValueError:
      print(Fore.RED +"\nBalance must be a number, please try again.") 
    except NegativeError:
      print(Fore.RED +"\nBalance must be positive, please try again.") 

  if new_account == False:
    balance = float(account_balances[username]) # assigns previously saved balance to balance variable

  while True:
    replit.clear()
    menu()
    # takes action from user
    print("Choose an action", end=" (")
    action = input(Fore.BLUE+"1"+Fore.WHITE+", "+Fore.MAGENTA+"2"+Fore.WHITE+", "+Fore.BLACK+"3"+Fore.WHITE+", or "+Fore.CYAN+"4"+Fore.WHITE+"): ")
    replit.clear()

    match action:
      case "1": # takes valid withdrawal amount from user
        print(Fore.WHITE+"Enter 0 to go back to menu.")
        amount = withdraw_exceptions()      
        if amount !=0:
          balance = new_bal_withdraw(balance) # updates balance
          print(Fore.GREEN+"You have successfully withdrawn $"+str(format(amount,'.2f'))+". Thank you.")
          transactions.append(f"Withdrawal: ${amount:.2f}")
          delay_and_clear(2.5) 

      case "2": # takes valid deposit amount from user
        print(Fore.WHITE+"Enter 0 to go back to menu.")  
        amount = deposit_exceptions()
        if amount !=0:
          balance = new_bal_deposit(balance) # updates balance
          print(Fore.GREEN+"You have successfully deposited $"+str(format(amount,'.2f'))+". Thank you.")
          transactions.append(f"Deposit: ${amount:.2f}")
          delay_and_clear(2.5)   

      case "3": # shows user their balance
        print(Fore.WHITE+ "Your current balance is " + Fore.GREEN+"$"+str(format(balance,'.2f'))+".")
        if len(transactions) > 0: 
          print (Fore.WHITE+"\nTransactions:")
          for action in range(len(transactions)): # displays list of transactions
            print("\t"+ str(action+1)+". "+transactions[action])
        delay_and_clear(len(transactions)+2) 

      case "4": # ends program and resets to menu for next user
        print(Fore.WHITE+ "Your current balance is " + Fore.GREEN+"$"+str(format(balance, '.2f'))+".")
        if len(transactions) > 0:  
          print (Fore.WHITE+"\nTransactions:")
          for action in range(len(transactions)): # displays list of transactions
            print("\t"+str(action+1)+". "+transactions[action])
        print (Fore.WHITE+"""\nThank you for using EH Banking. Goodbye and have a great day!""")
        time.sleep(len(transactions)+6)
        f = open("accounts.txt","a")
        balance_string = str(format(balance,'.2f'))
        f.write(username+", "+password+", "+balance_string+"\n") # saves new account info in accounts file
        f.close()
        replit.clear()
        break 

      case _: # tells user they must enter a valid action 
        print(Fore.RED+"Invalid action, please try again.")
        time.sleep(2)