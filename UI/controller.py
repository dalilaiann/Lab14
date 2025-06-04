import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._source=None



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

        options=list(map(lambda n: ft.dropdown.Option(key=str(n), data=n, on_click=self.handledd), self._model._graph.nodes))

        self._view._ddNode.options=options
        self._view._btnRicorsione.disabled=False
        self._view._btnCerca.disabled=False
        self._view.update_page()

    def handledd(self, e):
        if e.control.data is not None:
            self._source=e.control.data


    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        self._view._ddNode.options.clear()
        source=self._source
        if source is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un nodo!", color="red"))
            return

        longPath=self._model.getLongestPath(source)
        if len(longPath)==0:
            self._view.txt_result.controls.append(ft.Text("Il nodo selezionato è isolato"))
            return

        self._view.txt_result.controls.append(ft.Text(f"Nodo selezionato: {source}"))
        for n in longPath:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()


    def handleRicorsione(self, e):
        self._view.txt_result.controls.clear()
        self._view._ddNode.options.clear()
        source = self._source
        if source is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un nodo!", color="red"))
            return

        optPath, cost=self._model.getOptPath(source)
        if len(optPath)==0:
            self._view.txt_result.controls.append(ft.Text("Il nodo selezionato è isolato"))
            return

        self._view.txt_result.controls.append(ft.Text(f"Il cammino ottimo per il nodo {source} ha costo {cost}"))
        for n in optPath:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()


    def fillDD(self):
        stores=self._model.getAllStores()
        options=list(map(lambda x:ft.dropdown.Option(x), stores))
        self._view._ddStore.options=options
        self._view.update_page()