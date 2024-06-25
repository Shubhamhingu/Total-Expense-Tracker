from django.shortcuts import render # type: ignore
from django.utils import timezone # type: ignore
from .forms import ShiftForm, TransactionForm, TransactionResultForm, ShiftResultForm
from .models import  Shift, Transaction, GlobalVariable
from datetime import datetime
from django.db import connection, OperationalError # type: ignore

def add_shift(request):
    data_submitted = False
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift_start = form.cleaned_data['shift_start']
            shift_end = form.cleaned_data['shift_end']
            is_cash = form.cleaned_data['is_cash']
            tip = form.cleaned_data['tip']
            ride = form.cleaned_data['ride']
            date_created = timezone.now()
            time_diff = shift_end - shift_start
            hours_worked = time_diff.total_seconds() / 3600
            outList = list()
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT value FROM Total_Expense_Tracker_globalvariable WHERE key = "cash";')
                    outList.append(round(cursor.fetchall()[0][0],2))
                    cursor.execute('SELECT value FROM Total_Expense_Tracker_globalvariable WHERE key = "bank";')
                    outList.append(round(cursor.fetchall()[0][0],2))
                    sql_query = 'UPDATE Total_Expense_Tracker_globalvariable SET value = %s WHERE key = %s;'
                    if is_cash == 'True':
                        value = outList[0] - float(ride) + float(tip)
                        cursor.execute(sql_query,[value,'cash'])
                    else:
                        value = outList[1] - float(ride) + float(tip)
                        cursor.execute(sql_query,[value,'bank'])
            except OperationalError as e:
                print(f"Error updating global variable: {e}")
            
            transaction = Transaction.objects.create(credit=tip, debit=ride, date_created=shift_start, is_cash=is_cash, type='Shift')
            Shift.objects.create(shift_start=shift_start, shift_end=shift_end,hours_worked=hours_worked,  is_cash=is_cash,tip = transaction, ride=transaction, date_created=date_created)
            data_submitted = True
            form = ShiftForm()
    else:
        form = ShiftForm()
    errors = {}
    if form.errors:
        for field, error_list in form.errors.items():
            errors[form[field].label] = error_list

    return render(request, 'shiftform.html', {'form': form, 'errors':errors,'data_submitted': data_submitted})


def add_transaction(request):
    data_submitted = False
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            creditvar, debitvar = 0, 0
            is_credit = form.cleaned_data['is_credit']
            amount = form.cleaned_data['amount']
            if str(is_credit) == 'True':
                creditvar = amount
            else:
                debitvar = amount
            is_cash = form.cleaned_data['is_cash']
            type = form.cleaned_data['type']
            if type == 'Other':
                type = form.cleaned_data['other_type']
            date_created = timezone.now()
            Transaction.objects.create(credit=creditvar, debit=debitvar, date_created=date_created, is_cash=is_cash, type=type)
            outList = list()
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT value FROM Total_Expense_Tracker_globalvariable WHERE key = "cash";')
                    outList.append(round(cursor.fetchall()[0][0],2))
                    cursor.execute('SELECT value FROM Total_Expense_Tracker_globalvariable WHERE key = "bank";')
                    outList.append(round(cursor.fetchall()[0][0],2))
                    sql_query = 'UPDATE Total_Expense_Tracker_globalvariable SET value = %s WHERE key = %s;'
                    if is_cash == 'True':
                        value = outList[0] - float(debitvar) + float(creditvar)
                        cursor.execute(sql_query,[value,'cash'])
                    else:
                        value = outList[1] - float(debitvar) + float(creditvar)
                        cursor.execute(sql_query,[value,'bank'])
            except OperationalError as e:
                print(f"Error updating global variable: {e}")
            data_submitted = True
            form = TransactionForm()
    else:
        form = TransactionForm()
    errors = {}
    if form.errors:
        for field, error_list in form.errors.items():
            errors[form[field].label] = error_list
    return render(request, 'add_transaction.html', {'form': form, 'errors':errors,'data_submitted': data_submitted})


def transactionresult(request):
    data_submitted = False
    rows = list()
    default_data = list()
    debit_data = {
        'Walmart': 0,
        'India_Bazaar': 0,
        'Shift': 0,
        'Rent': 0,
        'Other': 0
    }
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT value FROM Total_Expense_Tracker_globalvariable WHERE key = "cash";')
            default_data.append(round(cursor.fetchall()[0][0],2))
            cursor.execute('SELECT value FROM Total_Expense_Tracker_globalvariable WHERE key = "bank";')
            default_data.append(round(cursor.fetchall()[0][0],2))
    except OperationalError as e:
        print(f"Error executing SQL query: {e}")

    if request.method == 'POST':
        form = TransactionResultForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            start_datestr = start_date.strftime('%Y-%m-%d')
            end_datestr = end_date.strftime('%Y-%m-%d')
            def convert_to_localtime(dt):
                if isinstance(dt, str):  # Check if dt is a string
                    dt = datetime.fromisoformat(dt)
                if isinstance(dt, datetime):
                    dt = timezone.make_aware(dt, timezone.utc)  # Make datetime timezone aware
                    return timezone.localtime(dt)  # Convert to local time
                return dt
            def convert_tospace(var):
                if '_' in var:
                    var = var.replace('_', ' ')
                    return var
                return var
            try:
                with connection.cursor() as cursor:
                    sql_query = """
                            SELECT * FROM Total_Expense_Tracker_transaction 
                            WHERE DATE(date_created) BETWEEN %s AND %s ORDER BY id ASC;
                        """
                    cursor.execute(sql_query, [start_datestr, end_datestr])
                    rows = cursor.fetchall()
                    rows = [(
                        convert_to_localtime(row[1]),
                        row[2],
                        row[3],
                        row[4],
                        convert_tospace(row[5])
                    ) for row in rows if row[2] != 0 or row[3] != 0]
                    creditList, debitList = [i[1] for i in rows if i[1] != 0], [i[2] for i in rows if i[2] != 0]
                    default_data.append(sum(creditList))
                    default_data.append(sum(debitList))
                    default_data.append(len(creditList))
                    default_data.append(len(debitList))
                    for row in rows:
                        if row[2] != 0:
                            if row[4] == "India Bazaar":
                                debit_data["India_Bazaar"] += row[2]
                            elif row[4] == "Shift":
                                debit_data["Shift"] += row[2]
                            elif row[4] in debit_data:
                                debit_data[row[4]] += row[2]
                            else:
                                debit_data['Other'] += row[2]
            except OperationalError as e:
                print(f"Error executing SQL query: {e}")
                rows = []
            data_submitted = True
    else:
        form = TransactionResultForm()
    errors = {}
    if form.errors:
        for field, error_list in form.errors.items():
            errors[form[field].label] = error_list


    return render(request, 'transactionresult.html', {'form': form, 'errors':errors,'data_submitted': data_submitted, 'rows':rows, 'default_data':default_data, 'debit_data':debit_data})

def shiftresult(request):
    data_submitted = False
    rows = list()
    finalData = list()
    no_data_found = False
    if request.method == 'POST':
        form = ShiftResultForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            shift_type = form.cleaned_data['shift_type']
            start_datestr = start_date.strftime('%Y-%m-%d')
            end_datestr = end_date.strftime('%Y-%m-%d')
            try:
                with connection.cursor() as cursor:
                    sql_query = """
                        SELECT 
                        S.shift_start, 
                        S.shift_end, 
                        S.hours_worked, 
                        T.credit, 
                        T.debit,
                        S.is_cash
                        FROM
                        Total_Expense_Tracker_shift S JOIN Total_Expense_Tracker_transaction T ON S.tip_id = T.id
                        WHERE S.is_cash = %s AND DATE(S.shift_start) BETWEEN %s AND %s ORDER BY S.shift_start;
                    """
                    if shift_type == 'Online':
                        cursor.execute(sql_query, [False, start_datestr, end_datestr])
                    elif shift_type == 'Offline':
                        cursor.execute(sql_query, [True, start_datestr, end_datestr])
                    else:
                        sql_query = """
                        SELECT 
                        S.shift_start, 
                        S.shift_end, 
                        S.hours_worked, 
                        T.credit, 
                        T.debit,
                        S.is_cash
                        FROM
                        Total_Expense_Tracker_shift S JOIN Total_Expense_Tracker_transaction T ON S.tip_id = T.id
                        WHERE DATE(S.shift_start) BETWEEN %s AND %s ORDER BY S.shift_start;
                    """
                        cursor.execute(sql_query, [start_datestr, end_datestr])
                    def convert_to_localtime(dt):
                        if isinstance(dt, str):  # Check if dt is a string
                            dt = datetime.fromisoformat(dt)
                        if isinstance(dt, datetime):
                            dt = timezone.make_aware(dt, timezone.utc)  # Make datetime timezone aware
                            return timezone.localtime(dt)  # Convert to local time
                        return dt
                    def expectedPayCalculate(is_cash,hours_worked):
                        try:
                            with connection.cursor() as cursor:
                                sql_query = """
                                            SELECT value FROM Total_Expense_Tracker_globalvariable
                                            WHERE key = %s;
                                            """
                                if is_cash:
                                    cursor.execute(sql_query, ['offline'])
                                else:
                                    cursor.execute(sql_query, ['online'])
                                pay = cursor.fetchall()
                        except OperationalError as e:
                            print(f"Error executing SQL query: {e}")
                            pay = []
                        return pay[0][0] * hours_worked
                    rows = cursor.fetchall()
                    if not rows:
                        no_data_found = True
                    rows = [
                        (
                            convert_to_localtime(row[0]),  # DATE_CREATED
                            convert_to_localtime(row[1]),  # SHIFT_START
                            row[2],
                            round(expectedPayCalculate(row[5],row[2]), 2),
                            row[3],
                            row[4],
                            round(expectedPayCalculate(row[5],row[2]) + row[3] - row[4], 2),
                            round(round(expectedPayCalculate(row[5],row[2]) + row[3] - row[4], 2)/row[2],2)
                        )
                        for row in rows
                    ]
                    for j in range(2,7):
                        finalData.append(round(sum([i[j] for i in rows]),2))
                    if finalData[0] != 0:finalData.append(round(finalData[4]/finalData[0],2))
            except OperationalError as e:
                print(f"Error executing SQL query: {e}")
                rows = []
            data_submitted = True
    else:
        form = ShiftResultForm()
    errors = {}
    if form.errors:
        for field, error_list in form.errors.items():
            errors[form[field].label] = error_list

    return render(request, 'shiftresult.html', {'form': form, 'errors':errors,'data_submitted': data_submitted, 'rows':rows, 'no_data_found': no_data_found, 'finalData':finalData})

def homepage(request):
    return render(request,'homepage.html')