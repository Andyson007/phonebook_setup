import psycopg2
from json import loads

with open('./.secrets.json', 'r') as f:
  secrets = loads(f.read())

ended = False
db = psycopg2.connect(database=secrets['db'], user=secrets['user'], password=secrets['password'])

main_menu_text = '''
**********************************
**                              **
**  Phone book                  **
**  ---                         **
**  1: Add to phone book        **
**  2: Search the phone book    **
**  3: Remove phone book entry  **
**  4: Edit phone book entry    **
**  5: End session              **
**                              **
**********************************
'''

def add_to_book():
  cur = db.cursor()
  first_name = input('First name $ ')
  last_name = input('Last name $ ')
  phone_number = input('Phone number $ ')

  cur.execute('INSERT INTO people (phonenumber, firstname, lastname) VALUES (%s,%s,%s)', (phone_number, first_name, last_name))
  cur.close()

def search():
  cur = db.cursor()
  name_or_number = input('Search query $ ')
  cur.execute('SELECT phonenumber, firstname, lastname FROM people WHERE firstname = %(n)s OR phonenumber = %(n)s OR lastname = %(n)s', {'n': name_or_number})
  
  entries = cur.fetchall()

  if (len(entries) == 0): print('\nNo search results')
  else: print(f'\nSearch results for \'{name_or_number}\': ')

  for i in range(len(entries)):
    entry = entries[i]
    print(f'{(i+1): 3}. {entry[1]} {entry[2]}: {entry[0]}')
  
  cur.close()

  if len(entries) != 0: input('\nPress Enter to continue')

def remove():
  phone_number = input('Phone number $ ')
  doublecheck = input(f'Are you sure you want to remove ({phone_number}) from the phone book [y/N] $ ')
  if doublecheck in ['y', 'Y', 'yes', 'Yes', 'yeah', 'Yeah']:
    cur = db.cursor()
    # Do it
    cur.execute('DELETE FROM people WHERE phonenumber=%(number)s', {'number': phone_number})
    print(f'Removed {phone_number}')

    cur.close()

def edit():
  cur = db.cursor()
  phonenumber = input('Phone number $ ')

  cur.execute('SELECT phonenumber, firstname, lastname FROM people WHERE phonenumber=%(number)s', {'number': phonenumber})
  person_to_change = cur.fetchone()

  if not person_to_change:
    print('Phone number unrecognized.')
    return
  
  print (f'{person_to_change[1]} {person_to_change[2]}: {person_to_change[0]}')

  tochange = input('What do you want to change? (F/L/P) $ ').lower()
  changeto = input('What do you want to change it to? $ ')

  variable_to_change = None

  if tochange in ['f', 'first name', 'firstname']:
    cur.execute('UPDATE people SET firstname = %s WHERE phonenumber = %s', (changeto, phonenumber))

  if tochange in ['l', 'last name', 'lastname']:
    cur.execute('UPDATE people SET lastname = %s WHERE phonenumber = %s', (changeto, phonenumber))

  if tochange in ['p', 'phone number', 'phonenumber']:
    cur.execute('UPDATE people SET phonenumber = %s WHERE phonenumber = %s', (changeto, phonenumber))
  
  if not variable_to_change: return

  cur.close()

def main_menu():
  global ended
  while not ended:
    print(main_menu_text)
    action = input ('1-5 $ ')

    if action == '1': add_to_book()
    elif action == '2': search()
    elif action == '3': remove()
    elif action == '4': edit()
    else: ended = True
  db.commit()

if __name__ == '__main__':
  main_menu()