# Sistema de Gestión de Impresión y Cotización

## Índice
1. [Visión General](#visión-general)
2. [Módulos del Sistema](#módulos-del-sistema)
3. [Flujos de Trabajo](#flujos-de-trabajo)
4. [Reglas de Negocio](#reglas-de-negocio)
5. [Plan de Implementación](#plan-de-implementación)

## Visión General

### Descripción del Proyecto
Sistema integral para la gestión de una empresa de impresión que maneja múltiples tipos de productos y metodologías de cotización. El sistema permite administrar productos, calcular precios según diferentes criterios, y gestionar pedidos.

### Objetivos del Sistema
- Gestionar el catálogo completo de productos de impresión
- Automatizar los cálculos de cotizaciones según tipo de trabajo
- Manejar de forma diferenciada los tres sectores: Offset, Digital y Gran Formato
- Proporcionar interfaces específicas para clientes y administradores
- Optimizar el proceso de presupuestación
- Mantener un registro organizado de productos y configuraciones

## Módulos del Sistema

### 1. Módulo de Productos

#### Gestión de Sectores
- Digital
- Offset
- Gran Formato
- Cada sector afecta:
  * División de caja
  * Filtrado de productos
  * Filtrado de pedidos

#### Gestión de Categorías
- Estructura jerárquica (categorías y subcategorías)
- Ejemplos:
  * Tarjetas
    - Tarjetas Clásicas
    - Tarjetas Personales
  * Folletos
  * Carteles

#### Gestión de Colores
- Define procesos de impresión
- Afecta precios
- Define intervención en caras del producto
- Ejemplos:
  * Full color frente y dorso
  * Negro frente
  * Color en cara externa

#### Gestión de Materiales
- Tipos de papel/sustrato
- Gramajes
- Características especiales
- Ejemplos:
  * Papel 115 gramos
  * Vinilo
  * Lona

#### Gestión de Tamaños
- Predefinidos por sector
- Medidas en cm o metros
- Sistema de bonificaciones
- Ejemplos:
  * 20cm x 30cm (Digital)
  * 0.85m x 2m (Gran Formato)

#### Gestión de Terminaciones
- Estructura jerárquica
- Tipos:
  * Fijas (obligatorias)
  * Opcionales
- Ejemplos:
  * Agujereado
  * Plastificado
  * Corte

### 2. Módulo de Cotizaciones

#### Sistema de Monedas
- Peso argentino (ARS)
- Dólar estadounidense (USD)
- Actualización manual de cotización
- Precios sin IVA

#### Tipos de Cotización

##### Cotización Offset
- Base: superficie y color
- Variables:
  * Precio por cm²
  * Bonificaciones por tamaños predefinidos
  * Penalizaciones por rangos de superficie
- Sistema de multiplicadores por cantidad

##### Cotización Digital
- Base: sistema de clicks
- Variables:
  * Tipo de click (A3, A4)
  * Costo de papel
  * Cargos por bajada
  * Terminaciones

##### Cotización Gran Formato
- Base: material y calidad
- Variables:
  * Costo por m²
  * Tipo de impresión
  * Nivel de calidad
  * Terminaciones específicas

#### Sistema de Cantidades
1. Sin cantidad (productos empaquetados)
2. Libre (multiplicador directo)
3. Múltiplo (intervalos fijos)
4. Cantidades fijas
5. Cantidades personalizadas con multiplicadores

#### Tiempos de Producción
- Días estándar por producto
- Sistema de urgencias
- Recargos por adelanto
- Descripción de opciones de tiempo

## Flujos de Trabajo

### 1. Configuración de Productos
1. Definición de características base
2. Asignación de sector
3. Configuración de opciones disponibles
4. Establecimiento de precios base

### 2. Proceso de Cotización
1. Selección de producto
2. Elección de características según tipo
3. Selección de cantidades
4. Cálculo automático
5. Aplicación de markup según cliente

### 3. Gestión de Pedidos
1. Creación desde cotización
2. Asignación a sector
3. Seguimiento de producción
4. Control de tiempos

## Reglas de Negocio

### Productos
- Todo producto debe tener sector asignado
- Un producto puede pertenecer a múltiples categorías
- Productos pueden ocultarse de tienda sin eliminarse

### Cotizaciones
- Precios siempre sin IVA
- Bonificaciones tienen prioridad sobre penalizaciones
- Tiempos de producción afectan precio final
- Markup varía según tipo de cliente

## Plan de Implementación

### Fase 1: Estructura Base
- Configuración inicial
- Carga de datos maestros
- Pruebas de configuración

### Fase 2: Módulo de Productos
- Implementación de ABMs
- Gestión de características
- Sistema de categorización

### Fase 3: Módulo de Cotizaciones
- Implementación por tipo:
  1. Offset (más simple)
  2. Digital
  3. Gran Formato
- Pruebas de cálculos

### Fase 4: Integración y Ajustes
- Refinamiento de interfaces
- Ajustes de cálculos
- Capacitación de usuarios

