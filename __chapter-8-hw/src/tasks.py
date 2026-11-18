from pathlib import Path

import numpy as np
import pandas as pd

from src.db import db_connection, ensure_database, query_df
from src.utils import to_snake_case

# ../data/du_lieu_giai_thuong.xlsx
DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "du_lieu_giai_thuong.xlsx"

# sheet name = "giai_thuong"
TABLE = "giai_thuong"


def initial_data() -> None:
  ensure_database()
  df = pd.read_excel(DATA_FILE)
  df.columns = [to_snake_case(c) for c in df.columns]
  with db_connection(commit=True) as conn:
    df.to_sql(TABLE, conn, if_exists="replace", index=False)
  print(f"Loaded {len(df)} rows into '{TABLE}'.")


def analysis_numbers() -> None:
  with db_connection() as conn:
    total = query_df(f"SELECT COUNT(*) AS n FROM {TABLE}", conn=conn)
    top = query_df(f"SELECT * FROM {TABLE} LIMIT :n", {"n": 10}, conn=conn)

  print(f"Total: {total['n'][0]}")
  print(top)


def data_tong_hop_theo_thang(df: pd.DataFrame) -> pd.DataFrame:
  ngay = pd.to_datetime(df["ngay_phat_hanh_so_trung_thuong"])
  return (
    df.assign(thang=ngay.dt.to_period("M").astype(str))
    .groupby("thang", as_index=False)
    .agg(
      so_ngay_phat_hanh=("ngay_phat_hanh_so_trung_thuong", "nunique"),
      so_giai=("so_de_trung_thuong", "count"),
      tong_nguoi_trung=("so_nguoi_da_trung", "sum"),
      tong_gia_tri_da_trao=("tong_gia_tri_giai_thuong_da_trao", "sum"),
    )
    .sort_values("thang")
  )


def data_co_cau_giai_thuong(df: pd.DataFrame) -> pd.DataFrame:
  out = (
    df.groupby("gia_tri_giai_thuong", as_index=False)
    .agg(
      so_lan_xuat_hien=("so_de_trung_thuong", "count"),
      tong_nguoi_trung=("so_nguoi_da_trung", "sum"),
      tb_nguoi_trung_moi_giai=("so_nguoi_da_trung", "mean"),
      tong_gia_tri_da_trao=("tong_gia_tri_giai_thuong_da_trao", "sum"),
    )
    .sort_values("gia_tri_giai_thuong", ascending=False)
  )
  out["tb_nguoi_trung_moi_giai"] = out["tb_nguoi_trung_moi_giai"].round(2)
  out["ty_le_gia_tri"] = (
    out["tong_gia_tri_da_trao"] / out["tong_gia_tri_da_trao"].sum() * 100
  ).round(2)
  return out


def data_tan_suat_2_so_cuoi(df: pd.DataFrame) -> pd.DataFrame:
  so_cuoi = (df["so_de_trung_thuong"] % 100).map("{:02d}".format)
  out = (
    df.assign(hai_so_cuoi=so_cuoi)
    .groupby("hai_so_cuoi", as_index=False)
    .agg(
      so_lan_xuat_hien=("so_de_trung_thuong", "count"),
      tong_nguoi_trung=("so_nguoi_da_trung", "sum"),
      lan_cuoi_xuat_hien=("ngay_phat_hanh_so_trung_thuong", "max"),
    )
  )
  out["ty_le_xuat_hien"] = (
    out["so_lan_xuat_hien"] / out["so_lan_xuat_hien"].sum() * 100
  ).round(3)
  return out.sort_values("so_lan_xuat_hien", ascending=False)


DATAMARTS = {
  "data_tong_hop_theo_thang": data_tong_hop_theo_thang,
  "data_co_cau_giai_thuong": data_co_cau_giai_thuong,
  "data_tan_suat_2_so_cuoi": data_tan_suat_2_so_cuoi,
}


def build_datamarts() -> None:
  with db_connection(commit=True) as conn:
    base = query_df(f"SELECT * FROM {TABLE}", conn=conn)
    for name, build in DATAMARTS.items():
      dm = build(base)
      dm.to_sql(name, conn, if_exists="replace", index=False)
      print(f"\n[{name}] {len(dm)} rows")
      print(dm.head(5).to_string(index=False))


SPECIAL_PRIZE = 2_000_000_000

PRIZE_NAMES = {
  2_000_000_000: "Giai dac biet",
  50_000_000: "Giai phu dac biet",
  30_000_000: "Giai nhat",
  15_000_000: "Giai nhi",
  10_000_000: "Giai ba",
  6_000_000: "Giai khuyen khich",
  3_000_000: "Giai tu",
  1_000_000: "Giai nam",
  400_000: "Giai sau",
  200_000: "Giai bay",
  100_000: "Giai tam",
}


def analysis_prize_names() -> None:
  df = query_df("SELECT * FROM data_co_cau_giai_thuong")
  df.insert(0, "ten_giai", df["gia_tri_giai_thuong"].map(PRIZE_NAMES))
  print(df.to_string(index=False))


def analysis_special_prize_by_month() -> None:
  months = query_df(
    "SELECT thang, so_giai, tong_gia_tri_da_trao FROM data_tong_hop_theo_thang"
  )
  special = query_df(
    f"SELECT ngay_phat_hanh_so_trung_thuong AS ngay FROM {TABLE} "
    "WHERE gia_tri_giai_thuong = :v",
    {"v": SPECIAL_PRIZE},
  )
  special["thang"] = pd.to_datetime(special["ngay"]).dt.to_period("M").astype(str)
  counts = special.groupby("thang").size().reset_index(name="so_giai_dac_biet")

  df = months.merge(counts, on="thang", how="left")
  df["so_giai_dac_biet"] = df["so_giai_dac_biet"].fillna(0).astype(int)
  avg = df["tong_gia_tri_da_trao"].mean()
  df["muc_chi"] = np.where(df["tong_gia_tri_da_trao"] > avg, "Cao", "Thap")

  print("Top 10 months by payout:")
  print(df.nlargest(10, "tong_gia_tri_da_trao").to_string(index=False))


def analysis_high_low_numbers() -> None:
  sql = (
    "SELECT hai_so_cuoi, so_lan_xuat_hien, ty_le_xuat_hien "
    "FROM data_tan_suat_2_so_cuoi WHERE ty_le_xuat_hien {cond} 1 "
    "ORDER BY so_lan_xuat_hien {order} LIMIT 5"
  )
  hot = query_df(sql.format(cond=">", order="DESC"))
  cold = query_df(sql.format(cond="<", order="ASC"))

  df = pd.concat([hot.assign(nhom="High"), cold.assign(nhom="Low")], ignore_index=True)
  print(df.to_string(index=False))
