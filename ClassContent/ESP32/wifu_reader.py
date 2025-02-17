import network
import binascii

wlan = network.WLAN()  # network.WLAN(network.STA_IF)
wlan.active(True)
networks = wlan.scan()  # Lista de tuplas con 6 campos ssid, bssid, channel, RSSI, security, hidden
i = 0
networks.sort(key=lambda x: x[3], reverse=True)  # sorted on RSSI (3)

# Imprimir encabezado de la tabla con ancho fijo
print(f"{'N°':<4} {'SSID':<20} {'BSSID':<20} {'Canal':<6} {'RSSI':<6} {'Seguridad':<10} {'Oculto':<6}")

for w in networks:
    i += 1
    ssid = w[0].decode() if w[0] else "N/A"  # En caso de que el SSID esté vacío
    bssid = binascii.hexlify(w[1]).decode()
    channel = w[2]
    rssi = w[3]
    security = w[4]
    hidden = w[5]

    # Imprimir cada red con formato alineado
    print(f"{i:<4} {ssid:<20} {bssid:<20} {channel:<6} {rssi:<6} {security:<10} {hidden:<6}")

