from nicegui import ui
from DataHandling.local_file_picker import local_file_picker
from DataHandling.CustomerDataParser import CustomerDataParser
from DataHandling.ContractorDataParser import ContractorDataParser

customer_data = CustomerDataParser()


with ui.row().classes("content-center"):
    ui.icon("drive_eta", color="#0ea5e9").classes("text-5xl")
    ui.label("Contractor Route Generator").classes("text-5xl")

async def pick_file() -> None:
    result = await local_file_picker('~', upper_limit='.', multiple=False)
    if result:
        status = customer_data.set_file_path(result[0])
        if status == -1:
            ui.notify('Invalid file type! Must be a .csv file!')
        elif status == 0:
            ui.notify('File loaded!')
    else:
        ui.notify('Cancelled!')

with ui.row().classes("content-center"):
    ui.button('Customer Data', on_click=pick_file).props('icon=folder')


if __name__ == '__main__':
    ui.run(reload=False, title='NiceGUI', native=True, window_size=(800, 600))