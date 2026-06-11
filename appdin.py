import streamlit as st
import pandas as pd

# ==============================================================================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILOS
# ==============================================================================
st.set_page_config(
    page_title="Portal de Consulta - Dineria.mx",
    page_icon="💼",
    layout="wide"
)

# Estilos personalizados (Verde Institucional de Dineria y Gris Claro para legibilidad)
st.markdown("""
    <style>
    .main-title {
        color: #1b5e20;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        font-size: 30px;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #444444;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        margin-bottom: 25px;
    }
    .section-header {
        color: #1b5e20;
        font-family: 'Segoe UI', sans-serif;
        border-bottom: 2px solid #1b5e20;
        padding-bottom: 5px;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .rule-card {
        background-color: #f1f8e9;
        border-left: 5px solid #2e7d32;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 12px;
        color: #212121;
    }
    .payment-brand {
        color: #1b5e20;
        font-weight: bold;
        font-size: 18px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# ENCABEZADO PRINCIPAL
# ==============================================================================
st.markdown('<div class="main-title">DINERIA.MX - PORTAL DE CONSULTA OPERATIVA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Módulo de Glosario, Estructura de Tasas, Descuentos y Métodos de Pago</div>', unsafe_allow_html=True)

# ==============================================================================
# MENÚ DE NAVEGACIÓN LATERAL (SIDEBAR)
# ==============================================================================
st.sidebar.header("Control de Módulos")
opcion = st.sidebar.radio(
    "Selecciona la sección a consultar:",
    [
        "1. Glosario de Tecnicismos", 
        "2. Cuadro de Tasas Financieras",
        "3. Matriz de Descuentos (Wash) y Reglas",
        "4. Métodos y Canales de Pago"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Instrucción Operativa:**\n"
    "Este portal centraliza los términos oficiales del Core Bancario, las tasas vigentes, los márgenes de negociación y las cuentas bancarias autorizadas para la recaudación."
)

# ==============================================================================
# MÓDULO 1: GLOSARIO DE TECNICISMOS DE LA CAMPAÑA
# ==============================================================================
if opcion == "1. Glosario de Tecnicismos":
    st.markdown('<h2 class="section-header">📖 Glosario de Tecnicismos de la Campaña</h2>', unsafe_allow_html=True)
    st.write(
        "A continuación se detallan los conceptos técnicos obligatorios para la gestión en piso, "
        "así como su equivalencia comercial directa para negociaciones eficaces."
    )
    
    glosario_data = {
        "Término Técnico (Core)": [
            "LOAN REPAYMENT",
            "ROLLOVER",
            "MONTO PRINCIPAL (issued_amount)",
            "UNIFICACIÓN",
            "FINES",
            "ABANDERAMIENTO",
            "WASH (0, 1, 2, 3)"
        ],
        "Nombre Comercial / Común": [
            "Saldo Total / Monto para Liquidar",
            "Extensión de Plazo / Prórroga de Pago",
            "Capital Neto Otorgado / Préstamo Base",
            "Fusión de Saldos / Ajuste de Cuenta",
            "Intereses Moratorios / Penalización por Atraso",
            "Cuenta Retenida por Promesa / Prórroga Especial",
            "Segmentos de Mora (Temprana a Profunda)"
        ],
        "Definición Operativa y Regla de Negocio": [
            "Es el saldo deudor total requerido para cerrar el crédito en ceros. Integrado estrictamente por: Monto del crédito + comisión por disposición + IVA.",
            "Importe mínimo requerido para aplazar el vencimiento nominal de la deuda por un nuevo periodo. Se calcula con base en el monto otorgado y los días de extensión solicitados.",
            "Es el capital neto real transferido originalmente a la tarjeta de débito del cliente. No incluye comisiones ni impuestos agregados.",
            "Proceso operativo inhouse mediante el cual la mesa de control unifica múltiples depósitos parciales para acreditar el costo de una extensión o liquidación total.",
            "Cargo punitivo generado de manera diaria por atraso en el pago. Se calcula aplicando fijamente el 2% sobre el saldo total deudor (Loan Repayment).",
            "Proceso semanal que permite a una agencia retener la gestión de una cuenta mediante el registro de una promesa de pago válida antes del martes a las 11:00 PM.",
            "Clasificación interna de las cuentas según sus días de atraso. Define las estrategias de cobranza aplicables y los factores permitidos en la matriz de descuentos."
        ]
    }
    
    df_glosario = pd.DataFrame(glosario_data)
    
    busqueda = st.text_input("🔍 Filtrar término por palabra clave:", "")
    if busqueda:
        df_filtrado = df_glosario[
            df_glosario['Término Técnico (Core)'].str.contains(busqueda, case=False) | 
            df_glosario['Nombre Comercial / Común'].str.contains(busqueda, case=False)
        ]
    else:
        df_filtrado = df_glosario

    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)


# ==============================================================================
# MÓDULO 2: CUADRO DE TASAS FINANCIERAS
# ==============================================================================
elif opcion == "2. Cuadro de Tasas Financieras":
    st.markdown('<h2 class="section-header">📊 Cuadro de Tasas Financieras de la Operación</h2>', unsafe_allow_html=True)
    st.write("Estructura oficial de recargos moratorios programados inhouse extraída de las reglas de negocio:")

    tasas_data = {
        "Concepto de Tasa": [
            "Penalización Moratoria por Atraso (Fines)"
        ],
        "Tasa Diaria": ["2.00%"],
        "Base de Cálculo del Sistema": [
            "Se calcula de manera fija y diaria directamente sobre el saldo deudor total (Loan Repayment)."
        ]
    }
    
    df_tasas = pd.DataFrame(tasas_data)
    st.table(df_tasas)

    st.markdown('<h3 style="color:#1b5e20; margin-top:25px;">⚠️ Reglas Críticas de Aplicación de Tasas</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="rule-card">
        <strong>1. Aplicación de Penalizaciones (Fines):</strong><br>
        De acuerdo con las políticas corporativas de la campaña, las penalizaciones moratorias diarias equivalentes al 2% se ejecutan de manera automática e ininterrumpida por cada día de atraso registrado tras vencer la fecha límite de pago de la cuenta.
    </div>
    <div class="rule-card">
        <strong>2. Regla del Abono Parcial Insuficiente:</strong><br>
        Cualquier depósito realizado por el cliente que resulte <strong>menor al monto parametrizado como rollover_fee (extensión)</strong> se aplicará contablemente como una reducción al saldo deudor, pero <strong>no detendrá el motor de generación de Fines (2% diario)</strong> ni frenará el avance de la cuenta hacia el siguiente segmento de mora profunda.
    </div>
    <div class="rule-card">
        <strong>3. Cierre de Conciliaciones:</strong><br>
        Todos los montos recaudados deben revisarse contra el Layout de Pre-Cierres provisto por el área de Pagos. Las agencias externas cuentan con un plazo límite e improrrogable de 8 días naturales para conciliar diferencias antes de que el cierre financiero sea definitivo en los servidores.
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# MÓDULO 3: MATRIZ DE DESCUENTOS (WASH) Y REGLAS DE NEGOCIO
# ==============================================================================
elif opcion == "3. Matriz de Descuentos (Wash) y Reglas":
    st.markdown('<h2 class="section-header">📉 Matriz de Descuentos Máximos Permitidos</h2>', unsafe_allow_html=True)
    st.write(
        "Lineamientos, criterios técnicos y limitantes para la aplicación de descuentos máximos autorizados "
        "en las gestiones de cobranza de las carteras Dineria, Lanu y Prestomin."
    )

    descuentos_data = {
        "Segmento (Wash)": [
            "0 y 1", 
            "2", 
            "3"
        ],
        "Descuento Máximo (Factor)": [
            "1.4", 
            "1.2", 
            "1.0"
        ],
        "Criterio de Base para Liquidación": [
            "Aplica sobre el Principal Unpaid (Columna L).",
            "Aplica sobre el Principal Unpaid (Columna L).",
            "Aplica estrictamente sobre el Principal Inicial / Otorgado (Columna K)."
        ]
    }

    df_descuentos = pd.DataFrame(descuentos_data)
    st.dataframe(df_descuentos, use_container_width=True, hide_index=True)

    st.markdown('<h3 style="color:#1b5e20; margin-top:25px;">📋 Reglas de Validación y Restricciones de Negocio</h3>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rule-card">
        <strong>1. Restricción de Pago Mínimo (Tope contra Principal - Wash 0, 1 y 2):</strong><br>
        Al aplicar el factor de descuento (1.4 o 1.2) sobre el <em>Principal Unpaid (Columna L)</em>, si el monto de liquidación resultante es menor al valor registrado bajo el concepto de <strong>Principal (Columna K)</strong>, el descuento quedará automáticamente cancelado. En estos supuestos, la agencia deberá gestionar la liquidación de la cuenta tomando como base el adeudo total al día.
    </div>
    <div class="rule-card">
        <strong>2. Restricción de Pago Máximo (Tope contra Adeudo Total - Wash 0, 1 y 2):</strong><br>
        Al aplicar el factor de descuento, si el monto final de liquidación resultante es mayor al adeudo total vigente del usuario, el descuento no tendrá validez. La cobranza y liquidación se deberán formalizar exclusivamente cobrando el importe exacto del adeudo total al día.
    </div>
    <div class="rule-card">
        <strong>3. Tratamiento Especial Exclusivo para Cuentas Wash 3:</strong><br>
        Las cuentas en el segmento Wash 3 cuentan con una regla diferenciada y definitiva para proteger el capital original otorgado:
        <ul>
            <li>El factor de descuento del 1.0 se aplicará de forma única y exclusiva sobre el <strong>Principal Inicial otorgado al cliente (Columna K - issued_amount)</strong> del archivo de saldos.</li>
            <li><strong>Límite Crítico:</strong> Este monto (1.0 del Principal inicial) constituye el <em>descuento máximo absoluto</em> autorizado para este segmento. Bajo ninguna circunstancia se podrá ofrecer o procesar un esquema de liquidación que resulte en un pago menor al Principal otorgado de la cuenta.</li>
            <li>Los topes cruzados explicados en las restricciones 1 y 2 no operan bajo la misma lógica para Wash 3, ya que la base de cálculo cambia directamente a la Columna K.</li>
        </ul>
    </div>
    <div class="rule-card">
        <strong>4. Criterios Operativos y de Cumplimiento General:</strong><br>
        <ul>
            <li><strong>Vigencia Estricta de la Información:</strong> Para generar, simular o registrar cualquier tipo de convenio de pago o descuento, es obligatorio e indispensable utilizar el archivo de "Saldos" emitido el mismo día en que se efectúa el compromiso con el cliente. Queda estrictamente prohibido utilizar bases de datos de días o fechas anteriores.</li>
            <li><strong>Frecuencia e Historial de Pagos:</strong> Estas directrices de descuento se aplicarán de forma uniforme, sin importar el número de pagos previos que el cliente titular de la cuenta haya realizado a lo largo de la vida del crédito.</li>
            <li><strong>Canal de Excepciones Especiales:</strong> Ante cualquier escenario, caso particular o cuenta atípica que requiera una valoración diferenciada o soporte adicional fuera de esta matriz, se deberá mantener el canal habitual de comunicación enviando la solicitud formal con el caso documentado a través del grupo oficial de WhatsApp para su respectiva validación y apoyo.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# MÓDULO 4: MÉTODOS Y CANALES DE PAGO AUTORIZADOS
# ==============================================================================
elif opcion == "4. Métodos y Canales de Pago":
    st.markdown('<h2 class="section-header">💳 Métodos y Canales de Pago Oficiales 2026</h2>', unsafe_allow_html=True)
    st.write(
        "Cuentas, convenios bancarios y referencias oficiales asignadas por marca para recibir extensiones o liquidaciones totales. "
        "Es obligatorio indicar al cliente el concepto de pago de manera exacta para evitar problemas de unificación."
    )

    # Pestañas estructuradas homogéneamente para una excelente visualización
    tab1, tab2, tab3 = st.tabs(["Dineria.mx", "PRESTOMIN", "Lanu.mx"])

    # --- PESTAÑA 1: DINERIA.MX ---
    with tab1:
        st.markdown('<div class="payment-brand">Canales Autorizados para dineria.mx</div>', unsafe_allow_html=True)
        
        with st.expander("1. Transferencia Electrónica (SPEI)"):
            st.markdown("""
            * **Beneficiario:** Proximus Finance S DE RL DE CV
            * **Banco:** BBVA Bancomer
            * **CLABE:** `012180001068375493`
            * **Concepto:** `RFC + Dígito verificador` del cliente
            """)
            
        with st.expander("2. Practicaja o Ventanilla BBVA"):
            st.markdown("""
            * **Ubicación:** Sucursal BBVA más cercana.
            * **Instrucciones en Practicaja:** Seleccionar la opción **"Pago de Servicios"**.
            * **Número de Convenio:** `1371681`
            * **Nombre del Beneficiario:** Proximus Finance S DE RL DE CV
            * **Referencia y/o Concepto:** `RFC + Dígito verificador` del cliente
            """)
            
        with st.expander("3. Pago Presencial en OXXO"):
            st.markdown("""
            * **Ubicación:** Cualquier sucursal OXXO de la República Mexicana.
            * **Mecánica:** El cliente tiene que acudir al OXXO más cercano y realizar su pago directamente en caja.
            * **Requisito Obligatorio:** Deberá presentar su **Estado de Cuenta impreso** y mostrar el código de barras al cajero para su escaneo.
            """)

    # --- PESTAÑA 2: PRESTOMIN ---
    with tab2:
        st.markdown('<div class="payment-brand">Canales Autorizados para PRESTOMIN</div>', unsafe_allow_html=True)
        
        with st.expander("1. Ventanilla Bancaria BBVA"):
            st.markdown("""
            * **Ubicación:** Sucursal BBVA más cercana.
            * **Mecánica:** El cliente tiene que acudir de manera presencial a la zona de cajas.
            * **Número de Convenio:** `002370344`
            * **Nombre del Beneficiario:** SOFI DIGITAL MX,S.A. DE C.V.
            * **Referencia y/o Concepto:** `RFC + Dígito verificador` del cliente
            """)
            
        with st.expander("2. Practicaja BBVA"):
            st.markdown("""
            * **Ubicación:** Área de autoservicio (Practicajas) en cualquier sucursal BBVA.
            * **Instrucciones en Pantalla:** Escoger la opción **"Pago de Servicios"**.
            * **Ingreso de Datos:** Capturar manualmente el número de convenio oficial.
            * **Número de Convenio:** `002370344`
            * **Nombre del Beneficiario:** SOFI DIGITAL MX,S.A. DE C.V.
            * **Referencia y/o Concepto:** `RFC + Dígito verificador` del cliente
            """)

    # --- PESTAÑA 3: LANU.MX ---
    with tab3:
        st.markdown('<div class="payment-brand">Canales Autorizados para lanu.mx</div>', unsafe_allow_html=True)
        
        with st.expander("1. Practicaja o Ventanilla BBVA"):
            st.markdown("""
            * **Ubicación:** Sucursal BBVA más cercana.
            * **Instrucciones en Ventanilla:** Brindar el número de convenio de forma directa al cajero.
            * **Instrucciones en Practicaja:** Escoger la opción **"Pago de Servicios"** e ingresar manualmente el identificador.
            * **Número de Convenio:** `2460149`
            * **Nombre del Beneficiario:** SOFI DIGITAL MX,S.A. DE C.V.
            * **Referencia y/o Concepto:** `RFC + Dígito verificador` del cliente
            """)
            
        with st.expander("2. Transferencia Bancaria (De Bancomer a Bancomer)"):
            st.markdown("""
            * **Mecánica:** Operación directa desde la aplicación móvil de BBVA Bancomer.
            * **Instrucción de Registro:** El cliente tiene que dar de alta nuestro servicio como **"Pago de Servicios"** dentro de su app móvil.
            * **Número de Convenio:** `2460149`
            * **Nombre del Beneficiario:** SOFI DIGITAL MX,S.A. DE C.V.
            * **Acción:** Capturar el monto exacto de la operación (extensión o totalidad).
            * **Referencia y/o Concepto:** `RFC + Dígito verificador` del cliente
            """)
            
        with st.expander("3. Tiendas de Conveniencia via PAYNET"):
            st.markdown("""
            * **Comercios Participantes:** Walmart, Sam's Club, Bodega Aurrera, 7-Eleven, Farmacias del Ahorro, Extra y Círculo K.
            * **Mecánica Digital Previa:** El cliente tiene que generar su **código de barras** oficial ingresando a su perfil personal en el portal de la marca.
            * **Selección en Portal:** Indicar explícitamente el método de pago **Paynet** y capturar el importe de su trámite (extensión o liquidación completa).
            * **Pago Presencial:** Presentarse en las cajas de cualquiera de los comercios enlistados arriba exhibiendo el código de barras impreso o digital para completar el depósito.
            """)
