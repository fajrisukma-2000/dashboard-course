from pathlib import Path
from unittest.mock import patch
import pandas as pd
from streamlit.testing.v1 import AppTest
from utils.model_utils import load_metadata

app = AppTest.from_file(str(Path.cwd() / 'sesi4/app_prediksi.py')).run(timeout=60)
assert not app.exception, app.exception

def metric(label):
    return next(m.value for m in app.metric if m.label == label)

app.slider(key='threshold').set_value(0.3).run(timeout=60)
low = int(metric('Prediksi churn').replace(',', ''))
app.slider(key='threshold').set_value(0.7).run(timeout=60)
high = int(metric('Prediksi churn').replace(',', ''))
assert low > high, (low, high)
assert load_metadata()['decision_threshold'] == 0.5
summary = app.dataframe[0].value
assert summary.to_numpy().sum() == 200
from utils.model_utils import predict, load_model
result = predict(load_model(), pd.read_csv('data/new_customers.csv'), load_metadata())
expected = result.loc[result.risk_category == 'Tinggi', 'monthly_charges'].sum()
assert metric('Potensi pendapatan berisiko per bulan') == f'Rp{expected:,.0f}'.replace(',', '.')
assert metric('Risiko tinggi') == str((result.risk_category == 'Tinggi').sum())

original_read = pd.read_csv
bad = original_read('data/new_customers_invalid.csv')
assert len(bad) == 3
assert (bad.contract_type == 'Mingguan').sum() == 1

def read_csv(path, *args, **kwargs):
    if str(path).endswith('new_customers.csv'):
        return bad.copy()
    return original_read(path, *args, **kwargs)

with patch('pandas.read_csv', side_effect=read_csv):
    invalid_app = AppTest.from_file(str(Path.cwd() / 'sesi4/app_prediksi.py')).run(timeout=60)
    assert not invalid_app.exception, invalid_app.exception
    assert any('contract_type' in e.value and 'Mingguan' in e.value for e in invalid_app.error)
print(f'PASS: threshold 0.3={low}, 0.7={high}; crosstab=200; pendapatan={expected}; CSV invalid menampilkan error.')

