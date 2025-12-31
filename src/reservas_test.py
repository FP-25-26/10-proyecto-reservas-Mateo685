from reservas import *

def test_lee_reservas(ruta_fichero):
    print("Test lee_reservas")
    l = lee_reservas(ruta_fichero)
    print(f"Total reservas: {len(l)}")
    print(f"Las tres primeras:\n {l[:3]}")

def test_total_facturado(reservas):
    print("Test total_facturado")
    print(f"En todo el periodo de datos{total_facturado(reservas)}")
    print(f"Desde 1 de febrero de 2022 hasta 28 de febrero de 2022: {total_facturado(reservas,datetime(2022, 2, 1).date(),datetime(2022, 2, 28).date())}")
    print(f"Desde 1 de febrero de 2022 (fecha final None):{total_facturado(reservas,datetime(2022, 2, 1).date())}")
    print(f"Hasta 28 de febrero de 2022 (fecha inicio None): {total_facturado(reservas,fecha_fin = datetime(2022, 2, 28).date())}")

def test_reservas_mas_largas(reservas):
    print("Test reservas_mas_largas")
    print(f"Con n = 3: {reservas_mas_largas(reservas)} ")

def test_cliente_mayor_facturacion(reservas):
    print("Test cliente_mayor_facturacion")
    print(f"Sin filtrar por servicios: {cliente_mayor_facturacion(reservas)}")
    print(f"Con Parking: {cliente_mayor_facturacion(reservas, {"Parking"})}")
    print(f"Con Parking o Spa: {cliente_mayor_facturacion(reservas, {"Parking", "Spa"})}")

def test_servicios_estrella_por_mes(reservas):
    print("Test servicios_estrella_por_mes")
    a = servicios_estrella_por_mes(reservas).items()
    b = servicios_estrella_por_mes(reservas, {"Familiar", "Deluxe"}).items()
    print("Todos los tipos de habitación:")
    for m in a:
        print(f"    {m}")
    
    print("Habitación familiar o deluxe:")
    for m in b:
        print(f"    {m}")

def test_media_dias_entre_reservas(reservas):
    print("Test media_dias_entre_reservas")
    print(media_dias_entre_reservas(reservas))

def test_cliente_reservas_mas_seguidas(reservas):
    print("Test cliente_reservas_mas_seguidas")
    min_reservas = 5
    print(f"El DNI del cliente con al menos {min_reservas} reservas y menor media de días entre reservas consecutivas es {cliente_reservas_mas_seguidas(reservas, min_reservas)}, con una media de días entre reservas de {cliente_reservas_mas_seguidas1(reservas, min_reservas)}.")

if __name__ == '__main__':
    datos = lee_reservas('data/reservas.csv')
    test_cliente_reservas_mas_seguidas(datos)