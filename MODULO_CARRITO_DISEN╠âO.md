# 🛒 Módulo de Carrito de Compras - Diseño Técnico

## 🚨 Problemática y Definición del Nuevo Módulo

### **Problemática Identificada**

**Limitaciones del Sistema Actual:**
- ❌ **Falta de Persistencia de Selección**: Los usuarios no pueden guardar productos para comprar después
- ❌ **Experiencia de Compra Incompleta**: No existe un flujo natural de selección → carrito → compra
- ❌ **Pérdida de Conversión**: Los usuarios deben recordar qué productos querían comprar
- ❌ **Funcionalidad E-commerce Básica Ausente**: Carrito es fundamental en cualquier tienda online
- ❌ **Escalabilidad Limitada**: Sin carrito, no se puede implementar checkout, órdenes o pagos

### **Definición del Módulo de Carrito**

**¿Qué es el Módulo de Carrito?**
Un sistema que permite a los usuarios:
- Agregar productos seleccionados a una "canasta virtual"
- Modificar cantidades de productos
- Remover productos no deseados
- Visualizar el total de su compra
- Persistir su selección entre sesiones

**Alcance Funcional:**
```
📦 CORE FEATURES
├── Agregar productos al carrito
├── Actualizar cantidades de productos
├── Remover productos del carrito
├── Calcular totales automáticamente
├── Persistir carrito por usuario
└── Validar disponibilidad de productos

🔮 FUTURE FEATURES (Fuera del alcance actual)
├── Descuentos y cupones
├── Carrito compartido
├── Wishlist integration
└── Recomendaciones en carrito
```

**Objetivos Específicos:**
1. **Funcional**: Proporcionar funcionalidad completa de carrito de compras
2. **Técnico**: Demostrar aplicación de múltiples patrones de diseño
3. **Arquitectural**: Mantener coherencia con la estructura existente
4. **Escalabilidad**: Preparar base para módulos de Orders y Payments

## 🎨 Patrones de Diseño Seleccionados

### **1. Repository Pattern** *(Reutilización + Extensión)*

**Justificación:**
- Mantiene consistencia con la arquitectura existente
- Abstrae la persistencia del carrito
- Permite cambiar storage (JSON → DB) sin afectar lógica de negocio

**Implementación:**
```python
# Interface
class CartRepository(ABC):
    @abstractmethod
    def get_cart_by_user_id(self, user_id: int) -> List[CartItem]
    
    @abstractmethod
    def add_item(self, user_id: int, cart_item: CartItem) -> CartItem
    
    @abstractmethod
    def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> bool
    
    @abstractmethod
    def remove_item(self, user_id: int, product_id: int) -> bool
    
    @abstractmethod
    def clear_cart(self, user_id: int) -> bool

# Implementación Concreta
class JsonCartRepository(CartRepository):
    # Implementación específica para JSON
```

### **2. Strategy Pattern** *(Nuevo)*

**Justificación:**
- Permite diferentes estrategias de cálculo de precios
- Facilita implementación futura de descuentos
- Cumple principio Open/Closed

**Implementación:**
```python
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_item_total(self, cart_item: CartItem) -> float
    
    @abstractmethod
    def calculate_cart_total(self, items: List[CartItem]) -> float

class StandardPricingStrategy(PricingStrategy):
    def calculate_item_total(self, cart_item: CartItem) -> float:
        return cart_item.price * cart_item.quantity
    
    def calculate_cart_total(self, items: List[CartItem]) -> float:
        return sum(self.calculate_item_total(item) for item in items)

class DiscountPricingStrategy(PricingStrategy):
    # Implementación futura para descuentos
```

### **3. Observer Pattern** *(Nuevo)*

**Justificación:**
- Notifica cambios en el carrito a otros módulos
- Desacopla carrito de sistemas dependientes (inventario, analytics)
- Facilita extensibilidad futura

**Implementación:**
```python
class CartObserver(ABC):
    @abstractmethod
    def on_item_added(self, user_id: int, cart_item: CartItem) -> None
    
    @abstractmethod
    def on_item_removed(self, user_id: int, product_id: int) -> None
    
    @abstractmethod
    def on_quantity_updated(self, user_id: int, product_id: int, old_qty: int, new_qty: int) -> None

class InventoryObserver(CartObserver):
    # Actualiza disponibilidad cuando se modifica carrito
    
class AnalyticsObserver(CartObserver):
    # Registra eventos para analytics
```

### **4. Command Pattern** *(Nuevo)*

**Justificación:**
- Encapsula operaciones del carrito como objetos
- Permite undo/redo futuro
- Facilita logging y auditoría

**Implementación:**
```python
class CartCommand(ABC):
    @abstractmethod
    def execute(self) -> bool
    
    @abstractmethod
    def undo(self) -> bool

class AddItemCommand(CartCommand):
    def __init__(self, cart_service, user_id: int, product_id: int, quantity: int):
        self.cart_service = cart_service
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
    
    def execute(self) -> bool:
        return self.cart_service.add_item(self.user_id, self.product_id, self.quantity)
    
    def undo(self) -> bool:
        return self.cart_service.remove_item(self.user_id, self.product_id)
```

### **5. Decorator Pattern** *(Reutilización)*

**Justificación:**
- Reutiliza sistema de autenticación existente
- Mantiene consistencia en seguridad
- Aplica cross-cutting concerns

**Implementación:**
```python
class CartController(Resource):
    def __init__(self, cart_service: CartService, auth_service: AuthService):
        self.cart_service = cart_service
        self.method_decorators = [require_auth(auth_service)]
    
    @require_auth(auth_service)
    def get(self):
        # Endpoint protegido
```

## 🏗️ Diseño de Alto Nivel del Módulo

### **Arquitectura por Capas**

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  CartController │  │   @require_auth │  │ REST Endpoints│ │
│  │   (Flask-RESTful)│  │   (Decorator)   │  │   /cart/*    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   CartService   │  │ PricingStrategy │  │ CartObserver │ │
│  │  (Orchestration)│  │   (Strategy)    │  │  (Observer)  │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │  CartCommand    │  │ ProductService  │                   │
│  │   (Command)     │  │  (Integration)  │                   │
│  └─────────────────┘  └─────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ CartRepository  │  │JsonCartRepository│  │   CartItem   │ │
│  │  (Interface)    │  │ (Implementation)│  │   (Model)    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    PERSISTENCE LAYER                        │
│                        db.json                              │
│                    { "carts": [...] }                       │
└─────────────────────────────────────────────────────────────┘
```

### **Modelo de Datos**

```python
@dataclass
class CartItem:
    user_id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int
    added_at: datetime
    
    def get_total_price(self) -> float:
        return self.product_price * self.quantity
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_price': self.product_price,
            'quantity': self.quantity,
            'added_at': self.added_at.isoformat(),
            'total_price': self.get_total_price()
        }
```

### **Estructura JSON en db.json**

```json
{
  "products": [...],
  "categories": [...],
  "favorites": [...],
  "carts": [
    {
      "user_id": 1,
      "items": [
        {
          "product_id": 1,
          "product_name": "T-Shirt",
          "product_price": 20.99,
          "quantity": 2,
          "added_at": "2024-01-15T10:30:00"
        }
      ]
    }
  ]
}
```

### **API Endpoints Design**

```http
# Obtener carrito del usuario autenticado
GET /cart
Response: {
  "items": [...],
  "total_items": 3,
  "total_price": 89.97
}

# Agregar producto al carrito
POST /cart/items
Body: {
  "product_id": 1,
  "quantity": 2
}

# Actualizar cantidad de producto
PUT /cart/items/<product_id>
Body: {
  "quantity": 3
}

# Remover producto del carrito
DELETE /cart/items/<product_id>

# Vaciar carrito completo
DELETE /cart

# Obtener resumen del carrito
GET /cart/summary
Response: {
  "total_items": 5,
  "total_price": 149.95,
  "item_count": 3
}
```

## 🔧 Plan de Integración con el Proyecto Existente

### **Fase 1: Preparación de Infraestructura**

**Modificaciones en Archivos Existentes:**

1. **src/container.py**
```python
# Agregar configuración del CartService
def _setup_dependencies(self):
    # ... configuraciones existentes ...
    
    # Nuevas configuraciones para Cart
    self._instances['cart_repository'] = RepositoryFactory.create_cart_repository(Config.DATABASE_FILE)
    self._instances['pricing_strategy'] = StandardPricingStrategy()
    self._instances['cart_service'] = CartService(
        self._instances['cart_repository'],
        self._instances['product_service'],
        self._instances['pricing_strategy']
    )
    self._instances['cart_controller_args'] = (
        self._instances['cart_service'], 
        self._instances['auth_service']
    )
```

2. **src/factories/repository_factory.py**
```python
class RepositoryFactory:
    # ... métodos existentes ...
    
    @staticmethod
    def create_cart_repository(database_file: str) -> CartRepository:
        return JsonCartRepository(database_file)
```

3. **app.py**
```python
def create_app():
    # ... configuración existente ...
    
    # Agregar endpoints del carrito
    api.add_resource(
        container.get('cart_controller'),
        '/cart',
        '/cart/items',
        '/cart/items/<int:product_id>',
        '/cart/summary',
        resource_class_args=container.get('cart_controller_args')
    )
```

4. **db.json**
```json
{
  "products": [...],
  "categories": [...],
  "favorites": [...],
  "carts": []  // Nueva sección
}
```

### **Fase 2: Implementación del Core**

**Nuevos Archivos a Crear:**

```
src/
├── models/
│   └── cart_item.py              # ✅ Nuevo
├── repositories/
│   ├── interfaces/
│   │   └── cart_repository.py    # ✅ Nuevo
│   └── implementations/
│       └── json_cart_repository.py # ✅ Nuevo
├── services/
│   └── cart_service.py           # ✅ Nuevo
├── controllers/
│   └── cart_controller.py        # ✅ Nuevo
└── strategies/
    └── pricing_strategy.py       # ✅ Nuevo
```

### **Fase 3: Integración con Servicios Existentes**

**Dependencias del CartService:**

```python
class CartService:
    def __init__(
        self, 
        cart_repository: CartRepository,
        product_service: ProductService,  # ← Integración existente
        pricing_strategy: PricingStrategy
    ):
        self.cart_repository = cart_repository
        self.product_service = product_service
        self.pricing_strategy = pricing_strategy
        self.observers: List[CartObserver] = []
    
    def add_item(self, user_id: int, product_id: int, quantity: int) -> bool:
        # Validar que el producto existe usando ProductService
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Lógica del carrito...
```

### **Fase 4: Testing y Validación**

**Estrategia de Testing de Integración:**

```python
# Tests de integración con módulos existentes
def test_cart_integration_with_product_service():
    # Verificar que CartService usa ProductService correctamente
    
def test_cart_integration_with_auth_service():
    # Verificar que endpoints requieren autenticación
    
def test_cart_endpoints_with_existing_api():
    # Verificar que nuevos endpoints no rompen API existente
```

### **Fase 5: Documentación y Deploy**

**Actualizaciones de Documentación:**

1. **README.md**: Agregar endpoints del carrito
2. **postman_collection.json**: Incluir requests del carrito
3. **API Documentation**: Swagger/OpenAPI specs
4. **Architecture Docs**: Diagramas UML actualizados

### **Puntos de Integración Críticos**

**✅ Reutilización Máxima:**
- AuthService para autenticación
- ProductService para validación de productos
- Container para inyección de dependencias
- RepositoryFactory para creación de repositorios

**✅ Cero Breaking Changes:**
- No modificar interfaces existentes
- Mantener endpoints actuales intactos
- Preservar estructura de datos existente
- Backward compatibility garantizada

**✅ Extensibilidad Futura:**
- Base preparada para Orders module
- Hooks para Payments integration
- Observer pattern para Analytics
- Command pattern para Audit trails

Este plan de integración garantiza una implementación incremental y segura, manteniendo la estabilidad del sistema existente mientras se agrega la nueva funcionalidad de carrito de compras.