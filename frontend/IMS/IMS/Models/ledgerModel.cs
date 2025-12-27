using DocumentFormat.OpenXml.Office2016.Drawing.Command;
using System;
using System.Configuration;

namespace IMS.Models
{
    public class LedgerItem
    {

        public void CopyFrom(LedgerItem o)
        {
            if (o == null) return;

            this.idx = o.idx;
            this.Ledger_code = o.Ledger_code;
            this.ledger_page = o.ledger_page;

            this.ohs_number = o.ohs_number;
            this.isg_number = o.isg_number;
            this.ssg_number = o.ssg_number;

            this.part_number = o.part_number;
            this.nomenclature = o.nomenclature;
            this.a_u = o.a_u;

            this.no_off = o.no_off;
            this.scl_auth = o.scl_auth;
            this.unsv_stock = o.unsv_stock;
            this.rep_stock = o.rep_stock;
            this.serv_stock = o.serv_stock;

            this.msc = o.msc;
            this.ved = o.ved;
            this.in_house = o.in_house;

            this.dues_in = o.dues_in;
            this.consumption = o.consumption;

            this.bin_number = o.bin_number;
            this.group = o.group;

            // Extra fields
            this.cos_sec = o.cos_sec;
            this.cab_no = o.cab_no;
            this.old_pg_ref = o.old_pg_ref;
            this.Assy_Comp = o.Assy_Comp;
            this.Re_ord_lvl = o.Re_ord_lvl;
            this.safety_stk = o.safety_stk;

            // Response-only fields
            this.cds_unsv_stock = o.cds_unsv_stock;
            this.cds_rep_stock = o.cds_rep_stock;
            this.cds_serv_stock = o.cds_serv_stock;

            this.lpp = o.lpp;
            this.rate = o.rate;
            this.rmks = o.rmks;
            this.lpp_dt = o.lpp_dt;

            // Local WPF-side fields
            this.Store = o.Store;
            this.SubStore = o.SubStore;
        }

        public int idx { get; set; }
        public string Ledger_code { get; set; }
        public string ledger_page { get; set; }
        public string? ohs_number { get; set; }
        public string? isg_number { get; set; }
        public string? ssg_number { get; set; }
        public string part_number { get; set; }
        public string nomenclature { get; set; }
        public string a_u { get; set; }
        public int no_off { get; set; }
        public int scl_auth { get; set; }
        public int unsv_stock { get; set; }
        public int rep_stock { get; set; }
        public int serv_stock { get; set; }
        public string msc { get; set; }
        public string ved { get; set; }
        public string in_house { get; set; }
        public int? dues_in { get; set; }
        public int? consumption { get; set; }
        public string? bin_number { get; set; }
        public string? group { get; set; }

        // Extra fields from LedgerMaintanenceCreate
        public string cos_sec { get; set; }
        public string cab_no { get; set; }
        public double old_pg_ref { get; set; }
        public string Assy_Comp { get; set; }
        public int Re_ord_lvl { get; set; }
        public int safety_stk { get; set; }

        // Response-only fields
        public int cds_unsv_stock { get; set; }
        public int cds_rep_stock { get; set; }
        public int cds_serv_stock { get; set; }
        public string? lpp { get; set; }
        public double rate { get; set; }
        public string rmks { get; set; }
        public string lpp_dt { get; set; }

        // Local WPF-side fields
        public string Store { get; set; }
        public string SubStore { get; set; }
    }
}

