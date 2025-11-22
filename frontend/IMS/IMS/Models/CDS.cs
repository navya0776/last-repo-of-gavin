using System;

namespace IMS.Models
{
    public class CDS
    {
        public bool SEL { get; set; }

        // ===== Primary identifiers =====
        public int job_no { get; set; }
        public DateTime? job_date { get; set; }
        public string ledger_page { get; set; }

        // ===== Item details =====
        public int? ohs_no { get; set; }
        public string part_number { get; set; }
        public string spart_no { get; set; }
        public string nomenclature { get; set; }
        public string auth_officer { get; set; }

        // ===== Demand / Addl Demand =====
        public int? dem_ref_no { get; set; }
        public int? add_dem_no { get; set; }

        // ===== Stock & Issue Details =====
        public string curr_stock { get; set; }
        public string now_issue_qty { get; set; }
        public string recd_qty { get; set; }
        public DateTime? date_nr { get; set; }

        // ===== OSS Issue series =====
        public int? oss_qty1 { get; set; }
        public string oss_iv1 { get; set; }
        public DateTime? oss_ivdt1 { get; set; }

        public int? oss_qty2 { get; set; }
        public string oss_iv2 { get; set; }
        public DateTime? oss_ivdt2 { get; set; }

        public int? oss_qty3 { get; set; }
        public string oss_iv3 { get; set; }
        public DateTime? oss_ivdt3 { get; set; }

        // ===== CDS Issue series =====
        public string cds_iv1 { get; set; }
        public DateTime? cds_ivdt1 { get; set; }
        public int? cds_qty2 { get; set; }
        public string cds_iv2 { get; set; }
        public DateTime? cds_ivdt2 { get; set; }

        // ===== Extra CDS fields =====
        public string cds_qty1 { get; set; }   // If exist
        public string cds_qty3 { get; set; }   // If exist
        public string cds_iv3 { get; set; }
        public DateTime? cds_ivdt3 { get; set; }

        // ===== LPR =====
        public int? lpr_qty { get; set; }
        public string lpr_no { get; set; }
        public DateTime? lpr_date { get; set; }

        // ===== Demand Control =====
        public string demand_ctrl_no { get; set; }
        public DateTime? demand_ctrl_date { get; set; }

        // ===== Dem ID =====
        public string dem_id { get; set; }
    }
}
