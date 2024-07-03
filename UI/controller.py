import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._choiceCountry = None
        self._choiceYear = None

    def fillDD(self):
        countries = self._model.getCountries()
        for country in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(data=country, on_click=self.readDDCountry, text=country))
        for year in range(2015,2019):
            self._view.ddyear.options.append(ft.dropdown.Option(data=year, on_click=self.readDDYear, text=str(year)))
        self._view.update_page()

    def readDDCountry(self, e):
        if e.control.data is None:
            self._choiceCountry=None
        else:
            self._choiceCountry = e.control.data
        print(f"readDDCountry called -- {self._choiceCountry}")
    def readDDYear(self, e):
        if e.control.data is None:
            self._choiceYear=None
        else:
            self._choiceYear = e.control.data
        print(f"readDDYear called -- {self._choiceYear}")


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        if self._choiceCountry is None:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Selezionare una nazione")
            self._view.update_page()
            return
        if self._choiceYear is None:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Selezionare un anno")
            self._view.update_page()
            return

        self._model.buildGraph(self._choiceCountry, self._choiceYear)
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato! #{n} nodi #{a} archi"))

        self._view.update_page()


    def handle_volume(self, e):
        volumi = self._model.volumiTotali()
        for volume in volumi:
            self._view.txtOut2.controls.append(ft.Text(f"{volume[0].Retailer_name} --> {volume[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        n = self._view.txtN.value
        try:
            intN = int(n)
        except ValueError:
            self._view.create_alert("Inserire un numero intero")
            return
        if intN == "":
            self._view.create_alert("Inserire un numero")
            return
        if intN < 2:
            self._view.create_alert("Il numero inserito deve maggiore o uguale a 2")
            return

        path, score = self._model.calcolaPercorso(intN)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {score}"))
        for p in path:
            self._view.txtOut3.controls.append(ft.Text(f"{p[0].Retailer_name} --> {p[1].Retailer_name}: {p[2]}"))
        self._view.update_page()




