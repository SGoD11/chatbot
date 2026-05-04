import pandas as pd
import os

DATA_PATH = "data/inventory.csv"   # change to .xlsx anytime

def load_data() -> pd.DataFrame:
    """
    Load from CSV or Excel.
    Later: replace this function body with DB query → rest of app untouched.
    """
    ext = os.path.splitext(DATA_PATH)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(DATA_PATH)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(DATA_PATH)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # compute margin column
    df["margin_pct"] = round(
        ((df["sell_price"] - df["buy_price"]) / df["buy_price"]) * 100, 1
    )
    df["profit_per_unit"] = df["sell_price"] - df["buy_price"]

    return df


def get_data_as_text() -> str:
    """Convert dataframe → readable text block for AI prompt."""
    df = load_data()
    lines = []
    for _, row in df.iterrows():
        lines.append(
            f"- [{row['category']}] {row['name']} | "
            f"Stock: {row['stock']} {row.get('unit','pcs')} | "
            f"Buy: ₹{row['buy_price']} | Sell: ₹{row['sell_price']} | "
            f"Margin: {row['margin_pct']}% | "
            f"Profit/unit: ₹{row['profit_per_unit']} | "
            f"Reorder at: {row.get('reorder_level','N/A')} | "
            f"Supplier: {row.get('supplier','N/A')}"
        )
    return "\n".join(lines)


def get_summary_stats() -> dict:
    """Quick stats — useful for /stats endpoint."""
    df = load_data()
    return {
        "total_items": len(df),
        "total_stock_value": round((df["stock"] * df["buy_price"]).sum(), 2),
        "avg_margin_pct": round(df["margin_pct"].mean(), 1),
        "low_stock_items": df[df["stock"] <= df["reorder_level"]]["name"].tolist()
        if "reorder_level" in df.columns else [],
        "top_margin_item": df.loc[df["margin_pct"].idxmax(), "name"],
        "categories": df["category"].unique().tolist()
    }