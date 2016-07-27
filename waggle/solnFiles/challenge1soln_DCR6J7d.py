# make any necessary imports?

# setup env for testing user code
my_list = [10,20,30,40]

#challenge is to pull 3rd elem of list and store result in 'answer'
answer = ''


USERCODE



solution = my_list[2]
if solution == answer:
    print('CORRECT. Good job!')
elif answer == '':
    print('Make sure to put your solution in the variable \'answer\'')
elif answer == my_list[1]:
    print('Your answer gave the incorrect solution. We got the 2nd element in the list instead of the 3rd.')
elif answer == my_list[3]:
    print('Your answer gave the incorrect solution. We got the 4th element in the list instead of the 3rd.')
else:
    print('The answer you submitted was incorrect. Try again and if you need help send the instructor a message.')
