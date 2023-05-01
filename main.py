from nicegui import ui
from dotenv import load_dotenv
import urllib.parse
import os
from DataHandling.local_file_picker import local_file_picker
from DataHandling.CustomerDataParser import CustomerDataParser
from DataHandling.ContractorDataParser import ContractorDataParser
from MapHandling.GoogleDirections import GoogleDirections
from MapHandling.GooglePlaces import GooglePlaces
from MapHandling.GoogleDistanceMatrix import GoogleDistanceMatrix

load_dotenv()

# data globals
customer_data = CustomerDataParser()
contractor_data = ContractorDataParser()
google_directions = GoogleDirections(os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_DIRECTIONS_ENDPOINT"))
google_places = GooglePlaces(os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_PLACES_ENDPOINT"))
google_distance_matrix = GoogleDistanceMatrix(os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_DISTANCE_MATRIX_ENDPOINT"))

# ui globals
customer_upload_btn = None
contractor_upload_btn = None
selector = None
names = ["No contractor data loaded!"]
map_generate_btn = None
spinner = None
map_html_content = '''
<div>
    No map has been generated.
</div>
'''
map_html_object = None
weekday_selector = None

##todo: clean this up to make it not so spaghetti

## asynchronous callbacks
##todo: make these not spaghetti
##todo: also some of this stuff should be backend
##todo: tl;dr separate ui from backend and make it not spaghetti
async def pick_file_customer() -> None:
    result = await local_file_picker('~', upper_limit='.', multiple=False)
    if result:
        status = None
        try:
            status = customer_data.set_file_path(result[0])
        except:
            ui.notify('An error has occured!', icon='error')

        if status == -1:
            ui.notify('Invalid file type! Must be a .csv file!', icon='error')
        elif status == 0:
            ui.notify('File loaded!', icon='done')
            customer_upload_btn.props('icon=done')
    else:
        ui.notify('Cancelled!', icon='error')

async def pick_file_contractor() -> None:
    global names
    result = await local_file_picker('~', upper_limit='.', multiple=False)
    if result:
        status = None
        try:
            status = contractor_data.set_file_path(result[0])
        except:
            ui.notify('An error has occured!', icon='error')
        
        if status == -1:
            ui.notify('Invalid file type! Must be a .csv file!', icon='error')
        elif status == 0:
            ui.notify('File loaded!', icon='done')
            names = [contractor['name'] for contractor in contractor_data.get_all_contractors()]
            selector.options.clear()
            selector.options.extend(names)
            selector.value = None
            selector.set_enabled(True)
            contractor_upload_btn.props('icon=done')
    else:
        ui.notify('Cancelled!', icon='error')

async def generate_map() -> None:
    global spinner
    status_customers = customer_data.get_all_customers()
    status_contractors = contractor_data.get_all_contractors()

    if next(status_customers) == -1:
        ui.notify('No customer data loaded!', icon='error')
        return
    if next(status_contractors) == -1:
        ui.notify('No contractor data loaded!', icon='error')
        return
    
    # get the selected contractor
    selected_contractor = selector.value
    if selected_contractor == None:
        ui.notify('No contractor selected!', icon='error')
        return

    contractor = contractor_data.get_contractor(selected_contractor)
    contractor_address = google_places.get_place_id(contractor['address'])
    contractor_regions = contractor['regions']
    contractor_weekdays = contractor['available']

    if weekday_selector.value not in contractor_weekdays:
        ui.notify('Contractor is not available on the selected weekday!', icon='error')
        return

    # filter out customers that are not in the contractor's regions
    customer_list = [customer for customer in customer_data.get_all_customers()]
    for i in range(len(customer_list)):
        customer = customer_list[i]
        if customer['region'] not in contractor_regions:
            customer_list[i] = None

    # also filter out customers that are not available on the selected weekday
    if weekday_selector.value == None:
        ui.notify('No weekday selected!', icon='error')
        return
    for i in range(len(customer_list)):
        customer = customer_list[i]
        if customer != None:
            if weekday_selector.value not in customer['weekdays']:
                customer_list[i] = None

    # remove all the None values from the list then check if the list is empty
    customer_list = [customer for customer in customer_list if customer != None]
    if len(customer_list) == 0:
        ui.notify('No customers available on the selected weekday!', icon='error')
        return

    # reget the customer data
    waypoints = []
    for customer in customer_list:
        waypoints.append(google_places.get_place_id(customer['address']))

    spinner.set_visibility(True)
    spinner.update()

    # find the furthest customer from the contractor and we'll use that as the final destination
    google_distance_matrix.calculate_matrix([contractor_address], waypoints)
    furthest_customer_dist = google_distance_matrix.get_furthest_distance_row(0)

    # now get the optimal waypoint order
    # first pop the furthest customer from the list
    index_of_furthest_customer = google_distance_matrix.get_matrix_row(0).index(furthest_customer_dist)
    furthest_customer = waypoints[index_of_furthest_customer]

    waypoints.pop(index_of_furthest_customer)
    # now calculate the optimal order
    waypoint_order = google_directions.get_optimized_waypoints(contractor_address, furthest_customer, waypoints)

    # rearrange the waypoints to match the order
    new_waypoints = []
    for waypoint in waypoint_order:
        new_waypoints.append(waypoints[waypoint])

    # now we can calculate the route and generate the map
    maps_embed_url_endpoint = "https://www.google.com/maps/embed/v1/directions"
    maps_api_key = "?key=" + os.getenv("GOOGLE_API_KEY")
    maps_origin = "&origin=place_id:" + urllib.parse.quote(contractor_address)
    maps_destination = "&destination=place_id:" + urllib.parse.quote(furthest_customer)

    maps_waypoints = ""
    if len(new_waypoints) > 0:
        waypoints_placeid = "|".join("place_id:" + waypoint for waypoint in new_waypoints)
        maps_waypoints = "&waypoints=" + urllib.parse.quote(waypoints_placeid)
    maps_mode = "&mode=driving"

    maps_embed_url = maps_embed_url_endpoint + maps_api_key + maps_origin + maps_destination + maps_mode
    maps_embed_url += maps_waypoints if len(new_waypoints) > 0 else ""

    global map_html_content
    global map_html_object
    map_html_content = f'''
    <div class='w-auto aspect-square border border-solid rounded-md'>
        <iframe
            width="100%"
            height="100%"
            frameborder="0" style="border:0"
            src="{maps_embed_url}"
            allowfullscreen>
        </iframe>
    </div>
    '''
    map_html_object.set_content(map_html_content)
    map_html_object.update()
    
    spinner.set_visibility(False)
    spinner.update()

    ui.notify('Map generated!', icon='done')


## (mostly) UI generation
with ui.row().classes("content-center"):
    ui.icon("drive_eta", color="#0ea5e9").classes("text-5xl")
    ui.label("Contractor Route Generator").classes("text-5xl")

with ui.row().classes("content-center w-3/4 place-content-evenly"):
    customer_upload_btn = ui.button('Customer Data', on_click=pick_file_customer).props('icon=folder')
    contractor_upload_btn = ui.button('Contractor Data', on_click=pick_file_contractor).props('icon=folder')

selector = ui.select(names, label='Contractor', value=names[0]).classes('w-3/4')
selector.set_enabled(False)

weekday_selector = ui.toggle({
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun'
}).classes('w-3/4 place-content-evenly')

map_generate_btn = ui.button('Generate Map', on_click=generate_map).classes('w-3/4')
with ui.element('div').classes('absolute bottom-0 right-0 p-1 m-1'):
    spinner = ui.spinner(size='lg')
    spinner.set_visibility(False)

map_html_object = ui.html(map_html_content)

if __name__ == '__main__':
    ui.run(reload=False, title='Contractor Route Generator', native=True, window_size=(800, 800))