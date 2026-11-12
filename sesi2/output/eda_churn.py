# sesi2/eda_churn.py — EDA lengkap dengan Pandas + Matplotlib (jalankan: python sesi2/output/eda_churn.py) 
from pathlib import Path 
import matplotlib 
matplotlib.use("Agg")            # agar bisa jalan tanpa layar; hapus baris ini di Jupyter 
import matplotlib.pyplot as plt 
from matplotlib.patches import FancyBboxPatch 
import numpy as np 
import pandas as pd 
  
ROOT = Path(__file__).resolve().parents[2] 
OUT = ROOT / "sesi2" / "output" 
OUT.mkdir(parents=True, exist_ok=True) 
  
# ---------- Gaya visual konsisten untuk semua grafik ---------- 
BIRU, ORANYE, HIJAU, KUNING, UNGU = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#4a3aa7" 
TEKS, TEKS2, GRID = "#0b0b0b", "#52514e", "#e6e5e0" 
STATUS = {"Bertahan": BIRU, "Churn": ORANYE} 
plt.rcParams.update({ 
    "figure.dpi": 110, "savefig.dpi": 200, "font.size": 10, "axes.titlesize": 12, 
    "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.spines.top": False, 
    "axes.spines.right": False, "axes.edgecolor": "#b9b8b2", "axes.grid": True, 
    "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True, 
    "axes.labelcolor": TEKS2, "xtick.color": TEKS2, "ytick.color": TEKS2, 
}) 
KONTRAK = ["Bulanan", "Tahunan", "Dua Tahun"] 
  
def simpan(fig, nama): 
    fig.tight_layout() 
    fig.savefig(OUT / nama, bbox_inches="tight", facecolor="white") 
    plt.close(fig) 
  
# =============== 1. LOAD DATA =============== 
df = pd.read_csv(ROOT / "sesi2" / "customer_churn.csv", parse_dates=["signup_date"]) 
df["status"] = df["churn"].map({0: "Bertahan", 1: "Churn"}) 
  
# =============== 2. PROFILING =============== 
print("Shape:", df.shape) 
profil = pd.DataFrame({"tipe": df.dtypes.astype(str), "missing": df.isna().sum(), 
                       "unik": df.nunique()}) 
print(profil) 
print("Duplikat customer_id:", df["customer_id"].duplicated().sum()) 
  
# =============== 3. STATISTIK DESKRIPTIF =============== 
num_cols = ["tenure_months", "monthly_charges", "total_charges", "num_complaints", "support_calls"] 
print(df[num_cols].describe().T.round(1)) 
print("Churn rate keseluruhan: {:.1%}".format(df["churn"].mean())) 
  
# =============== 4. CLEANING RINGAN =============== 
df["total_charges"] = df["total_charges"].fillna(df["total_charges"].median()) 
df["kelompok_tenure"] = pd.cut(df["tenure_months"], bins=[0, 12, 24, 48, 72], 
                               labels=["0-12", "13-24", "25-48", "49-72"]) 
  
# =============== 5. FILTERING =============== 
berisiko = df[(df["contract_type"] == "Bulanan") & (df["num_complaints"] >= 3)] 
print(f"Bulanan & keluhan>=3: {len(berisiko)} pelanggan, churn {berisiko['churn'].mean():.1%}") 
print("Fiber di Jawa:", len(df.query("region == 'Jawa' and internet_service == 'Fiber'"))) 
  
# =============== 6. GROUPING =============== 
churn_kontrak = (df.groupby("contract_type") 
                   .agg(pelanggan=("customer_id", "count"), churn_rate=("churn", "mean"), 
                        rata2_tagihan=("monthly_charges", "mean")) 
                   .reindex(KONTRAK)) 
print(churn_kontrak.round(3)) 
pivot = pd.pivot_table(df, values="churn", index="region", columns="segment", aggfunc="mean") 
print(pivot.round(3))
