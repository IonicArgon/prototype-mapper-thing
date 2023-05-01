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

##todo: clean this up to make it not so spaghetti

## asynchronous callbacks
##todo: make these not spaghetti
##todo: also some of this stuff should be backend
##todo: tl;dr separate ui from backend and make it not spaghetti
async def pick_file_customer() -> None:
    result = await local_file_picker('~', upper_limit='.', multiple=False)
    if result:
        status = customer_data.set_file_path(result[0])
        if status == -1:
            ui.notify('Invalid file type! Must be a .csv file!')
        elif status == 0:
            ui.notify('File loaded!')
            customer_upload_btn.props('icon=check')
    else:
        ui.notify('Cancelled!')

async def pick_file_contractor() -> None:
    global names
    result = await local_file_picker('~', upper_limit='.', multiple=False)
    if result:
        status = contractor_data.set_file_path(result[0])
        if status == -1:
            ui.notify('Invalid file type! Must be a .csv file!')
        elif status == 0:
            ui.notify('File loaded!')
            names = [contractor['name'] for contractor in contractor_data.get_all_contractors()]
            selector.options.clear()
            selector.options.extend(names)
            selector.value = None
            selector.set_enabled(True)
            contractor_upload_btn.props('icon=check')
    else:
        ui.notify('Cancelled!')

async def generate_map() -> None:
    global spinner
    status_customers = customer_data.get_all_customers()
    status_contractors = contractor_data.get_all_contractors()

    if next(status_customers) == -1:
        ui.notify('No customer data loaded!')
        return
    if next(status_contractors) == -1:
        ui.notify('No contractor data loaded!')
        return
    
    # get the selected contractor
    selected_contractor = selector.value
    if selected_contractor == None:
        ui.notify('No contractor selected!')
        return
    spinner.set_visibility(True)

    contractor = contractor_data.get_contractor(selected_contractor)
    contractor_address = google_places.get_place_id(contractor['address'])
    print(f'[DEBUG] Contractor: {contractor}')
    print(f'[DEBUG] Contractor address: {contractor_address}')

    # reget the customer data
    waypoints = []
    for customer in customer_data.get_all_customers():
        waypoints.append(google_places.get_place_id(customer['address']))
    print(f'[DEBUG] Waypoints: {waypoints}')

    # find the furthest customer from the contractor and we'll use that as the final destination
    google_distance_matrix.calculate_matrix([contractor_address], waypoints)
    furthest_customer_dist = google_distance_matrix.get_furthest_distance_row(0)
    print(f'[DEBUG] Furthest customer distance: {furthest_customer_dist}')

    # now get the optimal waypoint order
    # first pop the furthest customer from the list
    index_of_furthest_customer = google_distance_matrix.get_matrix_row(0).index(furthest_customer_dist)
    furthest_customer = waypoints[index_of_furthest_customer]
    print(f'[DEBUG] Furthest customer: {furthest_customer}')

    waypoints.pop(index_of_furthest_customer)
    # now calculate the optimal order
    waypoint_order = google_directions.get_optimized_waypoints(contractor_address, furthest_customer, waypoints)
    print(f'[DEBUG] Waypoint order: {waypoint_order}')

    # rearrange the waypoints to match the order
    new_waypoints = []
    for waypoint in waypoint_order:
        new_waypoints.append(waypoints[waypoint])
    print(f'[DEBUG] New waypoints: {new_waypoints}')

    # now we can calculate the route and generate the map
    maps_embed_url_endpoint = "https://www.google.com/maps/embed/v1/directions"
    maps_api_key = "?key=" + os.getenv("GOOGLE_API_KEY")
    maps_origin = "&origin=place_id:" + urllib.parse.quote(contractor_address)
    maps_destination = "&destination=place_id:" + urllib.parse.quote(furthest_customer)
    waypoints_placeid = "|".join("place_id:" + waypoint for waypoint in new_waypoints)
    maps_waypoints = "&waypoints=" + urllib.parse.quote(waypoints_placeid)
    maps_mode = "&mode=driving"

    maps_embed_url = maps_embed_url_endpoint + maps_api_key + maps_origin + maps_destination + maps_waypoints + maps_mode
    print(f'[DEBUG] Maps embed URL: {maps_embed_url}')

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
    print(f'[DEBUG] Map HTML content: {map_html_content}')
    map_html_object.set_content(map_html_content)
    map_html_object.update()
    
    spinner.set_visibility(False)


## (mostly) UI generation
with ui.row().classes("content-center"):
    ui.icon("drive_eta", color="#0ea5e9").classes("text-5xl")
    ui.label("Contractor Route Generator").classes("text-5xl")

with ui.row().classes("content-center"):
    customer_upload_btn = ui.button('Customer Data', on_click=pick_file_customer).props('icon=folder')
    contractor_upload_btn = ui.button('Contractor Data', on_click=pick_file_contractor).props('icon=folder')

selector = ui.select(names, label='Contractor', value=names[0]).classes('w-1/2')
selector.set_enabled(False)

map_generate_btn = ui.button('Generate Map', on_click=generate_map).classes('w-1/2')
with ui.element('div').classes('absolute bottom-0 right-0 p-1 m-1'):
    spinner = ui.spinner(size='lg')
    spinner.set_visibility(False)

map_html_object = ui.html(map_html_content)

if __name__ == '__main__':
    ui.run(reload=False, title='Contractor Route Generator', native=True, window_size=(800, 600))