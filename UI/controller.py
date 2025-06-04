import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        store_id=self._view._ddStore.value
        if store_id is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un id!", color="red"))
            return

        self._model.buildGraph(int(store_id))
        nodi, archi=self._model.getGraphDetails()

        if nodi!=0:
            self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato: "))
            self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nodi} "))
            self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {archi} "))

        self._view.update_page()



    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass

    def fillDD(self):
        stores=self._model.getAllStores()
        options=map(lambda x:ft.dropdown.Option(x), stores)
        self._view._ddStore.options=options