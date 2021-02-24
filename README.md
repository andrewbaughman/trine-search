 # trine-search
 11/1/2020

 ## Code Naming Convention
 * Python / JavaScript
   - functions: CamelCase
   - variables: lowercase_with_underscores
   - classes: CapsCase 
 * HTML / CSS:
 	 - classes: lowecase_underscores
 	 - ID's: lowecase-dashes
 * Else:
 	 - follow industry standard

  ## Helpful Commands
  * manage.py
    - 'python3 manage.py runserver' : starts the server
    - 'python3 manage.py flush' : removes all data while retaining table structures
    - 'python3 manage.py shell
      from django.contrib.auth.models import User
      user = User.objects.create_user(username='josh', password='password')
      exit()'
      :creates new user, 'josh', with password, 'password'
    - 'python3 manage.py makemigrations' run after model changes
    - 'python3 manage.py migrate' run to apply model chenges



 
 
