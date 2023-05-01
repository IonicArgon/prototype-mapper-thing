from nicegui import ui
from DataHandling.local_file_picker import local_file_picker
from DataHandling.CustomerDataParser import CustomerDataParser
from DataHandling.ContractorDataParser import ContractorDataParser
from MapHandling.GoogleDirections import GoogleDirections
from MapHandling.GooglePlaces import GooglePlaces

customer_data = CustomerDataParser()
contractor_data = ContractorDataParser()

with ui.row().classes("content-center"):
    ui.icon("drive_eta", color="#0ea5e9").classes("text-5xl")
    ui.label("Contractor Route Generator").classes("text-5xl")

# ui globals
contractor_upload_btn = None
selector = None
names = ["No contractor data loaded!"]

##todo: clean this up to make it not so spaghetti

async def pick_file_customer() -> None:
    result = await local_file_picker('~', upper_limit='.', multiple=False)
    if result:
        status = customer_data.set_file_path(result[0])
        if status == -1:
            ui.notify('Invalid file type! Must be a .csv file!')
        elif status == 0:
            ui.notify('File loaded!')
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
    else:
        ui.notify('Cancelled!')

with ui.row().classes("content-center"):
    ui.button('Customer Data', on_click=pick_file_customer).props('icon=folder')
    contractor_upload_btn = ui.button('Contractor Data', on_click=pick_file_contractor).props('icon=folder')

selector = ui.select(names, label='Contractor', value=names[0]).classes('w-1/2')
selector.set_enabled(False)

if __name__ == '__main__':
    ui.run(reload=False, title='NiceGUI', native=True, window_size=(800, 600))