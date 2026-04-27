from app.inventary.inventory_manager import InventoryManager
from app.ventas.ventas_logic import VentasLogic
from app.database.db_config import Database

def probar_sistema():
    # 1. Asegurar que las tablas existan
    Database().setup_database()
    
    inventario = InventoryManager()
    ventas = VentasLogic()

    print("--- 📦 PRUEBA DE INVENTARIO ---")
    # Intentamos agregar un producto
    exito, msg = inventario.agregar_producto("Laptop Gamer", 1500.0, 10, "Electrónica")
    print(f"Resultado: {msg}")

    # 2. Consultar productos con stock bajo (para ver si se guardó)
    productos = inventario.consultar_stock_bajo(15)
    print(f"Productos en sistema: {productos}")

    print("\n--- 💰 PRUEBA DE VENTAS ---")
    # Simulamos una venta del producto con ID 1 (el que acabamos de crear)
    # Vendemos 3 unidades
    exito_v, msg_v = ventas.procesar_venta(1, 3)
    print(f"Venta 1: {msg_v}")

    # 3. Validar si el stock bajó a 7
    stock_final = inventario.consultar_stock_bajo(10)
    print(f"Stock actualizado después de venta: {stock_final}")

    # 4. Prueba de seguridad lógica: Vender más de lo que hay
    print("\n--- 🛡️ PRUEBA DE INTEGRIDAD ---")
    exito_v2, msg_v2 = ventas.procesar_venta(1, 50)
    print(f"Intento de vender 50 unidades: {msg_v2}")

if __name__ == "__main__":
    probar_sistema()