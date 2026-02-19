import streamlit as st
import pandas as pd
from datetime import datetime
import json
import io

st.set_page_config(page_title="Browser Share Config Generator", layout="wide")

st.title("Browser Share LGF Config Generator")

# =====================================================
# DOWNLOAD TEMPLATE SECTION
# =====================================================

st.subheader("Download CSV Template")

template_df = pd.DataFrame(columns=[
    "customer", "platform", "web_or_app", "url", "location_id",
    "city_display_name", "category", "sub_category",
    "sub_sub_category", "sub_sub_sub_category",
    "sub_sub_sub_sub_category"
])

csv_template = template_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Template",
    data=csv_template,
    file_name="Browsershare_template.csv",
    mime="text/csv"
)

st.divider()

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def trim_strings(df):
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def clean_input_detail(detail_str):
    try:
        detail_dict = json.loads(detail_str)
        cleaned = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in detail_dict.items()}
        return json.dumps(cleaned)
    except:
        return detail_str

# =====================================================
# INPUT METHOD SELECTION
# =====================================================

method = st.radio("Choose Input Method", ["CSV Upload", "Manual Entry"])

data_list = []

# =====================================================
# CSV UPLOAD SECTION
# =====================================================

if method == "CSV Upload":

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df_csv = pd.read_csv(uploaded_file)
        df_csv = df_csv.fillna("")

        required_cols = [
            "customer", "platform", "web_or_app", "url", "location_id",
            "city_display_name", "category", "sub_category",
            "sub_sub_category", "sub_sub_sub_category",
            "sub_sub_sub_sub_category"
        ]

        missing_cols = [col for col in required_cols if col not in df_csv.columns]

        if missing_cols:
            st.error(f"Missing columns: {missing_cols}")
            st.stop()

        for _, row in df_csv.iterrows():

            categories = {"type": "url", "value": row["url"]}

            if row["category"]:
                categories["category"] = row["category"]
            if row["sub_category"]:
                categories["sub_category"] = row["sub_category"]
            if row["sub_sub_category"]:
                categories["sub_sub_category"] = row["sub_sub_category"]
            if row["sub_sub_sub_category"]:
                categories["sub_sub_sub_category"] = row["sub_sub_sub_category"]
            if row["sub_sub_sub_sub_category"]:
                categories["sub_sub_sub_sub_category"] = row["sub_sub_sub_sub_category"]

            data_list.append({
                "customer": row["customer"],
                "platform": str(row["platform"]).strip().lower(),
                "web_or_app": str(row["web_or_app"]).strip().lower(),
                "url": row["url"],
                "location_id": row["location_id"],
                "city_display_name": row["city_display_name"],
                "input_detail": json.dumps(categories)
            })

        st.success("CSV Processed Successfully")

# =====================================================
# MANUAL ENTRY SECTION
# =====================================================

elif method == "Manual Entry":

    with st.form("manual_form"):

        customer = st.text_input("Customer")
        platform = st.text_input("Platform")
        web_or_app = st.text_input("Web or App")
        url = st.text_input("URL")
        location_id = st.text_input("Location ID")
        city_display_name = st.text_input("City Display Name")

        st.subheader("Categories (Optional)")

        category = st.text_input("Category")
        sub_category = st.text_input("Sub Category")
        sub_sub_category = st.text_input("Sub Sub Category")
        sub_sub_sub_category = st.text_input("Sub Sub Sub Category")
        sub_sub_sub_sub_category = st.text_input("Sub Sub Sub Sub Category")

        submitted = st.form_submit_button("Add Entry")

        if submitted:

            if not all([customer, platform, web_or_app, url, location_id, city_display_name]):
                st.error("Please fill all mandatory fields.")
            else:

                categories = {"type": "url", "value": url}

                if category:
                    categories["category"] = category
                if sub_category:
                    categories["sub_category"] = sub_category
                if sub_sub_category:
                    categories["sub_sub_category"] = sub_sub_category
                if sub_sub_sub_category:
                    categories["sub_sub_sub_category"] = sub_sub_sub_category
                if sub_sub_sub_sub_category:
                    categories["sub_sub_sub_sub_category"] = sub_sub_sub_sub_category

                data_list.append({
                    "customer": customer.strip(),
                    "platform": platform.strip().lower(),
                    "web_or_app": web_or_app.strip().lower(),
                    "url": url.strip(),
                    "location_id": location_id.strip(),
                    "city_display_name": city_display_name.strip(),
                    "input_detail": json.dumps(categories)
                })

                st.success("Entry Added Successfully")

# =====================================================
# GENERATE EXCEL
# =====================================================

if data_list:

    config_rows = []
    input_rows = []
    recurrence_rows = []
    option_rows = []
    location_rows = []

    today_day = datetime.now().strftime("%A")

    for entry in data_list:

        customer = entry["customer"]
        platform = entry["platform"]
        web_or_app = entry["web_or_app"]
        url = entry["url"]
        location_id = entry["location_id"]
        city_display_name = entry["city_display_name"]
        input_detail = entry["input_detail"]

        input_group = f"{customer}_India_browser_share_{platform}"
        location_group = f"{customer}_India_{platform}_{location_id}_browser_share"

        config_rows.append({
            "customer": customer,
            "flow_type": "lgf",
            "web_or_app": web_or_app,
            "input_group": input_group,
            "location_group": location_group,
            "recurrence_id": f"recur_id_{customer}_browser_share",
            "option_id": f"opt_id_{customer}_{platform}_browser_share",
            "platform": platform,
            "staging_status": ""
        })

        input_rows.append({
            "customer": customer,
            "platform": platform,
            "country": "India",
            "input_detail": input_detail,
            "input_group": input_group,
            "input_sub_group": "browser share",
            "input_type": "url",
            "input_value": url
        })

        recurrence_rows.append({
            "customer": customer,
            "recurrence_id": f"recur_id_{customer}_browser_share",
            "type": "Weekly",
            "recurrence_day": today_day,
            "is_active": "TRUE"
        })

        option_rows.append({
            "customer": customer,
            "option_id": f"opt_id_{customer}_{platform}_browser_share",
            "options_detail": json.dumps({"number_of_pages": 1})
        })

        location_rows.append({
            "customer": customer,
            "location_id": location_id,
            "city_display_name": city_display_name,
            "location_group": location_group
        })

    config_df = trim_strings(pd.DataFrame(config_rows).drop_duplicates())
    input_df = trim_strings(pd.DataFrame(input_rows))
    recurrence_df = trim_strings(pd.DataFrame(recurrence_rows).drop_duplicates())
    option_df = trim_strings(pd.DataFrame(option_rows).drop_duplicates())
    location_df = trim_strings(pd.DataFrame(location_rows).drop_duplicates())

    input_df["input_detail"] = input_df["input_detail"].apply(clean_input_detail)

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        config_df.to_excel(writer, sheet_name="config", index=False)
        input_df.to_excel(writer, sheet_name="input", index=False)
        recurrence_df.to_excel(writer, sheet_name="recurrence", index=False)
        option_df.to_excel(writer, sheet_name="option", index=False)
        location_df.to_excel(writer, sheet_name="location", index=False)

    output.seek(0)

    st.divider()

    st.download_button(
        label="Download Excel File",
        data=output,
        file_name="Browsershare_config_multi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )