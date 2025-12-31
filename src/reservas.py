from typing import NamedTuple
from datetime import date, datetime
import csv
from collections import defaultdict, Counter


Reserva = NamedTuple("Reserva", 
                     [("nombre", str),
                      ("dni", str),
                      ("fecha_entrada", date),
                      ("fecha_salida", date),
                      ("tipo_habitacion", str),
                      ("num_personas", int),
                      ("precio_noche", float),
                      ("servicios_adicionales", list[str])
                    ])


#Ana Fernández,98762912S,2022-01-02,2022-01-06,Suite,4,202.97,"Parking,Gimnasio,Spa"


def lee_reservas(ruta_fichero:str)-> list[Reserva]:
    res  = []
    with open(ruta_fichero, encoding = 'utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for e in lector:
            nombre = e[0].strip()
            dni = e[1].strip()
            fecha_entrada = datetime.strptime(e[2], "%Y-%m-%d").date()
            fecha_salida = datetime.strptime(e[3], "%Y-%m-%d").date()
            tipo_habitacion = e[4].strip()
            num_personas = int(e[5])
            precio_noche = float(e[6])
            servicios_adicionales = e[7].split(',')
            res.append(Reserva(nombre, dni, fecha_entrada, fecha_salida, tipo_habitacion, num_personas, precio_noche, servicios_adicionales))
    return res    


def total_facturado(reservas: list[Reserva], 
                    fecha_ini: date | None = None, 
                    fecha_fin: date | None = None) -> float:
    res = 0
    for reserva in reservas:
        if (fecha_ini is None and fecha_fin is None) or (fecha_ini is None and fecha_fin>=reserva.fecha_entrada) or \
        (fecha_fin is None and fecha_ini <= reserva.fecha_entrada) or (fecha_ini is not None and fecha_fin is not None 
                                                                      and fecha_ini <= reserva.fecha_entrada and fecha_fin >= reserva.fecha_entrada):
            res += (reserva.fecha_salida - reserva.fecha_entrada).days * reserva.precio_noche
    return res        


def reservas_mas_largas(reservas: list[Reserva], n: int = 3) -> list[tuple[str, date]]:
    lista_ordenada = sorted(reservas, key = lambda x: (x.fecha_salida - x.fecha_entrada).days, reverse = True)[:n]
    res = [(reserva.nombre, reserva.fecha_entrada) for reserva in lista_ordenada]
    return res

def cliente_mayor_facturacion(reservas: list[Reserva], 
                              servicios: set[str] | None = None) -> tuple[str, float]:
    dict_auxiliar = dict()
    for reserva in reservas:
        if servicios is None or set(reserva.servicios_adicionales) & servicios:
            if reserva.dni in dict_auxiliar:
                dict_auxiliar[reserva.dni] += (reserva.fecha_salida - reserva.fecha_entrada).days * reserva.precio_noche
            else:
                dict_auxiliar[reserva.dni] = (reserva.fecha_salida - reserva.fecha_entrada).days * reserva.precio_noche
    cliente_maximo = max(dict_auxiliar.items(), key = lambda x: x[1])
    return cliente_maximo

def servicios_estrella_por_mes(reservas: list[Reserva], 
                               tipos_habitacion: set[str] | None = None
                               ) -> dict[str, str]:
    dict_auxiliar = defaultdict(list)
    res = dict()
    for reserva in reservas:
        if tipos_habitacion is None or reserva.tipo_habitacion in tipos_habitacion:
            m = reserva.fecha_entrada.month
            mes = parsea_meses(m)
            for servicio in reserva.servicios_adicionales:
                dict_auxiliar[mes].append(servicio)
    for clave in dict_auxiliar:
        c = Counter(dict_auxiliar[clave])
        res[clave] = c.most_common(1)[0][0]
    return res                   
                 



def parsea_meses(mes:int)->str:
    MESES = {1: "Enero",
             2: "Ferbrero",
             3 : "Marzo",
             4 : "Abril",
             5: "Mayo",
             6: "Junio",
             7:"Julio",
             8:"Agosto",
             9: "Septiembre",
             10:"Octubre",
             11 : "Noviembre",
             12:"Diciembre" 
    }
    return MESES[mes]

def media_dias_entre_reservas(reservas: list[Reserva]) -> float:
    fe = []
    tiempo = 0
    reservas_ordenadas = sorted(reservas, key = lambda x:x.fecha_entrada)
    for reserva in reservas_ordenadas:
        fe.append(reserva.fecha_entrada)
    for i in range(len(fe)-1):
        tiempo += ((fe[i+1]-fe[i]).days)
    return tiempo/(len(fe)-1)    


def cliente_reservas_mas_seguidas(reservas: list[Reserva], min_reservas: int) -> str:
    dict_auxiliar = defaultdict(list)
    dict_tiempo = dict()
    for reserva in reservas:
        dict_auxiliar[reserva.dni].append(reserva)
    for dni in dict_auxiliar:
        if len(dict_auxiliar[dni]) >= min_reservas:
            dict_tiempo[dni] = media_dias_entre_reservas(dict_auxiliar[dni])
    return min(dict_tiempo.items(), key = lambda x:x[1])[0] 

def cliente_reservas_mas_seguidas1(reservas: list[Reserva], min_reservas: int) -> float:
    dict_auxiliar = defaultdict(list)
    dict_tiempo = dict()
    for reserva in reservas:
        dict_auxiliar[reserva.dni].append(reserva)
    for dni in dict_auxiliar:
        if len(dict_auxiliar[dni]) >= min_reservas:
            dict_tiempo[dni] = media_dias_entre_reservas(dict_auxiliar[dni])
    return min(dict_tiempo.items(), key = lambda x:x[1])[1]       