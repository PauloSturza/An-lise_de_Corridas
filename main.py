import dearpygui.dearpygui as dpg
from database import iniciar_banco, distancia_total_corrida, lista_tenis, lancar_corrida_db, historico_corridas

largura = 600
altura = 500

iniciar_banco()

tenis = lista_tenis()
MAPA_TENIS = {nome: id_tenis for nome, id_tenis in tenis}
TODOS_TENIS = list(MAPA_TENIS.keys())

def tela_inicial():
    dpg.configure_item('tela_inicial', show=True)
    dpg.configure_item('tela_lancamento', show=False)
    dpg.set_primary_window('tela_inicial', True)

    total_corrido = distancia_total_corrida()
    dpg.set_value("total_corrido", total_corrido )
    atualizar_tabela_interface()

def atualizar_tabela_interface():
    dpg.delete_item("container_tabela",children_only=True)
    historico = historico_corridas()
    
    if not historico:
        dpg.add_text("Não há corridas!", parent="container_tabela")
        return
    with dpg.table(
        header_row=True,
        parent="container_tabela",
        borders_innerH=True,borders_outerH=True,borders_innerV=True, borders_outerV=True
    ):
        dpg.add_table_column(label="Data")
        dpg.add_table_column(label="Tênis")
        dpg.add_table_column(label="Distância")
        dpg.add_table_column(label="Tempo")
        for data, tenis, distancia, tempo in historico:
            with dpg.table_row():
                dpg.add_text(data)
                dpg.add_text(tenis)
                dpg.add_text(distancia)
                dpg.add_text(tempo)

def tela_lancamento():
    dpg.configure_item('tela_inicial', show=False)
    dpg.configure_item('tela_lancamento', show=True)
    dpg.set_primary_window('tela_lancamento', True)

def lancar_corrida():
    tenis = dpg.get_value("tenis_usado")
    distancia = dpg.get_value("distancia")
    tempo = dpg.get_value("hora")*3600 + dpg.get_value("minuto")*60 + dpg.get_value("segundo")
    data = dpg.get_value("data")
    tenis_id = MAPA_TENIS[tenis]
    lancar_corrida_db(tenis_id, distancia, tempo, data)

dpg.create_context()

with dpg.window(label="Inicio", tag='tela_inicial', width=largura, height=altura):
    total_corrido = distancia_total_corrida()
    with dpg.group(horizontal=True):
        dpg.add_text("Distância Total")
        dpg.add_text(total_corrido, tag="total_corrido")
    dpg.add_table()
    dpg.add_group(tag="container_tabela")
    dpg.add_button(label="Lançar Corrida", callback=tela_lancamento, width=50, height=50)

with dpg.window(label="Lançamento", tag='tela_lancamento', width=largura, height=altura, show=False):
    with dpg.group(horizontal=True):
        dpg.add_text("Tênis Usado:")
        dpg.add_combo(
            items=TODOS_TENIS,
            tag='tenis_usado',
            default_value=TODOS_TENIS[0] if TODOS_TENIS[0] else "",
            width=100
        )

    dpg.add_spacer()
    with dpg.group(horizontal=True):
        dpg.add_text("Distância(m):")  
        dpg.add_input_int(tag="distancia",default_value=0,width=100)

    dpg.add_spacer()
    dpg.add_text("Tempo de Corrida:")
    with dpg.group(horizontal=True, tag="tempo"):
        dpg.add_text("Horas:")
        dpg.add_input_int(tag="hora", default_value=0,width=100)
        dpg.add_text("Minutos:")
        dpg.add_input_int(tag="minuto", default_value=0,width=100)
        dpg.add_text("Segundos:")
        dpg.add_input_int(tag="segundo", default_value=0,width=100)
    
    dpg.add_spacer()
    with dpg.group(horizontal=True):
        dpg.add_text("Data:")
        dpg.add_input_text(tag="data", default_value="YYYY-MM-DD", width=150)

    dpg.add_spacer()
    dpg.add_button(label="Lançar Corrida", callback=lancar_corrida, width=125, height=40)
    dpg.add_button(label="Início", callback=tela_inicial, width=50, height=50)

dpg.create_viewport(title='Minhas Corridas', width=largura, height=altura)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window("tela_inicial", True)
atualizar_tabela_interface()
dpg.start_dearpygui()

dpg.destroy_context()