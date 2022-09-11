==================================
Invoice Alternative Payee Scenario
==================================

Imports::

    >>> from decimal import Decimal

    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import (
    ...     create_company, get_company)
    >>> from trytond.modules.account.tests.tools import (
    ...     create_fiscalyear, create_chart, get_accounts)
    >>> from trytond.modules.account_invoice.tests.tools import (
    ...     set_fiscalyear_invoice_sequences)

Activate modules::

    >>> config = activate_modules('account_invoice')

    >>> Invoice = Model.get('account.invoice')
    >>> Journal = Model.get('account.journal')
    >>> PaymentMethod = Model.get('account.invoice.payment.method')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')
    >>> period = fiscalyear.periods[0]

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)

    >>> journal_cash, = Journal.find([
    ...         ('code', '=', 'CASH'),
    ...         ])

    >>> payment_method = PaymentMethod()
    >>> payment_method.name = "Cash"
    >>> payment_method.journal = journal_cash
    >>> payment_method.credit_account = accounts['cash']
    >>> payment_method.debit_account = accounts['cash']
    >>> payment_method.save()

Create parties::

    >>> Party = Model.get('party.party')
    >>> party1 = Party(name="Party 1")
    >>> party1.save()
    >>> party2 = Party(name="Party 2")
    >>> party2.save()
    >>> party3 = Party(name="Party 3")
    >>> party3.save()

Post customer invoice::

    >>> invoice = Invoice()
    >>> invoice.party = party1
    >>> invoice.alternative_payees.append(Party(party2.id))
    >>> line = invoice.lines.new()
    >>> line.account = accounts['revenue']
    >>> line.quantity = 1
    >>> line.unit_price = Decimal(10)
    >>> invoice.click('post')
    >>> invoice.state
    'posted'
    >>> len(invoice.lines_to_pay)
    1
    >>> invoice.amount_to_pay
    Decimal('10.00')

    >>> party1.reload()
    >>> party1.receivable
    Decimal('0.0')
    >>> party2.reload()
    >>> party2.receivable
    Decimal('10.00')
    >>> party3.reload()
    >>> party3.receivable
    Decimal('0.0')

Set another payee::

    >>> delegate = Wizard(
    ...     'account.invoice.lines_to_pay.delegate', [invoice])
    >>> delegate_lines, = delegate.actions
    >>> delegate_lines.form.party = party3
    >>> delegate_lines.execute('delegate')

    >>> invoice.reload()
    >>> invoice.state
    'posted'
    >>> len(invoice.lines_to_pay)
    3
    >>> invoice.amount_to_pay
    Decimal('10.00')

    >>> party1.reload()
    >>> party1.receivable
    Decimal('0.0')
    >>> party2.reload()
    >>> party2.receivable
    Decimal('0.0')
    >>> party3.reload()
    >>> party3.receivable
    Decimal('10.00')

Pay the invoice::

    >>> pay = Wizard('account.invoice.pay', [invoice])
    >>> pay.form.payee = party3
    >>> pay.form.amount = Decimal('10.00')
    >>> pay.form.payment_method = payment_method
    >>> pay.execute('choice')
    >>> pay.state
    'end'
    >>> invoice.state
    'paid'
    >>> len(invoice.payment_lines)
    1
    >>> len(invoice.reconciliation_lines)
    1
