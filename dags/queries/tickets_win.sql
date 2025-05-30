SELECT
    CAST(so.id AS TEXT)                 AS "requirementVid",
    am.invoice_origin                   AS "N° TICKET",
    TO_CHAR(am.invoice_date, 'MM/YY')   AS "MES/AÑO",
    am.invoice_date                     AS "FECHA DE FACTURA",
    am.l10n_pe_document_number          AS "N° DE FACTURA",
    am.invoice_partner_display_name     AS "CLIENTE",
    am.amount_total_signed              AS "TOTAL FIRMADO",
        CASE
        when COALESCE(apt.name ->>'es_PE', 'No especificado') = 'Al contado'
        then 'CONTADO'
        else 'CRÉDITO'
    END                                 AS "FACTURACION",
    am.state                            AS estado,
    am.payment_state                    AS estado_de_pago,
    CASE
        WHEN am.name ILIKE '%FC%' THEN 'Nota de Crédito'
        WHEN am.name ILIKE '%B0%' THEN 'Boleta Tipo 1'
        WHEN am.name ILIKE '%BC%' THEN 'Boleta Tipo 2'
        ELSE 'Factura'
    END                                 AS "TIPO",
    CASE 
        WHEN am.is_move_sent IS TRUE THEN 'ENVIADO'
        ELSE 'NO ENVIADO'
    END                                 AS "ESTADO DE ENVIO DE FT AL CLIENTE"
FROM account_move am
LEFT JOIN res_currency rc ON rc.id = am.currency_id
LEFT JOIN account_payment_term apt ON apt.id = am.invoice_payment_term_id
LEFT JOIN res_users ru ON ru.id = am.invoice_user_id
LEFT JOIN res_partner rp ON rp.id = ru.partner_id
LEFT JOIN sale_order so ON so.name = am.invoice_origin
WHERE am.move_type IN ('out_invoice', 'out_refund')
    AND am.state != 'cancel'
    AND am.invoice_date >= '2024-01-01'
ORDER BY am.id DESC;