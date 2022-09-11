# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool

from . import account, company, invoice, party, payment_term


def register():
    Pool.register(
        payment_term.PaymentTerm,
        payment_term.PaymentTermLine,
        payment_term.PaymentTermLineRelativeDelta,
        payment_term.TestPaymentTermView,
        payment_term.TestPaymentTermViewResult,
        invoice.Invoice,
        invoice.InvoiceAdditionalMove,
        invoice.AlternativePayee,
        invoice.InvoicePaymentLine,
        invoice.InvoiceLine,
        invoice.InvoiceLineTax,
        invoice.InvoiceTax,
        invoice.PayInvoiceStart,
        invoice.PayInvoiceAsk,
        invoice.CreditInvoiceStart,
        party.Address,
        party.ContactMechanism,
        party.Party,
        party.PartyPaymentTerm,
        account.Configuration,
        account.ConfigurationDefaultPaymentTerm,
        account.InvoiceSequence,
        # Match pattern migration fallbacks to Fiscalyear values so Period
        # must be registered before Fiscalyear
        account.Period,
        account.FiscalYear,
        account.Move,
        account.MoveLine,
        account.Reconciliation,
        invoice.PaymentMethod,
        company.Company,
        module='account_invoice', type_='model')
    Pool.register(
        payment_term.TestPaymentTerm,
        invoice.PayInvoice,
        invoice.CreditInvoice,
        invoice.RescheduleLinesToPay,
        invoice.DelegateLinesToPay,
        party.Replace,
        party.Erase,
        account.RenewFiscalYear,
        account.RescheduleLines,
        account.DelegateLines,
        module='account_invoice', type_='wizard')
    Pool.register(
        invoice.InvoiceReport,
        module='account_invoice', type_='report')
