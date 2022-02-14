from pathlib import PurePath
import PySimpleGUI as sg
import do_resquests as request

# sg.theme("DarkTeal2")
list_sites = ["MLA", "MLB", "MLC", "MLU", "MLM", "MCO", "MPY", "MLV",
              "MBO", "MCR", "MEC", "MGT", "MHN", "MNI", "MPA", "MPE", "MRD", "MSV"]
list_logistic = ["drop_off", "xd_drop_off", "cross_docking"]
list_actions = ["Backup", "Rollback"]

layout = [
    [sg.Text("Select File: "),
     sg.Input(key="-IN2-", readonly=True),
     sg.FileBrowse(
         key="-IN-", file_types=(("csv files", "*.csv"), ("txt files", "*.txt"),("all files", "*.*")))
     #  sg.Radio("Backup", "RADIO1", key='-bak-', default=True),
     #  sg.Radio("Rollback", "RADIO1", key='-roll-', default=False)
     ],
    [sg.Text("Site: "),
     sg.Combo(list_sites, size=(6, 1), key="site", readonly=True),
     #  sg.Input(key="-site-",size=(4,0)),
     sg.Text("Logistic type: "),
     sg.Combo(list_logistic, auto_size_text=True,
              key="log_type", readonly=True),
     sg.Text("Opcion: "),
     sg.Combo(list_actions, auto_size_text=True, key="action", readonly=True)
     ],
    [sg.Button('Ok'),  sg.Button('Cancel')]]

window = sg.Window('Handling Time Backup/Rollback', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Cancel":
        break

    # sin seleccion de archivo csv
    elif event == "Ok" and values["-IN2-"] == "":
        sg.popup('Elegi un archivo')

    # seleccion Backup
    elif event == "Ok" and values["action"] == "Backup" and values["site"] != "" and values["log_type"] != "":
        file_csv_name = PurePath(values["-IN2-"])
        print("El site es "+values["site"] +
              " logistic type "+values["log_type"]+" y se va hacer un  " + values["action"])
        if sg.popup_ok_cancel("Esta por realizar un "+values["action"]+" en el site "+values["site"] +
                           " con la logistic type "+values["log_type"]+" ¿Son correctos los datos? ") == "OK":
            try:
                request.get_backup(values["site"], values["log_type"], file_csv_name)
                sg.popup_ok("Se pudo realizar el backup, controlar la carpeta donde esta el ejecutable por el archivo txt")
                window["-IN2-"].update([])
                window["action"].update("")
                window["site"].update("")
                window["log_type"].update("")
            except Exception as e:
                 sg.popup_error(f"NOK - Algo salio mal: {e}")
                #  print(f"NOK - Algo salio mal: {e}")
   
   #seleccion Rollback
    elif event == "Ok" and values["action"] == "Rollback" and values["site"] != "" and values["log_type"] != "":
        file_csv_name = PurePath(values["-IN2-"])
        print("El site es "+values["site"] +
              " logistic type "+values["log_type"]+" y se va hacer un  " + values["action"])
        if sg.popup_ok_cancel("Esta por realizar un "+values["action"]+" en el site "+values["site"] +
                           " con la logistic type "+values["log_type"]+" ¿Son correctos los datos? ") == "OK":
            try:
                request.post_backup(values["site"], values["log_type"], file_csv_name)
                sg.popup_ok("Se pudo realizar el rollback")
                window["-IN2-"].update([])
                window["action"].update("")
                window["site"].update("")
                window["log_type"].update("")
            except Exception as e:
               sg.popup_error(f"NOK - Algo salio mal: {e}")

    # sin seleccion de Site y Log type
    elif event == "Ok" and values["site"] == "" or values["log_type"] == "" or values["action"] == "":
        sg.popup('Site, Logistic y Opcion no pueden estar vacios')
