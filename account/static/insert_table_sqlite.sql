INSERT INTO CREDIT(id, source, transaction_date, bookkeeping_date, card_id, transaction_money,
balance_currency, balance_money, transaction_desc, payment_type_id, payment_type_name,
consumption_name, consumption_id, consume_name, consume_id, keyword, demoarea) 
values(null, '%s', datetime('%s'), datetime('%s'), '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');