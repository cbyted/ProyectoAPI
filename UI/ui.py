# import API
from API.api import consult_data 
from API.api import converto_to_dataframe
from API.api import parse_results_fields

# Textual
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Button, DataTable, Static, Select
from textual.binding import Binding

# Rich
from rich.align import Align
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich import print as rprint
from rich.text import Text

# Banner
from pyfiglet import Figlet

# others
from os import system
import time

console = Console()

class UserInterface(App):
     
    # Header Title
    TITLE = "Consultar casos positivos de COVID 19 en Colombia"

    # MAX registers a user can request
    MAX_REGISTERS = 6390000

    # This will be use in the select option
    valid_locations = [
        "Amazonas",
        "Antioquia",
        "Arauca",
        "Atlantico",
        "Bolivar",
        "Boyaca",
        "Caldas",
        "Caqueta",
        "Casanare",
        "Cauca",
        "Cesar",
        "Choco",
        "Cordoba",
        "Cundinamarca",
        "Guainia",
        "Guaviare",
        "Huila",
        "Guajira",
        "Magdalena",
        "Meta",
        "Nariño",
        "Norte Santander",
        "Putumayo",
        "Quindio",
        "Risaralda",
        "San Andres",
        "Santander",
        "Sucre",
        "Tolima",
        "Valle",
        "Vaupes",
        "Vichada",
        "Bogota"
    ]

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.location  = ""
        self.registers = 0
    
    # Layout style using custom CSS of textual
    CSS = """
    Screen {
        align: center middle;
        color: #0D1B2A;
    }

    Header {
        height: 3;
        text-style: bold;
        align: center middle;
    }
    
    #body {
        align: center middle;
        layout: horizontal;
    }

    #filter-title {
        text-style: bold;
        text-align: center;
    }

    #location {
        text-style: bold;
        margin: 3;
    }

    #limit{
        text-style: bold;
        margin: 3;
    }
    
    #confirm {
        text-style: italic;
        align: center middle;
        margin: 0 22;
        background: #262E76;
        color: white;
        border: none;
        padding: 1;
    }

    #confirm:hover {
        background: #262E96;
    }

    #sidebar {  
        width: 40%;
        border: round #777FF6;
        color: #E0E1DD;
        background:  #1B263B;
        align: center middle;
        padding: 3;
    }

    #main {
        background: #1B263B;
        border: round #777FF6;
        color: #E0E1DD;
        width: 100%;
        padding: 1 8;
    }
    
    #table {
        width: 92;
        margin: 0 1;
        background: #393939;
        text-style: bold;
        align: center middle;
        scrollbar-size-vertical: 0;
    }

    DataTable > .datatable--body {
       text-align: center;
    }
    """
      #align: center top;
    def compose(self) -> ComposeResult:
        yield Header()      

        # Divide screen in two
        with Horizontal(id="body"):
            # --- User input part
            with Vertical(id="sidebar"):
                self.static = Static(
                    "PARÁMETROS DE BUSQUEDA", id="filter-title"
                )
                yield self.static
                
                self.location = Select([(location, location) for location in self.valid_locations], value="Risaralda", id="location") 
                yield self.location

                self.registers = Input(placeholder="Límite", type="integer", tooltip="Error, Ingrese un número", id="limit")
                yield self.registers

                self.confirm = Button("Consultar registros", id="confirm") 
                yield self.confirm

            # --- Results table part
            with Vertical(id="main"):
                self.datatable = DataTable(id="table", zebra_stripes=True)
                yield self.datatable

        yield Footer()

    def on_mount(self):
        table = self.query_one("#table", DataTable)
        table.expand = True

        table.add_column(Text("Departamento", justify="center"), width=15)
        table.add_column(Text("Ciudad", justify="center"), width=15)
        table.add_column(Text("Ubicación", justify="center"), width=15)
        table.add_column(Text("Edad", justify="center"), width=15)
        table.add_column(Text("Tipo", justify="center"), width=10)
        table.add_column(Text("Estado", justify="center"), width=10)


    def on_button_pressed(self, event):
        if event.button.id == "confirm":
            location_widget = self.query_one("#location", Select).value

            if location_widget is Select.NULL:
                self.notify("[!] Campo obligatorio")
                return

            self.location = (location_widget).upper()

            registers_widget = self.query_one("#limit", Input)
            self.registers = registers_widget.value

            # Check for blank input or numbers less and equal than cero 
            if (self.registers == '') or (int(self.registers) <= 0):
                self.notify("[!] Error. El valor ingresado no es válido")
                return

            # Limit the number o requests a user can make
            if (int(self.registers) > self.MAX_REGISTERS):
                self.notify("[!] El valor ingresado supera el máximo permitido")
                return
            

            table = self.query_one("#table", DataTable)
            table.clear()

            results = consult_data(self.client, location=self.location, registers=self.registers)
            results = converto_to_dataframe(results)
            results = parse_results_fields(results)

            # here we will print the results
            for _, item in results.iterrows():
                table.add_row(
                    Text(str(item["departamento_nom"]), justify="center"),
                    Text(str(item["ciudad_municipio_nom"]), justify="center"),
                    Text(str(item["ubicacion"]), justify="center"),
                    Text(str(item["edad"]), justify="center"),
                    Text(str(item["estado"]), justify="center"),
                    Text(str(item["tipo_recuperacion"]), justify="center"),
                )
  
# Wellcome banner
def banner():
    print("\n")
    text_font = Figlet(font='slant')
    text = (text_font.renderText("Casos de covid"))

    rprint(Align.center(text))

    progress = Progress(
        TextColumn("[progress.description]{task.description}", justify="center"),
        BarColumn(bar_width=None), 
        "[progress.percentage]{task.percentage:>3.0f}%",
        expand=True 
    )

    with progress:
        loading = progress.add_task("[cyan]Iniciando ....[/cyan]", total=1000)
        while not progress.finished:
            progress.update(loading, advance=40)
            time.sleep(0.1)

    system('clear')
