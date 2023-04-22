from bookticket.models.helpers import Controller
from bookticket.models.ticketerror import TicketError

controller = Controller()
while True:
    print('0 - Exit')
    print('1 - Route list')
    print('2 - Buy ticket')
    print('3 - Free tickets')

    choice = input()
    try:
        if choice == '0':
            break
        elif choice == '1':
            controller.show_routes()
        elif choice == '2':
            controller.show_routes()
            route_id = input('Enter the route number: ')
            controller.show_free_tickets(int(route_id))
        elif choice == '3':
            controller.search_routes()
    except TicketError as e:
        print (e)

