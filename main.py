import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    txt_tipo = ft.TextField(label = "Tipo strumento")
    txt_marca = ft.TextField(label = "Marca")
    txt_anno = ft.TextField(label = "Anno di acquisto")
    valore_corrente = 0.0
    txt_valore = ft.TextField(value = str(valore_corrente), label = "Valore ($)", width = 120, text_align = ft.TextAlign.CENTER)

    # come diminuire il valore impostato dello strumento
    def diminuire_valore_strumento(e):
        nonlocal valore_corrente
        if valore_corrente >= 10:
            valore_corrente -= 10.0
            txt_valore.value = str(valore_corrente)
            page.update()

    # come aumentare il valore impostato dello strumento
    def aumentare_valore_strumento(e):
        nonlocal valore_corrente
        valore_corrente += 10.0
        txt_valore.value = str(valore_corrente)
        page.update()

    # creo bottoni per aumentare e diminuire il valore
    botton_meno = ft.ElevatedButton("-", on_click=diminuire_valore_strumento)
    botton_piu = ft.ElevatedButton("+", on_click=aumentare_valore_strumento)
    riga_contatore = ft.Row([ft.Text("Valore ($)"), botton_meno, txt_valore, botton_piu], alignment = ft.Alignment.START)


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def handle_aggiungi_strumento(e):
        tipo = txt_tipo.value.rstrip()
        marca = txt_marca.value.rstrip()
        anno_str = txt_anno.value.rstrip()
        valore_str = txt_valore.value

        # controllo che lo strumento inserito abbia tutti i campi
        if not tipo or not marca or not anno_str or not valore_str:
            alert.show_alert("Errore: tutti i campi devono essere inseriti")

        else:
            # controllo che l'anno di acquisto inserito abbia un valore valido
            try:
                anno_acquisto = float(anno_str)
                if anno_acquisto < 0:
                    alert.show_alert("L'anno inserito non è un numero intero positivo")
            except ValueError:
                alert.show_alert("L'anno inserito non è un numero intero positivo")
                return
            # controllo che il valore dello strumento abbia un valore valido
            try:
                valore_strumento = float(valore_str)
                if valore_strumento < 0:
                    alert.show_alert("L'anno inserito non è un numero intero positivo")
            except ValueError:
                alert.show_alert("L'anno inserito non è un numero intero positivo")
                return

            # aggiungo lo strumento inserito al deposito strumenti
            try:
                deposito.aggiungi_strumento(tipo, marca, anno_acquisto, valore_strumento)
            except Exception as e:
                alert.show_alert(f"Errore: {e}")
                return

        # resetto lo strumento inserito per consentire l'inserimento di un altro
        txt_tipo.value = ""
        txt_marca.value = ""
        txt_anno.value = ""
        nonlocal valore_corrente
        valore_corrente = 0.0
        txt_valore.value = str(valore_corrente)

        # aggiorno lista corrente
        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiunta_strumento = ft.Button("Aggiungi strumento", on_click = handle_aggiungi_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size = 20),
        txt_tipo,
        txt_marca,
        txt_anno,
        riga_contatore,
        pulsante_aggiunta_strumento,


        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
