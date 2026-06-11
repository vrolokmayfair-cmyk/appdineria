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
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# ENCABEZADO PRINCIPAL
# ==============================================================================
st.markdown('<div class="main-title">DINERIA.MX - PORTAL DE CONSULTA OPERATIVA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Módulo de Glosario, Estructura de Tasas y Políticas de Descuento</div>', unsafe_allow_html=True)

# ==============================================================================
# MENÚ DE NAVEGACIÓN LATERAL (SIDEBAR)
# ==============================================================================
st.sidebar.header("Control de Módulos")
opcion = st.sidebar.radio(
    "Selecciona la sección a consultar:",
    [
        "1. Glosario de Tecnicismos", 
        "2. Cuadro de Tasas Financieras",
        "3. Matriz de Descuentos (Wash) y Reglas"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Instrucción Operativa:**\n"
    "Este portal centraliza los términos oficiales del Core Bancario, las tasas vigentes y los márgenes de negociación autorizados para Dineria.mx."
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
    st.write("Estructura oficial de rendimientos, tasas equivalentes ordinarias y recargos moratorios programados inhouse:")

    tasas_data = {
        "Tipo de Concepto / Producto": [
            "Interés Ordinario Base (Dineria.mx)",
            "Penalización Moratoria por Atraso (Fines)",
            "Tasa Ponderada de Control Interno"
        ],
        "Tasa Diaria": ["0.80%", "2.00%", "1.15%"],
        "Tasa Mensual (Base 30 días)": ["24.00%", "60.00%", "34.50%"],
        "Tasa Anualizada (CAT Informativo)": ["288.00%", "720.00%", "414.00%"],
        "Mecánica de Aplicación en Sistema": [
            "Se calcula exclusivamente sobre el Monto Principal (Issued Amount) activo.",
            "Se ejecuta directo sobre el Saldo Total Deudor (Loan Repayment) por cada día de mora acumulado.",
            "Indicador referencial para métricas contables inhouse."
        ]
    }
    
    df_tasas = pd.DataFrame(tasas_data)
    st.table(df_tasas)

    st.markdown('<h3 style="color:#1b5e20; margin-top:25px;">⚠️ Reglas Críticas de Aplicación de Tasas</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="rule-card">
        <strong>1. Transición de Tasas en Asignación Externa:</strong><br>
        Cuando el core transfiere una cuenta a agencias externas por mora profunda (segmentos Wash 2 o superior), el sistema <strong>congela de forma automática la acumulación del interés ordinario</strong>. A partir de ese momento, la carga financiera recae de forma exclusiva en la tasa de interés moratorio (Fines del 2% diario) sobre el saldo acumulado.
    </div>
    <div class="rule-card">
        <strong>2. Regla del Abono Parcial Insuficiente:</strong><br>
        Cualquier depósito realizado por el cliente que resulte <strong>menor al monto parametrizado como rollover_fee (extensión)</strong> se aplicará contablemente como una reducción al saldo deudor, pero <strong>no detendrá el motor de generación de Fines (2% diario)</strong> ni frenará el avance de la cuenta hacia el siguiente segmento de mora profunda.
    </div>
    <div class="rule-card">
        <strong>3. Cierre de Conciliaciones:</strong><br>
        Todos los montos recaudados e intereses aplicados deben revisarse contra el Layout de Pre-Cierres provisto por el área de Pagos. Las agencias externas cuentan con un plazo límite e improrrogable de 8 días naturales para conciliar diferencias antes de que el cierre financiero sea definitivo en los servidores.
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# MÓDULO 3: MATRIZ DE DESCUENTOS (WASH) Y REGLAS DE NEGOCIO
# ==============================================================================
elif opcion == "3. Matriz de Descuentos (Wash) y Rules":
    st.markdown('<h2 class="section-header">📉 Matriz de Descuentos de Acuerdo al Segmento Wash</h2>', unsafe_allow_html=True)
    st.write(
        "Parámetros comerciales obligatorios y factores duros asignados para la negociación de cuentas en atraso. "
        "El uso de estas bases garantiza la correcta conciliación automatizada con el sistema core."
    )

    # Tabla estructurada de descuentos basados en los factores del modelo de negocio
    descuentos_data = {
        "Segmento de Mora": [
            "Wash 0 (Mora Preventiva)", 
            "Wash 1 (Mora Temprana)", 
            "Wash 2 (Mora Media)", 
            "Wash 3 (Mora Profunda)"
        ],
        "Factor de Descuento": [
            "No Aplica", 
            "Factor 1.4", 
            "Factor 1.2", 
            "Factor 1.0"
        ],
        "Base de Cálculo en Sistema": [
            "Liquidación al 100% del adeudo exigible.",
            "Calculado sobre el Saldo Bruto Total (Capital + Comisiones acumuladas + IVA).",
            "Calculado sobre el Saldo de Capital Remanente (Principal Unpaid).",
            "Calculado sobre el Monto Principal Otorgado Inicial (Issued Amount original)."
        ],
        "Margen de Condonación Permitido": [
            "0% de descuento. Solo se habilitan prórrogas ordinarias (Rollovers).",
            "Hasta un 20% máximo de condonación sobre el saldo total acumulado.",
            "Hasta un 40% de descuento, eliminando moratorios generados en el periodo.",
            "Liquidación al 100% del principal original, condonando el total de intereses y comisiones."
        ]
    }

    df_descuentos = pd.DataFrame(descuentos_data)
    st.dataframe(df_descuentos, use_container_width=True, hide_index=True)

    # REGLAS DE LOS DESCUENTOS
    st.markdown('<h3 style="color:#1b5e20; margin-top:25px;">📋 Reglas de Negocio para la Aplicación de Descuentos</h3>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rule-card">
        <strong>1. Respeto Estricto de Factores:</strong><br>
        Ningún asesor de cobranza o supervisor de agencia externa tiene facultades operativas en el core para aplicar quitas fuera de los factores asignados (1.4, 1.2 o 1.0). Cualquier desviación en el cálculo provocará que el script de validación de pagos rechace la conciliación automática.
    </div>
    <div class="rule-card">
        <strong>2. Ventana de Promesas y Cierre de Abanderamiento:</strong><br>
        Para que un descuento negociado sea respetado por el sistema y la cuenta no regrese al marcado masivo general, se debe registrar una promesa válida en el sistema antes del <strong>Martes a las 11:00 PM</strong>. Los acuerdos registrados los miércoles por la mañana se procesan sin abanderamiento y quedan expuestos a reasignación de cartera.
    </div>
    <div class="rule-card">
        <strong>3. Excepciones Especiales (Mesa de Control):</strong><br>
        Cualquier propuesta económica que requiera romper los límites fijados por la matriz Wash debido a condiciones socioeconómicas críticas demostradas por el cliente, deberá tramitarse mediante un ticket formal enviado a la <strong>Dirección de Finanzas / Mesa de Control Inhouse</strong>. La respuesta de validación toma un plazo máximo de 3 días hábiles.
    </div>
    <div class="rule-card">
        <strong>4. Validación de Cartas Convenio:</strong><br>
        Antes de indicarle al cliente que efectúe el depósito acordado con descuento, la agencia externa está obligada a emitir la Carta Convenio foliada y cargar el layout de pre-cierre. Pagos realizados sin el correspondiente soporte documental no se unificarán y se tomarán únicamente como abonos parciales al capital neto, reactivando la mora.
    </div>
    """, unsafe_allow_html=True)
