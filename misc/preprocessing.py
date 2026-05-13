import pandas as pd
import argparse

def get_agency_summary(data):
    print(data.iloc[0][["DEPARTMENT","AGENCY"]])

    cols = ["Personnel Services","Maintenance and Other Operating Expenses","Financial Expenses","Capital Outlays"]

    # Masks
    is_item_included = (data.FUNDCD=="10101101")|(data.SORDER==2)|(data.DEPARTMENT=="35")
    is_expense_type = {}
    for c in cols:
        is_expense_type[c] = data.UACS_EXP_DSC==c

    if data.SORDER.values[0]==2:
        data_obj = [{"Name":"Total","type":"group"}]
        for c in cols:
            data_obj[0][c] = 0
        subdata = data.loc[~pd.isna(data.AMT)].reset_index(drop=True)
        for x in subdata.itertuples():
            data_obj.append({"Name":x.DSC,"type":"activity",x.UACS_EXP_DSC:x.AMT})
            if x.UACS_EXP_DSC in data_obj[0]:
                data_obj[0][x.UACS_EXP_DSC] += x.AMT
        total_obj = {"Name":"Total New Appropriations","type":"total_sum"}
        for c in cols:
            if c in data_obj[0]:
                total_obj[c] = data_obj[0][c]
        data_obj.append(total_obj)
        summary_df = pd.DataFrame(data_obj)
        summary_df["Total"] = summary_df[cols].sum(axis=1)

        return summary_df

    data_obj = []
    # "Purpose" level (Regular Programs)
    data_obj.append({"Name":"A. Regular Programs","type":"group"})
    reg_obj = [{"Name":"General Administration and Support","type":"purpose"},
               {"Name":"Support to Operations","type":"purpose"},
               {"Name":"Operations","type":"purpose"},
               {"Name":"Total, Regular Program(s)","type":"sum"}]
    for c in cols:
        data_sub = data[is_item_included&is_expense_type[c]]
        reg_obj[0][c] = 1000*int(data_sub.loc[(data_sub.PREXC_FPAP_ID.str.get(0)=="1")&(data_sub.PREXC_FPAP_ID.str.get(6)=="1"),"AMT"].sum())
        reg_obj[1][c] = 1000*int(data_sub.loc[(data_sub.PREXC_FPAP_ID.str.get(0)=="2")&(data_sub.PREXC_FPAP_ID.str.get(6)=="1"),"AMT"].sum())
        reg_obj[2][c] = 1000*int(data_sub.loc[(data_sub.PREXC_FPAP_ID.str.get(0)=="3")&(data_sub.PREXC_FPAP_ID.str.get(6)=="1"),"AMT"].sum())
        reg_obj[3][c] = reg_obj[0][c] + reg_obj[1][c] + reg_obj[2][c]

    # "Programs" level (Regular Programs)
    for i in range(1,3+1):
        data_obj.append(reg_obj[i-1])
        progs = data.loc[(data.PREXC_LEVEL==3)&(data.PREXC_FPAP_ID.str.get(0)==f"{i}")]
        progs_startId = progs.PREXC_FPAP_ID.str[:3+1].values.tolist()
        if len(progs)>0:
            for prog in progs.itertuples():
                entry = {"Name":prog.DSC,"type":"program"}
                startID = prog.PREXC_FPAP_ID[:3+1]
                for c in cols:
                    entry[c] = 1000*int(data.loc[is_item_included & is_expense_type[c] & data.PREXC_FPAP_ID.str.startswith(startID) & (data.PREXC_FPAP_ID.str.get(6)=="1"),"AMT"].sum())
                data_obj.append(entry)

                # "Subprograms" level (Under Programs)
                subprogs = data.loc[(data.PREXC_LEVEL==4)&(data.PREXC_FPAP_ID.str.startswith(startID))]
                subprogs_startId = subprogs.PREXC_FPAP_ID.str[:5+1].values.tolist()

                for subprog in subprogs.itertuples():
                    entry = {"Name":subprog.DSC,"type":"subprogram"}
                    substartID = subprog.PREXC_FPAP_ID[:5+1]
                    for c in cols:
                        entry[c] = 1000*int(data.loc[is_item_included & is_expense_type[c] & data.PREXC_FPAP_ID.str.startswith(substartID) & (data.PREXC_FPAP_ID.str.get(6)=="1"),"AMT"].sum())
                    data_obj.append(entry)

                    # "Activities" level (Under Subprograms)
                    acts = data.loc[(data.PREXC_LEVEL==7)&(data.PREXC_FPAP_ID.str.startswith(substartID))&(~pd.isna(data.AMT)) & (data.PREXC_FPAP_ID.str.get(6)=="1")].drop_duplicates(subset=["PREXC_FPAP_ID","DSC"])
                    for act in acts.itertuples():
                        entry = {"Name":act.DSC,"type":"activity_subprogram"}
                        for c in cols:
                            entry[c] = 1000*int(data.loc[is_item_included & is_expense_type[c] & (data.PREXC_FPAP_ID==act.PREXC_FPAP_ID),"AMT"].sum())
                        data_obj.append(entry)

                # "Activities" level (Under Programs)
                acts = data.loc[(data.PREXC_LEVEL==7)&(data.PREXC_FPAP_ID.str.startswith(startID))&(~data.PREXC_FPAP_ID.str[:5+1].isin(subprogs_startId))&(~pd.isna(data.AMT)) & (data.PREXC_FPAP_ID.str.get(6)=="1")].drop_duplicates(subset=["PREXC_FPAP_ID","DSC"])
                for act in acts.itertuples():
                    entry = {"Name":act.DSC,"type":"activity_program"}
                    for c in cols:
                        entry[c] = 1000*int(data.loc[is_item_included & is_expense_type[c] & (data.PREXC_FPAP_ID==act.PREXC_FPAP_ID),"AMT"].sum())
                    data_obj.append(entry)

        # "Activities" level (Under Cost Structure)
        acts = data.loc[(data.PREXC_LEVEL==7)&(data.PREXC_FPAP_ID.str.get(0)==f"{i}")&(~data.PREXC_FPAP_ID.str[:3+1].isin(progs_startId))&(~pd.isna(data.AMT)) & (data.PREXC_FPAP_ID.str.get(6)=="1")].drop_duplicates(subset=["PREXC_FPAP_ID","DSC"])
        for act in acts.itertuples():
            entry = {"Name":act.DSC,"type":"activity"}
            for c in cols:
                entry[c] = 1000*int(data.loc[is_item_included & is_expense_type[c] & (data.PREXC_FPAP_ID==act.PREXC_FPAP_ID),"AMT"].sum())
            data_obj.append(entry)

    data_obj.append(reg_obj[3])

    # Projects
    data_obj.append({"Name":"B. Project(s)","type":"group"})
    proj_obj = [{"Name":"Locally-Funded Project(s)","type":"purpose"},
               {"Name":"Foreign-Assisted Project(s)","type":"purpose"},
               {"Name":"Total, Project(s)","type":"sum"}]
    for c in cols:
        proj_obj[0][c] = 1000*int(data.loc[is_item_included & is_expense_type[c] & (data.PREXC_FPAP_ID.str.get(6)=="2"),"AMT"].sum())
        proj_obj[1][c] = 1000*int(data.loc[is_expense_type[c] & (data.PREXC_FPAP_ID.str.get(6)=="3"),"AMT"].sum())
        proj_obj[2][c] = proj_obj[0][c] + proj_obj[1][c]

    # Local Projects
    data_obj.append(proj_obj[0])
    local_proj_df = data.loc[(data.PREXC_LEVEL==7)&(data.PREXC_FPAP_ID.str.get(6)=="2")&(~pd.isna(data.AMT))].drop_duplicates(subset=["PREXC_FPAP_ID","DSC"])
    for lproj in local_proj_df.itertuples():
        entry = {"Name":lproj.DSC,"type":"project"}
        for c in cols:
            entry[c] = 1000*int(data.loc[is_item_included & is_expense_type[c] & (data.PREXC_FPAP_ID==lproj.PREXC_FPAP_ID),"AMT"].sum())
        data_obj.append(entry)

    data_obj.append(proj_obj[1])
    foreign_proj_df = data.loc[(data.PREXC_LEVEL==7)&(data.PREXC_FPAP_ID.str.get(6)=="3")&(~pd.isna(data.AMT))].drop_duplicates(subset=["PREXC_FPAP_ID","DSC"])
    for fproj in foreign_proj_df.itertuples():
        entry = {"Name":fproj.DSC,"type":"project"}
        for c in cols:
            entry[c] = 1000*int(data.loc[is_expense_type[c] & (data.PREXC_FPAP_ID==fproj.PREXC_FPAP_ID),"AMT"].sum())
        data_obj.append(entry)

    data_obj.append(proj_obj[2])

    fin_obj = {"Name":"Total New Appropriations","type":"total_sum"}
    for c in cols:
        fin_obj[c] = reg_obj[-1][c] + proj_obj[-1][c]

    data_obj.append(fin_obj)

    summary_df = pd.DataFrame(data_obj)
    summary_df["Total"] = summary_df[cols].sum(axis=1)

    return summary_df

def get_agency_exptype(data):
    exp_types = [x for x in data.UACS_EXP_DSC.unique().tolist() if not pd.isna(x)]
    df_list = []
    for exp in exp_types:
        df_list.append(pd.DataFrame([{"Name":exp,"AMT":None}]))
        df_list.append(data.loc[data.UACS_EXP_DSC==exp,["UACS_OBJ_DSC","AMT"]].groupby("UACS_OBJ_DSC",as_index=False,sort=False).sum().rename(columns={"UACS_OBJ_DSC":"Name"}))

    if len(df_list) > 0:
        return pd.concat(df_list)
    else:
        return pd.DataFrame(columns=["Name","AMT"])


def preprocess(datapath, out_directory):
    if datapath.split(".")[-1] == "xlsx":
        data = pd.read_excel(datapath)
    elif datapath.split(".")[-1] == "csv":
        data = pd.read_csv(datapath)
    elif datapath.split(".")[-1] == "parquet":
        data = pd.read_parquet(datapath)
    
    if pd.isna(data.iloc[-1]["PREXC_FPAP_ID"]):
        print("Removing last row")
        data = data.iloc[:-1]

    data.loc[pd.isna(data.UACS_DPT_DSC),"UACS_DPT_DSC"] = "Unspecified"
    data.loc[pd.isna(data.UACS_AGY_DSC),"UACS_AGY_DSC"] = "Unspecified"

    print("Getting budget summary per department/agency")
    data_summary = data.groupby(["UACS_DPT_DSC","UACS_AGY_DSC"],as_index=True,sort=False).apply(get_agency_summary).reset_index(level=[0,1]).reset_index(drop=True)

    print("Getting budget details per line item description and per department/agency")
    data_summary_exp = data.groupby(["UACS_DPT_DSC","UACS_AGY_DSC"],as_index=True,sort=False).apply(get_agency_exptype).reset_index(level=[0,1]).reset_index(drop=True)
    data_summary_exp["AMT"] = 1000*data_summary_exp["AMT"]

    data_summary.to_parquet(out_directory+f"/{datapath.split("/")[-1].split(".")[0]}_summary.parquet")
    data_summary_exp.to_parquet(out_directory+f"/{datapath.split("/")[-1].split(".")[0]}_exptype.parquet")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output",help="Output file directory")
    parser.add_argument("-i","--input",help="Input file")
    args = parser.parse_args()

    if (not args.input) or (not args.output):
        print("Missing arguments")

    else:
        preprocess(args.input,args.output)