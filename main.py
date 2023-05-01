from nicegui import ui
from dotenv import load_dotenv
import os
from DataHandling.local_file_picker import local_file_picker
from DataHandling.CustomerDataParser import CustomerDataParser
from DataHandling.ContractorDataParser import ContractorDataParser
from MapHandling.GoogleDirections import GoogleDirections
from MapHandling.GooglePlaces import GooglePlaces

load_dotenv()

# data globals
customer_data = CustomerDataParser()
contractor_data = ContractorDataParser()
google_directions = GoogleDirections(os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_DIRECTIONS_ENDPOINT"))
google_places = GooglePlaces(os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_PLACES_ENDPOINT"))

# ui globals
customer_upload_btn = None
contractor_upload_btn = None
selector = None
names = ["No contractor data loaded!"]
map_generate_btn = None

##todo: clean this up to make it not so spaghetti

## asynchronous callbacks
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
    contractor = contractor_data.get_contractor(selected_contractor)

    # reget the customer data
    waypoints = []
    for customer in customer_data.get_all_customers():
        waypoints.append(google_places.get_place_id(customer['address']))


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

if __name__ == '__main__':
    ui.run(reload=False, title='NiceGUI', native=True, window_size=(800, 600))