# Documentación Detallada: Módulos de Productos y Cotizaciones

## Módulo de Productos

### 1. Gestión de Sectores

#### Características
- Identificador único
- Descripción
- Estado (activo/inactivo)

#### Funcionalidades
- División de caja por sector
- Filtrado de productos y pedidos
- Clasificación de máquinas

#### Reglas Específicas
- Un producto puede tener sector offset pero cotizar como digital
- Sectores predefinidos no pueden eliminarse
- Afecta reportes financieros por división

### 2. Sistema de Categorización

#### Estructura Jerárquica
- Categorías padre
  * Descripción
  * Imagen (opcional)
  * Estado
- Subcategorías
  * Referencia a categoría padre
  * Descripción propia
  * Estado independiente

#### Comportamiento
- Navegación en árbol
- Herencia de propiedades
- Filtrado multinivel

#### Restricciones
- Máximo 3 niveles de profundidad
- Categorías padre pueden existir sin hijas
- Subcategorías requieren padre válido

### 3. Gestión de Colores

#### Atributos
- Identificador
- Descripción técnica
- Descripción comercial
- Aplicabilidad por sector

#### Uso en Productos
- Define proceso de impresión
- Especifica caras afectadas
- Afecta cálculo de precios

#### Configuraciones
- Combinaciones permitidas
- Restricciones por material
- Impacto en tiempos de producción

### 4. Sistema de Materiales

#### Características Base
- Identificador
- Nombre comercial
- Descripción técnica
- Especificaciones

#### Atributos Técnicos
- Gramaje/Grosor
- Dimensiones estándar
- Restricciones de uso

#### Reglas de Uso
- Compatibilidad con sectores
- Limitaciones de tamaño
- Combinaciones con terminaciones

### 5. Gestión de Tamaños

#### Tamaños Predefinidos
- Dimensiones exactas
- Unidad de medida (cm/m)
- Factor de bonificación

#### Configuración
- Rangos permitidos
- Incrementos válidos
- Restricciones por sector

#### Reglas de Negocio
- Bonificaciones automáticas
- Validaciones por material
- Límites por máquina

### 6. Sistema de Terminaciones

#### Estructura
- Terminaciones base
- Subtipos de terminación
- Estados posibles

#### Clasificación
- Terminaciones fijas
  * Obligatorias para producto
  * Incluidas en precio base
  * No visibles al cliente
- Terminaciones opcionales
  * Seleccionables
  * Precio adicional
  * Visibles en cotizador

#### Configuraciones
- Compatibilidad entre terminaciones
- Restricciones por material
- Impacto en tiempos

### 7. Productos

#### Datos Base
- Información general
  * Nombre
  * Descripción
  * Imagen
  * Estado
- Clasificación
  * Sector
  * Categorías
  * Tipo de cotizador

#### Opciones de Control
- Trabajo con pliegos
- Visibilidad en tienda
- Producto destacado
- Precio base (opcional)

#### Markup por Cliente
- Tipos de cliente
- Porcentajes de ajuste
- Aplicación automática

## Módulo de Cotizaciones

### 1. Sistema Monetario

#### Gestión de Monedas
- Definición de monedas
  * Nombre/Código
  * Tasa de cambio
  * Fecha actualización
- Reglas de conversión
  * Actualización manual
  * Histórico de cambios
  * Redondeo

#### Precios
- Siempre sin IVA
- Moneda configurable
- Conversión automática

### 2. Cotización Offset

#### Variables Base
- Superficie del producto
- Color seleccionado
- Material base

#### Sistema de Cargos
1. Por Tamaños Fijos
   - Medidas exactas
   - Porcentajes de bonificación
   - Prioridad máxima

2. Por Rangos
   - Rangos de superficie
   - Porcentajes de ajuste
   - Aplicación secundaria

#### Cálculo
- Precio base por cm²
- Multiplicadores
- Bonificaciones/Penalizaciones

### 3. Cotización Digital

#### Sistema de Clicks
- Tipos de click
  * Definición
  * Precio base
  * Máquina asociada

#### Cargos por Bajada
- Rangos de cantidad
- Porcentajes de ajuste
- Mínimos por trabajo

#### Variables de Cálculo
- Papel seleccionado
- Cantidad de bajadas
- Terminaciones aplicables

### 4. Cotización Gran Formato

#### Variables Base
- Material seleccionado
- Calidad de impresión
- Dimensiones

#### Sistema de Calidades
- Niveles definidos
- Porcentajes de ajuste
- Restricciones por material

#### Cálculo
- Por metro cuadrado
- Por metro lineal
- Mínimos por trabajo

### 5. Sistema de Cantidades

#### Modalidades
1. Sin Cantidad
   - Productos empaquetados
   - Precio único
   - Cantidad predefinida

2. Cantidad Libre
   - Rango permitido
   - Multiplicador directo
   - Mínimos y máximos

3. Múltiplos
   - Intervalo base
   - Repeticiones máximas
   - Cálculo automático

4. Cantidades Fijas
   - Opciones predefinidas
   - Precios específicos
   - No modificables

5. Cantidades Personalizadas
   - Rangos configurables
   - Multiplicadores variables
   - Ajustes por volumen

### 6. Tiempos de Producción

#### Configuración Base
- Días estándar
- Opciones de urgencia
- Recargos aplicables

#### Sistema de Urgencias
- Porcentajes de incremento
- Validación de factibilidad
- Restricciones por producto

#### Reglas de Aplicación
- Prioridad en producción
- Impacto en precios
- Límites por sector

### 7. Reglas de Cálculo

#### Prioridades
1. Tamaños predefinidos
2. Rangos de superficie
3. Cantidades
4. Urgencias

#### Multiplicadores
- Secuencia de aplicación
- Acumulación permitida
- Límites máximos

#### Redondeos
- Por tipo de producto
- Por monto final
- Por cantidad

