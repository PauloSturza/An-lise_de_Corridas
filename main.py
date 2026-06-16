import dearpygui.dearpygui as dpg
from database import iniciar_banco, distancia_total_corrida, lista_tenis, lancar_corrida_db, historico_corridas, total_corrido_tenis, excluir_corrida_db, editar_corrida_db

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
    atualizar_tabela_pagina_inicial()

def atualizar_tabela_pagina_inicial():
    dpg.delete_item("container_tabela_tenis",children_only=True)
    total_tenis = total_corrido_tenis()
    
    if not total_tenis:
        dpg.add_text("Não há tenis cadastrados!", parent="container_tabela_tenis")
        return
    
    dpg.add_text("Total corrido por tênis", parent="container_tabela_tenis")
    with dpg.table(
        header_row=True,
        parent="container_tabela_tenis",
        borders_innerH=True,borders_outerH=True,borders_innerV=True, borders_outerV=True
    ):
        dpg.add_table_column(label="Tênis")
        dpg.add_table_column(label="Distância Total")
        dpg.add_table_column(label="Tempo Total")
        for tenis, distancia, tempo in total_tenis:
            with dpg.table_row():
                dpg.add_text(tenis)
                dpg.add_text(distancia)
                dpg.add_text(tempo)

def atualizar_tabela_corridas():
    dpg.delete_item("container_tabela_corridas",children_only=True)
    historico = historico_corridas()
    if not historico:
        dpg.add_text("Não há corridas!", parent="container_tabela_corridas")
        return
    
    dpg.add_spacer(parent="container_tabela_corridas")
    dpg.add_spacer(parent="container_tabela_corridas")
    dpg.add_spacer(parent="container_tabela_corridas")
    dpg.add_text("Tabela de Corridas", parent="container_tabela_corridas")
    with dpg.table(
        header_row=True,
        parent="container_tabela_corridas",
        borders_innerH=True,borders_outerH=True,borders_innerV=True, borders_outerV=True
        ):
        dpg.add_table_column(label="Data")
        dpg.add_table_column(label="Tênis")
        dpg.add_table_column(label="Distância")
        dpg.add_table_column(label="Tempo")
        for id, data, tenis, distancia, tempo in historico:
            with dpg.table_row():
                linha_clicavel = dpg.add_selectable(label=data, span_columns=True, tag=id)
                tag_popup = f"popup_{id}"
                if dpg.does_alias_exist(tag_popup):
                    dpg.delete_item(tag_popup)
                with dpg.popup(parent=linha_clicavel, mousebutton=dpg.mvMouseButton_Right, tag=tag_popup):
                    dpg.add_text("Edição Rápida")
                    dpg.add_separator()

                    dpg.add_input_text(label="Data", default_value=data, tag=f"edit_data_{id}")
                    dpg.add_input_text(label="Tenis", default_value=tenis, tag=f"edit_tenis_{id}")
                    dpg.add_input_text(label="Distancia", default_value=distancia, tag=f"edit_distancia_{id}")
                    dpg.add_input_text(label="Tempo", default_value=tempo, tag=f"edit_tempo_{id}")
                    dpg.add_menu_item(label="Salvar", callback=editar_corrida, user_data=id)
                    dpg.add_menu_item(label="Excluir", callback=excluir_corrida, user_data=id)
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
    dia = dpg.get_value("dia")
    mes = dpg.get_value("mes")
    ano = dpg.get_value("ano")
    mes_str = str(mes)
    mes_str = "0" + mes_str if len (mes_str) == 1 else mes_str
    dia_str = str(dia)
    dia_str = "0" + dia_str if len (dia_str) == 1 else dia_str
    tenis_id = MAPA_TENIS[tenis]
    lancar_corrida_db(tenis_id, distancia, tempo, str(ano) + "-" + mes_str + "-" + dia_str)
    atualizar_tabela_corridas()

def formata_data(data):
    # yyyy-mm-dd --> dd/mm/yyyy
    data_formatada = data[-2:] + "/" + data[5:7] + "/" + data[0:4]
    return data_formatada

def editar_corrida(sender, app_data, user_data):
    id = user_data
    nova_data = dpg.get_value(f"edit_data_{id}")
    novo_tenis = dpg.get_value(f"edit_tenis_{id}")
    nova_distancia = dpg.get_value(f"edit_distancia_{id}")
    novo_tempo = dpg.get_value(f"edit_tempo_{id}")

    editar_corrida_db(id, nova_data, novo_tenis, nova_distancia, novo_tempo)
    atualizar_tabela_corridas()

def excluir_corrida(sender, app_data, user_data):
    excluir_corrida_db(user_data)
    atualizar_tabela_corridas()

def centralizar_janela(tag_janela):
    largura_janela = dpg.get_item_width(tag_janela)
    altura_janela = dpg.get_item_height(tag_janela)

    largura_tela = dpg.get_viewport_width()
    altura_tela = dpg.get_viewport_height()

    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)

    dpg.set_item_pos(tag_janela, [pos_x, pos_y])

dpg.create_context()

with dpg.window(label="Inicio", tag='tela_inicial', width=largura, height=altura):
    total_corrido = distancia_total_corrida()
    with dpg.group(horizontal=True):
        dpg.add_text("Distância Total")
        dpg.add_text(total_corrido, tag="total_corrido")
    dpg.add_table()
    dpg.add_group(tag="container_tabela_tenis")
    dpg.add_button(label="Corridas", callback=tela_lancamento, width=125, height=40)

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
        dpg.add_input_int(tag="hora", default_value=0, width=50, step=0)
        dpg.add_text("Minutos:")
        dpg.add_input_int(tag="minuto", default_value=0, width=50, step=0)
        dpg.add_text("Segundos:")
        dpg.add_input_int(tag="segundo", default_value=0, width=50, step=0)
    
    dpg.add_spacer()
    dpg.add_text("Data:")
    with dpg.group(horizontal=True):
        dpg.add_text("Dia:")
        dpg.add_input_int(tag="dia", width=50, step=0)
        dpg.add_text("Mês:")
        dpg.add_input_int(tag="mes", width=50, step=0)
        dpg.add_text("Ano:")
        dpg.add_input_int(tag="ano", width=50, step=0)
    
    dpg.add_button(label="Lançar Corrida", callback=lancar_corrida, width=125, height=40)
    dpg.add_group(tag="container_tabela_corridas")
    atualizar_tabela_corridas()
    dpg.add_spacer()
    dpg.add_button(label="Início", callback=tela_inicial, width=50, height=50)

dpg.create_viewport(title='Minhas Corridas', width=largura, height=altura)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window("tela_inicial", True)
atualizar_tabela_pagina_inicial()
dpg.start_dearpygui()

dpg.destroy_context()